
## My Fitness Pal Extract

The script `myfitnesspal-extract/mfp.py` reads nutrition data from My Fitness Pal.

### Use

```
python mfp.py [start_date]
```

`start_date` (format: 'yyyy-mm-dd') is optional if provided data from `start_date` up to yesterday will be extracted otherwise only data for yesterday will be extracted.

### Configuration

Environment variables must be set up which contain your My Fitness Pal username and password:

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