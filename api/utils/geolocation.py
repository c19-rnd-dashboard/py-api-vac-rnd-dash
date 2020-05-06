import googlemaps
from utils.geolocation_pure import Geolocation as Geo
<<<<<<< HEAD
=======
from utils.tools import retry
>>>>>>> 0be3f42300e5dcb18e5aa28deeca61865c41f7a0
import os

gmaps = googlemaps.Client(key=os.getenv('GMAPS_GEOCODING_API_KEY'))

<<<<<<< HEAD
Geolocation = Geo(gmaps.geocode)
=======
Geolocation = Geo(retry(gmaps.geocode))
>>>>>>> 0be3f42300e5dcb18e5aa28deeca61865c41f7a0
