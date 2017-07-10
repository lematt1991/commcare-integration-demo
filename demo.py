#!/usr/bin/env python

from commcare import Commcare
from getpass import getpass
import psycopg2, pdb, json, argparse
from datetime import datetime
from psycopg2.extensions import AsIs

parser = argparse.ArgumentParser()
parser.add_argument('--reports', action='store_true', help='List all reports in a JSON file')
parser.add_argument('--update', action='store_true', help='Update the database')
args = parser.parse_args()

conn = psycopg2.connect(dbname='commcare-demo')
cursor = conn.cursor()

# Get the user's password and create the Commcare client.
pw = getpass('Enter password: ')
client = Commcare('matthew.le@mssm.edu', pw, 'atlas-api-demo')

def updateTable():
	# Fetch the neweset dates
	cursor.execute('SELECT MAX(modified_on) FROM gps_case_data')
	start_date, = cursor.fetchone()
	date_filter = None
	if start_date is not None:
		date_filter = client.mkDateRange(start_date, datetime.now(), 'modified_on_6457b79c_2')

	for rows in client.getReport('988058bd3248104e3114ecac4b3fc674', filter=date_filter):
		cursor.executemany("""
			INSERT INTO gps_case_data(
				name, 
				gps,
				latitude, 
				longitude, 
				altitude, 
				precision, 
				modified_on
			)
			VALUES (
				%(name)s,
				%(gps)s,
				%(latitude)s,
				%(longitude)s,
				%(altitude)s,
				%(precision)s,
				%(modified_on)s
			)
		""", rows)
	conn.commit()

if args.reports:
    report = client.listForms()
    json.dump(report, open('reports.json', 'w'), indent=2)
elif args.update:
	updateTable()