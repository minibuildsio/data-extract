import fitbit
import gather_keys_oauth2 as Oauth2
import datetime as dt
import os

import argparse


parser = argparse.ArgumentParser(description='Extract data from FitBit.')
parser.add_argument(
    "start_date", help="The date to start the extract from (yyyy-mm-dd)", nargs='?')

args = parser.parse_args()

heading = ['date', 'calories', 'carbs', 'fat', 'protein', 'sugar']
print('\t'.join(heading))

# create a list of dates from start date to yesterday (default to [yesterday] if no start date provided)
yesterday = dt.datetime.today() - dt.timedelta(days=1)

if args.start_date is None:
    dates = [yesterday]
else:
    start_date = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
    if start_date > yesterday:
        raise 'Start date must be before yesterday'

    delta = yesterday - start_date

    dates = []

    for i in range(delta.days + 1):
        dates.append(start_date + dt.timedelta(days=i))

client_id = os.environ['FITBIT_CLIENT_ID']
client_secret = os.environ['FITBIT_CLIENT_SECRET']

server = Oauth2.OAuth2Server(client_id, client_secret)
server.browser_authorize()

access_token = str(server.fitbit.client.session.token['access_token'])
refresh_token = str(server.fitbit.client.session.token['refresh_token'])

print(access_token)
print(refresh_token)

client = fitbit.Fitbit(client_id, client_secret, oauth2=True, 
                       access_token=access_token, refresh_token=refresh_token)

heading = ['date', 'steps', 'calories']
print('\t'.join(heading))

for date in dates:
    activity_summary = client.activities(date=date.strftime('%Y-%m-%d'))['summary']

    data = [
        date.strftime('%Y-%m-%d'),
        activity_summary['steps'] if 'steps' in activity_summary else '-',
        activity_summary['caloriesOut'] if 'caloriesOut' in activity_summary else '-'
    ]

    print('\t'.join(map(str, data)))
