from api.utils.ingest import run_ingest

source = 'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile2.csv'
params = {'loader': "unfiltered_csv"}


def start_test():
    run_ingest(category='product', source=source, **params)


start_test()
