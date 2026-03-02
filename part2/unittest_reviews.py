#!/usr/bin/env python3

from app.__init__ import create_app
from uuid import uuid4
import unittest


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': f'john.{uuid4()}@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.user = response.json

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user['id']
        })
        self.assertEqual(response.status_code, 201)
        self.place = response.json

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 4,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        })
        data = response.json

        self.assertEqual(response.status_code, 201)
        self.assertTrue(True if 'id' in data.keys() else False)
        self.assertEqual(data.get('text', None), 'Good rate')
        self.assertEqual(data.get('rating', None), 4)
        self.assertEqual(data.get('user_id', None), self.user['id'])
        self.assertEqual(data.get('place_id', None), self.place['id'])

    def test_create_with_bad_userid(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 4,
            'place_id': self.place['id'],
            'user_id': uuid4()
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Invalid input data')

    def test_create_with_bad_placeid(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 4,
            'place_id': uuid4(),
            'user_id': self.user['id']
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Invalid input data')

    def test_create_with_bad_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 6,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Invalid input data')

    def test_create_with_bad_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'ab',
            'rating': 4,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Invalid input data')

    def test_get_by_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 4,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        })
        review = response.json

        self.assertEqual(response.status_code, 201)

        response = self.client.get(f'/api/v1/reviews/{review["id"]}')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertTrue(True if 'id' in data.keys() else False)
        self.assertEqual(data.get('text', None), 'Good rate')
        self.assertEqual(data.get('rating', None), 4)
        self.assertEqual(data.get('place_id', None), review['place_id'])
        self.assertEqual(data.get('user_id', None), review['user_id'])

    def test_delete(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': f'Good rate',
            'rating': 4,
            'place_id': self.place['id'],
            'user_id': self.user['id']
        })
        review = response.json

        self.assertEqual(response.status_code, 201)

        response = self.client.delete(f'/api/v1/reviews/{review["id"]}')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('message', None), 'Review deleted')

    def test_delete_with_bad_id(self):
        response = self.client.delete(f'/api/v1/reviews/{uuid4()}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
