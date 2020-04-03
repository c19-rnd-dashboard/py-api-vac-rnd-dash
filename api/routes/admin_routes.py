from api.utils.ingest import run_ingest
#from api.utils.ingest import assign_transformations, assign_writer, transform_data, write_data, __init__
from flask import render_template, Blueprint, request, jsonify
from markdown2 import Markdown
import os

import logging

routelogger = logging.getLogger(__name__)

admin_routes = Blueprint("admin_routes", __name__)


### Helper Functions ###

def render_markdown(filename):
    # Convert markdown file to HTML for rendering
    with open(filename, 'rb') as f:
        html = Markdown().convert(f.read())

    return html

def get_local_filepath(relative_filepath):
    return os.path.join(os.getcwd(), relative_filepath)

### Routes ###

@admin_routes.route('/ingest', methods=['POST'])
def get_ingest():
    if request.method == 'POST':
        try:
            ingest_request = request.json
            routelogger.info(f'POST received at Ingest.  Running Ingest{ingest_request}')
            run_ingest(source=ingest_request['source'],
                       category=ingest_request['category'])
            # print(ingest_request)
            message = {"success": True, "message": f'Success!  Ingested {ingest_request}'}

        except Exception as ex:
            message = {"success": False, "message": f"Error occured {ex}"}
    return message


@admin_routes.route('/', methods=['GET'])
def render_home():
    if request.method == 'GET':
        local_file_path = get_local_filepath('README.md')
        if local_file_path:
            return render_markdown(local_file_path)
        else:
            return "Could not load readme.  Welcome to the API."
            