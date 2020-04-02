from api.utils.ingest import run_ingest
#from api.utils.ingest import assign_transformations, assign_writer, transform_data, write_data, __init__
from flask import render_template, Blueprint, request, jsonify

import logging

routelogger = logging.getLogger(__name__)

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route('/ingest', methods=['POST'])
def get_ingest():
    if request.method == 'POST':
        try:
            ingest_request = request.json
            routelogger.info(f'POST received at Ingest.  Running Ingest{ingest_request}')
            run_ingest(source=ingest_request['source'],
                       category=ingest_request['category'])
            message = {"success": True, "message": data}
        except Exception as ex:
            message = {"success": False, "message": f"Error occured {ex}"}
    return message
