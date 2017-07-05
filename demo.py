#!/usr/bin/env python

from commcare import Commcare
from getpass import getpass
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--reports', action='store_true', help='List all reports in a JSON file')
args = parser.parse_args()

# Get the user's password and create the Commcare client.
pw = getpass('Enter password: ')
client = Commcare('matthew.le@mssm.edu', pw, 'atlas-api-demo')

if args.reports:
    report = client.listForms()
    json.dump(report, open('reports.json', 'w'), indent=2)



