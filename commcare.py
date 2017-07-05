#!/usr/bin/env python

import requests
import pdb
import json

BASE = 'https://www.commcarehq.org'

def encodeParams(filter):
    if filter is None:
        return ''
    else:
        params = map(lambda p: '%s=%s' % (p, filter[p]), filter.keys())
        return '?%s' % '&'.join(params)

class Commcare:
    def __init__(self, username, password, project):
        self.project = project
        self.session = requests.Session()
        self.session.auth = (username, password)

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
                pdb.set_trace()
                print(req.text)
                raise Exception(req.text)

            body = json.loads(req.text)

            print('Done with %d out of %d' % (total, body['total_records']))

            total += len(body['data'])

            yield body['data'], body['columns']
            url = body['next_page']

