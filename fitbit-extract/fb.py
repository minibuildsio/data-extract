import fitbit
import gather_keys_oauth2 as Oauth2
import datetime as dt
import os

import argparse


parser = argparse.ArgumentParser(description='Extract data from FitBit.')
parser.add_argument(
    "start_date", help="The date to start the extract from (yyyy-mm-dd)", nargs='?')

args = parser.parse_args()

# create a list of dates from start date to yesterday (default to [yesterday] if no start date provided)
yesterday = dt.datetime.today() - dt.timedelta(days=1)

if args.start_date is None:
    dates = list(reversed(list(map(lambda x: yesterday - dt.timedelta(days=x), range(7)))))
else:
    start_date = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
    if start_date > yesterday:
        raise Exception('Start date must be before yesterday')

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

print()

heading = ['date', 'calories', 'carbs', 'fat', 'protein', 'fiber']
print('\t'.join(heading))

for date in dates:
    food_log = client.foods_log(date=date.strftime('%Y-%m-%d'))['summary']

    food_data = [
        date.strftime('%Y-%m-%d'),
        food_log['calories'] if 'calories' in food_log else '-',
        food_log['carbs'] if 'carbs' in food_log else '-',
        food_log['fat'] if 'fat' in food_log else '-',
        food_log['protein'] if 'protein' in food_log else '-',
        food_log['fiber'] if 'fiber' in food_log else '-',
    ]

    print('\t'.join(map(str, food_data)))

print()

heading = ['date', 'total_asleep', 'total_in_bed', 'deep', 'light', 'rem', 'wake']
print('\t'.join(heading))

for date in dates:
    sleep_log = client.sleep(date=date.strftime('%Y-%m-%d'))['summary']

    sleep_data = [
        date.strftime('%Y-%m-%d'),
        sleep_log['totalMinutesAsleep'],
        sleep_log['totalTimeInBed'],
        sleep_log['stages']['deep'],
        sleep_log['stages']['light'],
        sleep_log['stages']['rem'],
        sleep_log['stages']['wake'],
    ]

    print('\t'.join(map(str, sleep_data)))
