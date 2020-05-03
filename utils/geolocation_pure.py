from .tools import find, compose, assign_prop, flatten
import pandas as pd


data_frame_columns = [
    'product_id',
    'name',
    'city',
    'state',
    'country',
    'lat',
    'lng',
]


def _get_short_name(x): return x.get('short_name') if x else None


def _getAddressComponent(component): return compose(
    _get_short_name,
    find(lambda x: component in x['types'] if x else None)
)


def _map_geocode_to_site_location(gmaps_geocode):
    if len(gmaps_geocode) == 0:
        return None
    g_address = gmaps_geocode[0]  # TODO this can be emtpy
    address_types = ['locality', 'administrative_area_level_1', 'country', ]
    address_components = g_address["address_components"]
    city, state, country = (_getAddressComponent(address_type)(
        address_components) for address_type in address_types)  # can return null
    return {
        "name": g_address["formatted_address"],
        "lat": g_address["geometry"]["location"]["lat"],
        "lng": g_address["geometry"]["location"]["lng"],
        "city": city,
        "state": state,
        "country": country,
    }


def _map_record_to_locations(get_location):
    def actual_map(record):
        _, product_id, addresses_raw = record
        if addresses_raw != '':
            addresses = addresses_raw.split(",")
            site_locations = map(get_location, addresses)
            result = map(lambda x: assign_prop(
                'product_id', product_id, x), site_locations)
            return list(result)
    return actual_map


class Geolocation:
    def __init__(self, geocode):
        self.geocode = geocode

    def get(self, address):
        return _map_geocode_to_site_location(self.geocode(address))

    def transform(self, data: pd.DataFrame):
        records = list(data.to_records())
        site_locations = flatten(
            list(map(_map_record_to_locations(self.get), records)))
        buffer = {}
        for column in data_frame_columns:
            buffer[column] = []
        for location in site_locations:
            for column in data_frame_columns:
                buffer[column].append(location[column])

        return pd.DataFrame.from_dict(buffer)
