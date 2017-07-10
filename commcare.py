#!/usr/bin/env python

import requests, pdb, json, re
from time import sleep

BASE = 'https://www.commcarehq.org'

def encodeParams(filter):
    if filter is None:
        return ''
    else:
        params = map(lambda p: '%s=%s' % (p, filter[p]), filter.keys())
        return '?%s' % '&'.join(params)

# Rename columns to something that is PostgreSQL compliant
def renameCol(col):
    col = col.split('/')[-1]
    return re.sub(' +', '_', col.lower())

class Commcare:
    def __init__(self, username, password, project):
        self.project = project
        self.session = requests.Session()
        self.session.auth = (username, password)

    def mkDateRange(self, filter_name, begin, end):
        return {
            '%s-start' % filter_name : str(begin).split(' ')[0],
            '%s-end' % filter_name : str(end).split(' ')[0]
        }

    def listForms(self):
        req = self.session.get('%s/a/%s/api/v0.5/simplereportconfiguration/?format=json' % (BASE, self.project))
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            print(req.text)
            raise Exception(req.text)

    def getReport(self, reportID, filter=None):
        url = '/a/%s/api/v0.5/configurablereportdata/%s%s' % (self.project, reportID, encodeParams(filter))

        total = 0

        while url != '':
            req = self.session.get('%s/%s' % (BASE, url))
            if req.status_code != 200:
                if req.status_code == 429: #Throttling
                    sleep(1)
                    continue
                pdb.set_trace()
                print(req.text)
                raise Exception(req.text)

            body = json.loads(req.text)

            print('Done with %d out of %d' % (total, body['total_records']))

            total += len(body['data'])

            data = body['data']
            cols = body['columns']

            colMap = {}
            for rec in cols:
                colMap[rec['slug']] = renameCol(rec['header'])

            yield [{colMap[k] : None if r[k] == '' else r[k] for k in r.keys()} for r in data]
            url = body['next_page']

