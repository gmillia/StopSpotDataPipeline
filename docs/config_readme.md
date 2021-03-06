## Config Usage (in Python)

### Config JSON file

Can set config data in a JSON file that is passed to the config.load() as the first parameter.

Any arbitrary variables can be set at the top level of the object. There is also a "columns" attribute that contains a column name, and a "max" and "min" that can be an integer, date, float, or "NA" if it is not bounded in that direction.

Upon deployment, it is necessary to hardcode the password for the pipeline's
email into this file. Additionally, `user_emails` may be a list of emails, or
a singular email string.

### Load config

This method returns a boolean to reflect the success of the JSON parse.

``` py
from config import config
from config import BoundsResult

config.load('path_to_config.json')
```

### Set value

``` py
try:
    user = os.environ["PIPELINE_USER"]
    config.set_value('user', user)
except KeyError as err:
    print("Could not read environment data.")
```

### Get value

``` py
receiver_email = config.get_value('user_emails')
```

### Column bounds checking

``` py
result = config.check_bounds('id', 22)

if result == BoundsResult.VALID:
    print("it's valid!")
elif result == BoundsResult.MIN_ERROR:
    print("it's too low!")
elif result == BoundsResult.MAX_ERROR:
    print("it's too high!")

#also works for dates
result = config.check_bounds('service_date', '1990/01/01')
```
