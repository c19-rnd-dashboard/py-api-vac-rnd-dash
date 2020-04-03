from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session

covid_dash = Blueprint("covid_dash", __name__)


@covid_dash.route('/traditional-med')
def traditional_med():
    with get_session() as session:
        meds = session.query(TrialRaw).filter(TrialRaw.intervention_type=='traditional medicine (drug)').all()
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/treatments')
def treatments():
    with get_session() as session:
        meds = session.query(TrialRaw).filter(TrialRaw.intervention_type != 'traditional medicine (drug)' and TrialRaw.intervention_type != 'diagnosis').all()
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/products')
def products():
    with get_session() as session:
        prods = session.query(ProductRaw).all()
    return jsonify([prod.to_json() for prod in prods])