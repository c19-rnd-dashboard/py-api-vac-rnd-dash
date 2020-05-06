from api.utils.ingest import run_ingest
from api.db import init_db
from data import factory_countries, factory_milestones
from flask import render_template, Blueprint, request, jsonify, current_app
from markdown2 import Markdown
import os

from api.mq import get_q

import logging

routelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

admin_routes = Blueprint("admin_routes", __name__)


### Helper Functions ###


def render_markdown(filename):
    # Convert markdown file to HTML for rendering
    with open(filename, "rb") as f:
        html = Markdown().convert(f.read())

    return html


def get_local_filepath(relative_filepath):
    return os.path.join(os.getcwd(), relative_filepath)


### Routes ###


@admin_routes.route("/ingest", methods=["POST"])
def get_ingest():
    if request.method == "POST":
        try:
            ingest_request = request.json
            routelogger.info(
                f"POST received at Ingest.  Running Ingest{ingest_request}"
            )
            q = get_q()
            # Check for kwargs
            if 'kwargs' in ingest_request:
                kwargs = ingest_request['kwargs']
                routelogger.info(f'KWARGS received {kwargs}')
            else:
                kwargs = {}
            job = q.enqueue_call(
                func=run_ingest,
                args=(
                    ingest_request["source"],
                    ingest_request["category"]),
                kwargs=kwargs,
                timeout=1800,
            )
            # print(ingest_request)
            message = {
                "message": 'Job sent to queue.',
                'job_id': job.get_id(),
            }

        except Exception as ex:
            message = {"success": False, "message": f"Error occured {ex}"}
    return message


@admin_routes.route("/", methods=["GET"])
def render_home():
    if request.method == "GET":
        local_file_path = get_local_filepath("docs/endpoints.md")
        if local_file_path:
            return render_markdown(local_file_path)
        else:
            return "Could not load readme.  Welcome to the API."


def check_password(password):
    import hashlib
    m = hashlib.sha256()
    m.update(
        bytes(password, 'utf-8')
    )
    return m.hexdigest() == '2898a07b2cf23dda8530b14b6aa522e67b002886d170c02219acc3598fdb50f3'


def run_database_update():
    # Create a temporary application
    # Init the database
    init_db(context=False)
    # # Load factory tables
    # # Run known ingest
    jobs = [
        ('milestone',
         factory_milestones,
         {}
         ),
        ('country',
         factory_countries,
         {}
         ),
        ('product',
         'https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile2.csv',
         {'loader': "unfiltered_csv"}
         ),
        ('trial',
         'https://raw.githubusercontent.com/ebmdatalab/covid_trials_tracker-covid/master/notebooks/processed_data_sets/trial_list_2020-04-07.csv',
         {}
         ),
    ]
    for job in jobs:
        run_ingest(category=job[0], source=job[1], **job[2])


@admin_routes.route('/admin/update', methods=['POST'])
def update_db():
    if request.method == 'POST':
        json_data = request.json
        routelogger.info('Update DB Request Received.  Verifying.')
        if check_password(json_data['password']):
            routelogger.info('Verified. Updating Database.')
            q = get_q()
            job = q.enqueue_call(
                func=run_database_update, args=(), result_ttl=5000, timeout=1800,
            )
            return {
                'message': 'Database Update Started.',
                'job_id': job.get_id(),
            }
        else:
            return "Verification Failed.  Database not updated."


@admin_routes.route('/test', methods=['GET'])
def test_func():
    run_ingest(category='product', source='https://raw.githubusercontent.com/c19-rnd-dashboard/py-api-vac-rnd-dash/master/data/vaccines/vaccineworkfile2.csv', **{})
    return 'Test Success!!'


@admin_routes.route('/test/redis', methods=['GET', 'POST'])
def test_redis():
    if request.method == 'GET':
        routelogger.info('Getting redis connection.')
        q = get_q()
        job = q.enqueue_call(
            func=test_func, args=(), result_ttl=5000
        )
        routelogger.info(f'Job Created at {job.get_id()}')

    return 'Complete!'
