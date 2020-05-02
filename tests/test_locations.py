import unittest
from utils.geolocation_pure import Geolocation, _map_geocode_to_site_location

raw_locations = "kaiser permanente washington health research institute - seattle - washington,emory children's center - decatur - georgia"

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
        geolocation = Geolocation(lambda _: gmap_location)
        result = geolocation.transform(
            {'site_locations': raw_locations})
        self.assertEqual(result['site_locations'][0], self.expected)


if __name__ == "__main__":
    unittest.main()
