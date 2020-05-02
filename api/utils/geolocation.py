import googlemaps
from utils.geolocation_pure import Geolocation as Geo
import os

gmaps = googlemaps.Client(key=os.getenv('GMAPS_GEOCODING_API_KEY'))

Geolocation = Geo(gmaps.geocode)
