from flask import render_template, Blueprint, request, jsonify
from api.models import *
from api.db import get_session
from api.utils.serializer import DictionarySerializer
from sqlalchemy import or_, and_
import logging


routelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

covid_dash = Blueprint("covid_dash", __name__)

ccase_serializer = DictionarySerializer(transformer='camelcase_keys')

@covid_dash.route("/alternatives")
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
def assets():
    routelogger.info("Running Products Query")
    with get_session() as session:
        # Get assets
        assets = session.query(ProductRaw).all()
        # Serialize the assets 
        serialized_assets = [ccase_serializer.transform(item.json) for item in assets]
        # Bring in other data via joins and lookups
            # Sponsors #
        for asset in serialized_assets:
            asset_sponsors = [
                result.json \
                for result in \
                session.query(Sponsor).join(ProductSponsor).\
                    filter(ProductSponsor.product_id == asset['productId']).all()
            ]
            asset['sponsors'] = asset_sponsors
    return jsonify(serialized_assets)