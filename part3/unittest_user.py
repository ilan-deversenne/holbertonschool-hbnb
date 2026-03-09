#!/usr/bin/env python3

from app.__init__ import create_app
import unittest

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        data = response.json

        self.assertEqual(response.status_code, 201)
        self.assertTrue(True if 'id' in data.keys() else False)
        self.assertEqual(data.get('first_name', None), 'Jane')
        self.assertEqual(data.get('last_name', None), 'Doe')
        self.assertEqual(data.get('email', None), 'jane.doe@example.com')

    def test_email_arealy_exist(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Email already registered')

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get('error', None), 'Invalid input data')


if __name__ == '__main__':
    unittest.main()
