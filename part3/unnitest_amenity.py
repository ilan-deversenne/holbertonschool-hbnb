#!/usr/bin/env python3

from app.__init__ import create_app
import unittest

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

# --------------------
# GET api/v1/amenities
# --------------------

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        data = response.json

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data.get('name'), 'Wi-Fi')

# ---------------------
# POST api/v1/amenities
# ---------------------

    def test_get_amenities_list(self):
        self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        
        response = self.client.get('/api/v1/amenities/')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])

    def test_get_amenity_by_id(self):
        create_resp = self.client.post('/api/v1/amenities/', json={"name": "Spa"})
        amenity_id = create_resp.json['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('id'), amenity_id)
        self.assertEqual(data.get('name'), 'Spa')

# ---------------------------------
# GET api/v1/amenities/{amenity_id}
# ---------------------------------

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        data = response.json

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get('error'), 'Amenity not found')


if __name__ == '__main__':
    unittest.main()