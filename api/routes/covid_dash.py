from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session
from api.utils.serializer import DictionarySerializer
from api.cache import cache
from sqlalchemy import or_, and_
import logging


routelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

covid_dash = Blueprint("covid_dash", __name__)

ccase_serializer = DictionarySerializer(transformer='camelcase_keys')

@covid_dash.route("/alternatives")
@cache.cached(timeout=6000)
def alternatives():
    routelogger.info("Running Alternatives Query")
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(
                and_(
                    ~TrialRaw.intervention_type.like("%traditional%"),
                    ~TrialRaw.intervention_type.like("%drug%"),
                    ~TrialRaw.intervention.like("%vaccine%"),
                )
            )
            .all()
        )
    return jsonify([med.to_json() for med in meds])


@covid_dash.route("/treatments")
@cache.cached(timeout=6000)
def treatments():
    routelogger.info("Running Treatments Query")
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(
                or_(
                    TrialRaw.intervention_type.like("%traditional%"),
                    TrialRaw.intervention_type.like("%drug%"),
                )
            )
            .all()
        )
    return jsonify([med.to_json() for med in meds])


@covid_dash.route("/vaccines")
@cache.cached(timeout=6000)
def products():
    routelogger.info("Running Vaccines Query")
    with get_session() as session:
        meds = (
            session.query(TrialRaw)
            .filter(TrialRaw.intervention.like("%vaccine%"))
            .all()
        )
    return jsonify([med.to_json() for med in meds])


@covid_dash.route("/assets")
@cache.cached(timeout=6000)
def assets():
    routelogger.info("Running Products Query")
    with get_session() as session:
        assets = session.query(ProductRaw).all()
    return jsonify([ccase_serializer.transform(item.json) for item in assets])