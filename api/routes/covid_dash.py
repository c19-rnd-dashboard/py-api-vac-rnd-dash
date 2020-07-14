from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session
from api.utils.serializer import DictionarySerializer
from api.utils.transform import (
    fetch_value,
    get_product_sponsors, condense_sponsors,
    get_product_milestones, condense_milestones,
    get_product_locations, condense_locations,
    get_product_contacts, condense_contacts,
)
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
    with get_session(context=True) as session:
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
    with get_session(context=True) as session:
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
    with get_session(context=True) as session:
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
    with get_session(context=True) as session:
        assets = session.query(ProductRaw).all()

    # Serialize the assets
    serialized_assets = [ccase_serializer.transform(item.json) for item in assets]
    
    # Get related data
    sponsors = condense_sponsors(get_product_sponsors())
    milestones = condense_milestones(get_product_milestones())
    sitelocations = condense_locations(get_product_locations())
    contacts = condense_contacts(get_product_contacts())

    for asset in serialized_assets:
        asset['sponsors'] = fetch_value(sponsors, asset['productId'])
        asset['milestones'] = fetch_value(milestones, asset['productId'])
        asset['siteLocations'] = fetch_value(sitelocations, asset['productId'])
        asset['sources'] = asset['sources'].split(',')
        asset['countries'] = asset['countries'].split(',')
        asset['countryCodes'] = asset['countryCodes'].split(',')
        asset['contact'] = fetch_value(contacts, asset['productId'])

    return jsonify(serialized_assets)
