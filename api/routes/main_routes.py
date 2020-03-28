from flask import render_template, Blueprint, request, jsonify
import pandas as pd
import numpy as np

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def get_mock_data():
    data = [
        {
            "discovery": [
                {"x": "Vax 1", "y": np.random.rand()},
                {"x": "Vax 2", "y": np.random.rand()},
                {"x": "Vax 3", "y": np.random.rand()},
            ]
        },
        {
            "clinical_batch": [
                {"x": "Vax 1", "y": np.random.rand()},
                {"x": "Vax 2", "y": np.random.rand()},
                {"x": "Vax 3", "y": np.random.rand()},
            ]
        },
        {
            "phase1": [
                {"x": "Vax 1", "y": np.random.rand()},
                {"x": "Vax 2", "y": np.random.rand()},
                {"x": "Vax 3", "y": np.random.rand()},
            ]
        },
        {
            "phase2": [
                {"x": "Vax 1", "y": np.random.rand()},
                {"x": "Vax 2", "y": np.random.rand()},
                {"x": "Vax 3", "y": np.random.rand()},
            ]
        },
    ]
    return jsonify(data)
