# py-api-vac-rnd-dash

Flask based API for Vaccine R&amp;D Dashboard

## Endpoint

Production: https://c19-vac-rnd-dash-api.herokuapp.com/

Staging: https://c19-vac-rnd-dash-staging-api.herokuapp.com/


## Installation

### Requirements

See condaenv.yml or Pipfile for minimum installation requirements in your environment

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
## How to run it locally ?

1. Get Google Sheets API `credentials.json` from steps below and follow steps below
2. `conda` or `pip` `install pipenv`
3. `pipenv install` to install all dependencies
4. `pipenv shell` to activate python virtual environment
5. `python run.py` and navigate to the localhost endpoint
```

### Conda Environment Setup

> Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

> ```bash``` >> conda env create -f condaenv.yml

> Start environment with: ```bash``` >> conda activate condabe

## How to access Google Sheet data using the Python API and convert to Pandas dataframe ?

1. Enable [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)
   - Step 1. Enable the Google Sheets API, download the `credentials.json`
   - Step 2. Download the `credentials.json`


## Usage

### Run development server

From command line:

```bash
>> python run.py
```

From python shell:

```python
# Not Implemented
```

## Tests

Run unittests from application root folder (.../py-api-vac-rnd-dash/) with:

```bash
(Requirement Local) >> mkdir .../py-api-vac-rnd-dash/api/instance/logs
(Requirement Local) >> touch .../py-api-vac-rnd-dash/api/instance/logs/debg.log
>> python -m unittests discover
```


### Testing the Full Application locally
Requires: redis server
**May need three or more active terminals to run full server

1. Start redis
```bash
>> redis-server
```
2. Start worker
```bash
>> cd <RootDirectory>
>> python worker.py
```
3. Start Flask Application
```bash
>> cd <RootDirectory>
>> python run.py
```
4. Start a command terminal or postman/insomnia instance to send requests to the server at <Default: 127.0.0.1:5000/route>


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU v3](https://choosealicense.com/licenses/gpl-3.0/)
