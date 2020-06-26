import unittest
import pandas as pd
from pandas._testing import assert_frame_equal
from api.utils.geolocation.geolocation_pure import Geolocation, _map_geocode_to_site_location
from api.utils.geolocation import generate_hash

raw_locations = "kaiser permanente washington health research institute - seattle - washington,emory children's center - decatur - georgia"

df_sitelocations = pd.DataFrame(
    {
        'ID': [1, 2],
        'Sites Locations': [raw_locations, raw_locations],
    },
    columns=['ID', 'Sites Locations']
)

gmap_location = [{'access_points': [],
                  'address_components': [{'long_name': '1730',
                                          'short_name': '1730',
                                          'types': ['street_number']},
                                         {'long_name': 'Minor Avenue',
                                          'short_name': 'Minor Ave',
                                          'types': ['route']},
                                         {'long_name': 'Downtown Seattle',
                                          'short_name': 'Downtown Seattle',
                                          'types': ['neighborhood', 'political']},
                                         {'long_name': 'Seattle',
                                          'short_name': 'Seattle',
                                          'types': ['locality', 'political']},
                                         {'long_name': 'King County',
                                          'short_name': 'King County',
                                          'types': ['administrative_area_level_2',
                                                    'political']},
                                         {'long_name': 'Washington',
                                          'short_name': 'WA',
                                          'types': ['administrative_area_level_1',
                                                    'political']},
                                         {'long_name': 'United States',
                                          'short_name': 'US',
                                          'types': ['country', 'political']},
                                         {'long_name': '98101',
                                          'short_name': '98101',
                                          'types': ['postal_code']},
                                         {'long_name': '1466',
                                          'short_name': '1466',
                                          'types': ['postal_code_suffix']}],
                  'formatted_address': '1730 Minor Ave, Seattle, WA 98101, USA',
                  'geometry': {'location': {'lat': 47.6169397, 'lng': -122.329572},
                               'location_type': 'ROOFTOP',
                               'viewport': {'northeast': {'lat': 47.61828868029149,
                                                          'lng': -122.3282230197085},
                                            'southwest': {'lat': 47.6155907197085,
                                                          'lng': -122.3309209802915}}},
                  'place_id': 'ChIJG4id-zQVkFQRZam9C1RdzhY',
                  'plus_code': {'compound_code': 'JM8C+Q5 Seattle, Washington, United States',
                                'global_code': '84VVJM8C+Q5'},
                  'types': ['establishment', 'point_of_interest']}]

secondlocation = [{'access_points': [],
                   'address_components': [{'long_name': '1405',
                                           'short_name': '1405',
                                           'types': ['street_number']},
                                          {'long_name': 'East Clifton Road Northeast',
                                           'short_name': 'E Clifton Rd NE',
                                           'types': ['route']},
                                          {'long_name': 'Atlanta',
                                           'short_name': 'Atlanta',
                                           'types': ['locality', 'political']},
                                          {'long_name': 'DeKalb County',
                                           'short_name': 'Dekalb County',
                                           'types': ['administrative_area_level_2',
                                                     'political']},
                                          {'long_name': 'Georgia',
                                           'short_name': 'GA',
                                           'types': ['administrative_area_level_1',
                                                     'political']},
                                          {'long_name': 'United States',
                                           'short_name': 'US',
                                           'types': ['country', 'political']},
                                          {'long_name': '30322',
                                           'short_name': '30322',
                                           'types': ['postal_code']}],
                   'formatted_address': '1405 E Clifton Rd NE, Atlanta, GA 30322, USA',
                   'geometry': {'location': {'lat': 33.7934917, 'lng': -84.3195325},
                                'location_type': 'ROOFTOP',
                                'viewport': {'northeast': {'lat': 33.79484068029149,
                                                           'lng': -84.31818351970848},
                                             'southwest': {'lat': 33.79214271970849,
                                                           'lng': -84.3208814802915}}},
                   'place_id': 'ChIJR4J4LPoG9YgRJLnI9mqd85c',
                   'plus_code': {'compound_code': 'QMVJ+95 Atlanta, Georgia, United States',
                                 'global_code': '865QQMVJ+95'},
                   'types': ['establishment', 'health', 'hospital', 'point_of_interest']}]


class LocationsTest(unittest.TestCase):

    expected = {
        'name': '1730 Minor Ave, Seattle, WA 98101, USA',
        'lat': 47.6169397,
        'lng': -122.329572,
        'country': 'US',
        'state': 'WA',
        'city': 'Seattle'
    }

    def test_map_geocode_to_site_location(self):
        result = _map_geocode_to_site_location(gmap_location)
        self.assertEqual(result, self.expected)

    def test_get_location(self):
        geolocation = Geolocation(lambda _: gmap_location)
        result = geolocation.get(
            "kaiser permanente washington health research institute - seattle - washington")

        self.assertEqual(result, self.expected)

    def test_geolocation_transform(self):
        expected_frame = pd.DataFrame({
            'site_location_id': [
                generate_hash(
                    "kaiser permanente washington health research institute - seattle - washington"+str(1)),
                generate_hash(
                    "emory children's center - decatur - georgia"+str(1)),
                generate_hash(
                    "kaiser permanente washington health research institute - seattle - washington"+str(2)),
                generate_hash(
                    "emory children's center - decatur - georgia"+str(2)),
            ],
            'product_id': [
                1,
                1,
                2,
                2
            ],
            'name': [
                '1730 Minor Ave, Seattle, WA 98101, USA',
                '1730 Minor Ave, Seattle, WA 98101, USA',
                '1730 Minor Ave, Seattle, WA 98101, USA',
                '1730 Minor Ave, Seattle, WA 98101, USA'
            ],
            'city': [
                'Seattle',
                'Seattle',
                'Seattle',
                'Seattle',
            ],
            'state': [
                'WA',
                'WA',
                'WA',
                'WA',
            ],
            'country': ['US', 'US', 'US', 'US'],
            'lat': [47.6169397, 47.6169397, 47.6169397, 47.6169397, ],
            'lng': [-122.329572, -122.329572, -122.329572, -122.329572, ],

        }, columns=['site_location_id', 'product_id',  'name', 'city', 'state', 'country', 'lat', 'lng'])
        geolocation = Geolocation(lambda _: gmap_location)
        resulting_frame = geolocation.transform(df_sitelocations)
        assert_frame_equal(expected_frame, resulting_frame)


if __name__ == "__main__":
    unittest.main()
