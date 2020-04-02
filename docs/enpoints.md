## Testing Endpoints

### Ingest

```python
import requests

# Products - test_raw
requests.post('https://c19-vac-rnd-dash-staging-api.herokuapp.com/ingest', json={'category':'product', 'source':'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile1_clean.csv'})

# Categories - test_raw
response = requests.post('https://c19-vac-rnd-dash-staging-api.herokuapp.com/ingest', json={'category':'trial', 'source':'https://raw.githubusercontent.com/ebmdatalab/covid_trials_tracker-covid/master/notebooks/processed_data_sets/trial_list_2020-03-25.csv'})

```