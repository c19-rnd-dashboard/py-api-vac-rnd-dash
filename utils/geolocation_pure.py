from .tools import find, compose


def _get_short_name(x): return x.get('short_name')


def _getAddressComponent(component): return compose(
    _get_short_name,
    find(lambda x: component in x['types'])
)


def _map_geocode_to_site_location(gmaps_geocode):
    g_address = gmaps_geocode[0]
    address_types = ['locality', 'administrative_area_level_1', 'country', ]
    address_components = g_address["address_components"]
    city, state, country = (_getAddressComponent(address_type)(
        address_components) for address_type in address_types)
    return {
        "name": g_address["formatted_address"],
        "lat": g_address["geometry"]["location"]["lat"],
        "lng": g_address["geometry"]["location"]["lng"],
        "city": city,
        "state": state,
        "country": country,
    }


class Geolocation:
    def __init__(self, geocode):
        self.geocode = geocode

    def get(self, address):
        return _map_geocode_to_site_location(self.geocode(address))

    def transform(self, data):
        new_data = data.copy()
        addresses = new_data['site_locations'].split(",")
        new_data['site_locations'] = [
            self.get(address) for address in addresses]
        return new_data
