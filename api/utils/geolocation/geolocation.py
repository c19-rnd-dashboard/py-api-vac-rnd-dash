import googlemaps
from .geolocation_pure import Geolocation as Geo
from .tools import retry
import os

gmaps = googlemaps.Client(key=os.getenv('GMAPS_GEOCODING_API_KEY'))

Geolocation = Geo(retry(gmaps.geocode))
