"""Main application and routing logic for Vaccine R&D Dash API."""
from decouple import config
from flask import Flask, json, jsonify, request
from api.routes.mock_routes import mock_routes
from flask_cors import CORS


def create_app():
    """
    Creates app
    """
    app = Flask(__name__)
    CORS(app)

    # Register routes
    app.register_blueprint(mock_routes)

    return app
