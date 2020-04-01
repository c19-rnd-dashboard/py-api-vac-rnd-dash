from flask import render_template, Blueprint, request, jsonify
from api.models import *

covid_dash = Blueprint("covid_dash", __name__)


@covid_dash.route('/traditional-med')
def traditional_med():
    meds = TrialRaw.query.filter_by(intervention_type='traditional').all()
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/treatments')
def treatments():
    meds = TrialRaw.query.filter(Trial.intervention_type != 'traditional' and Trial.intervention_type != 'diagnosis').all()
    return jsonify([med.to_json() for med in meds])