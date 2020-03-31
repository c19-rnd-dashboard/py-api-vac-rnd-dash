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

## Mock Routes


Route: `/mock1`
Method: `GET`
Result:
```
[
  {
    "discovery": [
      {
        "x": "Vax 1", 
        "y": 0.3950416378989944
      }, 
      {
        "x": "Vax 2", 
        "y": 0.06409737261658588
      }, 
      {
        "x": "Vax 3", 
        "y": 0.19727813356604684
      }
    ]
  }, 
 ...
]
```



Route: `/mock2`
Method: `GET`
Result:
```
[
  {
    "milestones": [
      {
        "dates": [
          {
            "end": "05/09/20", 
            "label": "Actual Progress", 
            "name": "actual", 
            "start": "03/28/20"
          }, 
          {
            "end": "05/30/20", 
            "label": "Best Case", 
            "name": "best", 
            "start": "03/28/20"
          }, 
          {
            "end": "05/09/20", 
            "label": "Worst Case", 
            "name": "worst", 
            "start": "03/28/20"
          }
        ], 
        "label": "Discovery", 
        "name": "discovery"
      }, 
      {
        "dates": [
          {
            "end": "06/13/20", 
            "label": "Actual Progress", 
            "name": "actual", 
            "start": "03/28/20"
          }, 
          {
            "end": "05/30/20", 
            "label": "Best Case", 
            "name": "best", 
            "start": "03/28/20"
          }, 
          {
            "end": "06/13/20", 
            "label": "Worst Case", 
            "name": "worst", 
            "start": "03/28/20"
          }
        ], 
        "name": "clinicalBatch"
      }
    ], 
    "name": "Vax 1"
  }
]
```

## Tests


Run unittests from application root folder (.../py-api-vac-rnd-dash/) with:

```bash
(Requirement Local) >> mkdir .../py-api-vac-rnd-dash/api/instance/logs
(Requirement Local) >> touch .../py-api-vac-rnd-dash/api/instance/logs/debg.log
>> python -m unittests discover
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU v3](https://choosealicense.com/licenses/gpl-3.0/)
