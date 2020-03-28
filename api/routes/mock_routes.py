from flask import render_template, Blueprint, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
from random import randint

mock_routes = Blueprint("mock_routes", __name__)


@mock_routes.route("/mock1")
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


@mock_routes.route("/mock2")
def get_graph_mock_data():
    begin = datetime.now()

    mockVaccinesData = [
        {
            "name": "Vax 1",
            "milestones": [
                {
                    "name": "discovery",
                    "label": "Discovery",
                    "dates": [
                        {
                            "name": "actual",
                            "label": "Actual Progress",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                        {
                            "name": "best",
                            "label": "Best Case",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                        {
                            "name": "worst",
                            "label": "Worst Case",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                    ],
                },
                {
                    "name": "clinicalBatch",
                    "dates": [
                        {
                            "name": "actual",
                            "label": "Actual Progress",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                        {
                            "name": "best",
                            "label": "Best Case",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                        {
                            "name": "worst",
                            "label": "Worst Case",
                            "start": begin.strftime("%x"),
                            "end": (begin + timedelta(weeks=randint(4, 12))).strftime(
                                "%x"
                            ),
                        },
                    ],
                },
            ],
        }
    ]
    return jsonify(mockVaccinesData)
