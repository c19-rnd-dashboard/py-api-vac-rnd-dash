from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session

import logging 

routelogger = logging.getLogger(__name__)

covid_dash = Blueprint("covid_dash", __name__)


@covid_dash.route('/traditional-med')
def traditional_med():
    routelogger.info('Running Traditional Medicine Query')
    with get_session() as session:
        meds = session.query(TrialRaw).filter(TrialRaw.intervention_type=='traditional medicine (drug)').all()
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/treatments')
def treatments():
    routelogger.info('Running Treatments Query')
    with get_session() as session:
        meds = session.query(TrialRaw).filter(TrialRaw.intervention_type != 'traditional medicine (drug)' and TrialRaw.intervention_type != 'diagnosis').all()
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/vaccines')
def products():
    routelogger.info('Running Vaccines Query')
    with get_session() as session:
        prods = session.query(ProductRaw).all()
    return jsonify([prod.to_json() for prod in prods])