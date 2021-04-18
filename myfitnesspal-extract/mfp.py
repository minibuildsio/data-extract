import myfitnesspal
import os
import datetime as dt

import argparse


parser = argparse.ArgumentParser(description='Extract data from My Fitness Pal.')
parser.add_argument(
    "start_date", help="The date to start the extract from (yyyy-mm-dd)", nargs='?')

args = parser.parse_args()

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

client = myfitnesspal.Client(os.environ['MYFITNESSPAL_USER'], os.environ['MYFITNESSPAL_PASSWORD'])

heading = ['date', 'calories', 'carbs', 'fat', 'protein', 'sugar']
print('\t'.join(heading))

# extract nutrition data for the requested dates
for date in dates:
    nutrition = client.get_date(date.year, date.month, date.day)

    data = [
        date.strftime('%Y-%m-%d'),
        nutrition.totals['calories'] if 'calories' in nutrition.totals else '-',
        nutrition.totals['carbohydrates'] if 'carbohydrates' in nutrition.totals else '-',
        nutrition.totals['fat'] if 'fat' in nutrition.totals else '-',
        nutrition.totals['protein'] if 'protein' in nutrition.totals else '-',
        nutrition.totals['sugar'] if 'sugar' in nutrition.totals else '-'
    ]

    print('\t'.join(map(str, data)))
