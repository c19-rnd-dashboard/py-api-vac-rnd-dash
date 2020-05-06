import api
from api.db import init_db
from api.utils.ingest import run_ingest


init_db(context=False)

source = 'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile2.csv'
params = {'loader': "unfiltered_csv"}


run_ingest(category='product', source=source, **params)
