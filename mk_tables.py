#!/usr/bin/env python

import pandas, pdb, re, requests, os, numpy, glob
from sqlalchemy import create_engine
import getpass

client = requests.session()
engine = create_engine('postgresql://localhost:5432/commcare-demo')


# Rename columns to something that is PostgreSQL compliant
def renameCol(col):
    col = col.split('/')[-1]
    return re.sub(' +', '_', col.lower())

def mk_case_data_table():
    id = '988058bd3248104e3114ecac4b3fc674'
    df = downloadFile(id, 'case_data', 'atlas-api-demo')
    df.to_sql('case_data', engine, if_exists='replace', index=False, schema='tula')

if __name__ == '__main__':

    for file in glob.glob('data/*.xlsx'):
        df = pandas.read_excel(file)
        df.columns = map(renameCol, df.columns)
        table_name = renameCol(os.path.splitext(os.path.basename(file))[0])
        print('Creating %s' % table_name)
        df.to_sql(table_name, engine, if_exists='replace', index=False)















