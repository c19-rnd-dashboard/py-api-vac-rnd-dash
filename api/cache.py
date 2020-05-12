"""
Cache Instance

Created separately from app factory to prevent circular imports in Blueprint
"""

from flask_caching import Cache

cache = Cache()