"""Entry point for Flask application."""
from api.app import create_app
from api.config import DevelopmentConfig


APP = create_app()
