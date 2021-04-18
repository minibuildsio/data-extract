# Data Extract Tools

This project contains scripts to extract data from:

- MyFitnessPal
- FitBit

The intended use of these scripts is to extract data to be copied into a spreadsheet such as a health and fitness dashboard.

## MyFitnessPal Extract

The script `myfitnesspal-extract/mfp.py` reads nutrition data from MyFitnessPal.

### Use

```
python mfp.py [start_date]
```

`start_date` (format: 'yyyy-mm-dd') is optional if provided data from `start_date` up to yesterday will be extracted otherwise only data for yesterday will be extracted.

### Configuration

Environment variables must be set up which contain your MyFitnessPal username and password:

```yaml
MYFITNESSPAL_USER
MYFITNESSPAL_PASSWORD
```

### Example

Running the example below will print all nutrition data from 2021-01-01 until yesterday.

```bash
python mfp.py 2021-01-01

# date    calories        carbs   fat     protein sugar
# 2021-01-01      2500.0  200.0   120.0   115.0   20.0 
# 2021-01-02      -       -       -       -       -
# 2021-01-03      2600.0  201.0   125.0   120.0   20.0 
# ...
```

## FitBit

The script `fitbit-extract/fb.py` reads step and calories data from FitBit.

### Use

```
python fb.py [start_date]
```

`start_date` (format: 'yyyy-mm-dd') is optional if provided data from `start_date` up to yesterday will be extracted otherwise only data for yesterday will be extracted.

### Configuration

Environment variables must be set up which contain FitBit client id and secret:

```yaml
FITBIT_CLIENT_ID
FITBIT_CLIENT_SECRET
```

Visit https://dev.fitbit.com/apps/new to create an app which will provide a client id and secret.

### Example

Running the example below will print all data from 2021-01-01 until yesterday.

```bash
python fb.py 2021-01-01

# date      steps      calories
# 2021-01-01      15000  2600
# 2021-01-02      12000  2400
# 2021-01-03      20600  2800
# ...
```