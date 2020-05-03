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



def condense_sponsors(sponsor_results):
    # Requires sponsors in the form (product_id, sponsor_id, sponsor_name)
    unique_ids = sorted(list(set(result[0] for result in sponsor_results)))
    sponsor_dict= {}
    [sponsor_dict.update({unique_id:[]}) for unique_id in unique_ids]
    for result in sponsor_results:
        prod_id = result[0]
        spon_id = result[1]
        spon_name = result[2]
        sponsor_info = {'sponsorId': spon_id, 'sponsorName': spon_name}
        sponsor_dict[prod_id] = sponsor_dict[prod_id] + [sponsor_info]
    return sponsor_dict

def fetch_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return []

@covid_dash.route("/assets")
@cache.cached(timeout=6000)
def assets():
    routelogger.info("Running Products Query")
    with get_session(context=True) as session:
        assets = session.query(ProductRaw).all()
        # Serialize the assets 
        serialized_assets = [ccase_serializer.transform(item.json) for item in assets]
        # Bring in other data via joins and lookups
        # Sponsors #
        sponsors_info = session.query(ProductSponsor.product_id, Sponsor.sponsor_id, Sponsor.sponsor_name).join(ProductSponsor).all()
        sponsors = condense_sponsors(sponsors_info)

        for asset in serialized_assets:
            asset_sponsors = fetch_value(sponsors, asset['productId'])
            asset['sponsors'] = asset_sponsors
            asset['sources'] = asset['sources'].split(',')
    return jsonify(serialized_assets)


    