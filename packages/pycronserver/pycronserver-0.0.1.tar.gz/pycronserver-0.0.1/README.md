# pycronserver - Cron server for python functions
[![Python package](https://github.com/pyscioffice/pycronserver/actions/workflows/unittest.yml/badge.svg?branch=main)](https://github.com/pyscioffice/pycronserver/actions/workflows/unittest.yml)
[![Coverage Status](https://coveralls.io/repos/github/pyscioffice/pycronserver/badge.svg?branch=main)](https://coveralls.io/github/pyscioffice/pycronserver?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Execute python functions using cron tab. Rather than entering them all in the crontab file, they are stored in an SQL
table and executed by the `pycronserver` in a for loop. 

## Installation
Install via pip:
```
pip install git+https://github.com/pyscioffice/pycronserver.git
```

## Python Interface
Use python interface
```
from pycronserver import get_local_pycronserver
psc = get_local_pycronserver(config_dir="~/.pycronserver")
```
In the configuration directory `~/.pycronserver` the configuration is stored in the `config.json` file: 
- `connection_str` - connection string to connect to the SQL database - by default `"sqlite:///~/.pycronserver/cron.db`
- `username` - username (optional) - by default `True` but for windows a specific username is required. 
- `user_id` - user ID (optional) - the database can be shared with multiple users. 

To store a new python function call in the `pycronserver` database use: 
```
psc.store(crontab, python_funct_path, input_dict)
```
- `crontab` follows the cron notation of Minutes, Hours, Day of month, Month, Day of week - for example `0 0 * * 0`
- `python_funct_path` the path to the python function to execute - for example `crontab.get_cronvalue`
- `input_dict` the dictionary which contains the keyword arguments for the function call. 

Finally write the required entries to `crontab` so it can trigger the execution of the `pycronserver`: 
```
psc.write_to_crontab()
```

## Command Line Interface
During the execution `crontab` calls `pycronserver` using the specified date pattern in the cron notation:
```
pycronserver '0 0 * * 0'
```
So the same call can be used to debug the execution of the `pycronserver`. 
