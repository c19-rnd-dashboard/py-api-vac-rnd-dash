from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session

import logging 

routelogger = logging.getLogger(__name__)

covid_dash = Blueprint("covid_dash", __name__)


@covid_dash.route("/alternatives")
def alternatives():
    routelogger.info('Running Alternatives Query')
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(
                ~TrialRaw.intervention_type.like("%traditional%")
                and ~TrialRaw.intervention_type.like("%drug%")
                and ~TrialRaw.intervention.like("%vaccine%"))
            .all()
        )
    return jsonify([med.to_json() for med in meds])


@covid_dash.route("/treatments")
def treatments():
    routelogger.info('Running Treatments Query')
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(
                TrialRaw.intervention_type.like("%traditional%")
                or TrialRaw.intervention_type.like("%drug%")
            )
            .all()
        )
    return jsonify([med.to_json() for med in meds])


@covid_dash.route('/vaccines')
def products():
    routelogger.info('Running Vaccines Query')
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(TrialRaw.intervention.like("%vaccine%"))
            .all()
        )
    return jsonify([med.to_json() for med in meds])
