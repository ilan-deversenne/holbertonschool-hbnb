#!/usr/bin/env python3

import unittest
from app.__init__ import create_app
from uuid import uuid4

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        response = self.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f'john.{uuid4()}@example.com'
        })
        self.user = response.json
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", self.user)
        self.user_id = self.user["id"]


# ------------------------------
# POST /api/v1/places/ — success
# ------------------------------
    def test_create_place_success(self):
        payload = {
            "title": "Lovely House",
            "description": "Cozy and clean",
            "price": 120.0,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertEqual(data.get("title"), "Lovely House")
        self.assertEqual(data.get("owner_id"), self.user_id)

# --------------------
# POST — Invalid title
# --------------------
    def test_create_place_invalid_title_less_than_3(self):
        payload = {
            "title": "A",
            "description": "Invalid title too short",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")
    
    def test_create_place_invalid_title_more_tahn_50(self):
        payload = {
            "title": "Hello, this is a very good place you should buy a night in this good place even if it has a long name it is really good trust me!!!!",
            "description": "Invalid title too long",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# --------------------------
# POST — Invalid description
# --------------------------

    def test_create_place_invalid_description(self):
        payload = {
            "title": "Invalid description / empty description",
            "description": None,
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("description"), "")

# -----------------------------
# POST — Invalid price alphabet
# -----------------------------

    def test_create_place_invalid_price_alphabet(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": "Invalid price",
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# -------------------------
# POST — Invalid price bool
# -------------------------

    def test_create_place_invalid_price_bool(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": True,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# -----------------------------
# POST — Invalid price negative
# -----------------------------

    def test_create_place_invalid_price_negative(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": -1,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# ------------------------
# POST — Invalid price NaN
# ------------------------

    def test_create_place_invalid_price_NaN(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": "NaN",
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# ------------------------------
# POST — Invalid price too much
# ------------------------------

    def test_create_place_invalid_price_more_than_billion(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": 1.0e12,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id,
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# ------------------------------
# Latitude Invalid Tests too low
# ------------------------------
    def test_create_place_latitude_too_low(self):
        payload = {
            "title": "Bad Latitude Low",
            "description": "Latitude < -90",
            "price": 100.0,
            "latitude": -91.0,
            "longitude": 0.0,
            "owner_id": self.user_id,
        }
        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# -------------------------------
# Latitude Invalid Tests too high
# -------------------------------

    def test_create_place_latitude_too_high(self):
        payload = {
            "title": "Bad Latitude High",
            "description": "Latitude > 90",
            "price": 100.0,
            "latitude": 91.0,
            "longitude": 0.0,
            "owner_id": self.user_id,
        }
        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# -------------------------------
# Longitude Invalid Tests too low
# -------------------------------
    def test_create_place_longitude_too_low(self):
        payload = {
            "title": "Bad Longitude Low",
            "description": "Longitude < -180",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": -181.0,
            "owner_id": self.user_id,
        }
        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# --------------------------------
# Longitude Invalid Tests too high
# --------------------------------

    def test_create_place_longitude_too_high(self):
        payload = {
            "title": "Bad Longitude High",
            "description": "Longitude > 180",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 181.0,
            "owner_id": self.user_id,
        }
        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# --------------------
# POST — Invalid owner
# --------------------
    def test_create_place_invalid_owner(self):
        payload = {
            "title": "Nice House",
            "description": "Valid description",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": "nonexistent-user",
        }

        response = self.client.post("/api/v1/places/", json=payload)
        data = response.json

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"), "Invalid input data")

# -------------------------------
# GET /api/v1/places/ — list
# -------------------------------
    def test_get_all_places(self):
        create_resp = self.client.post("/api/v1/places/", json={
            "title": "Test House",
            "description": "Description",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
        })

        self.assertEqual(create_resp.status_code, 201)

        response = self.client.get("/api/v1/places/")
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)

        titles = [place.get("title") for place in data]
        self.assertIn("Test House", titles)

# -------------------------------
# PUT /api/v1/places/<id> — update
# -------------------------------
    def test_update_place_success(self):
        # Create a place first
        response = self.client.post("/api/v1/places/", json={
            "title": "Old Title",
            "description": "Old Desc",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
        })
        place_id = response.json["id"]

        update_payload = {
            "title": "New Title",
            "description": "Updated Desc",
            "price": 200.0,
            "latitude": 15.0,
            "longitude": 25.0,
            "owner_id": self.user_id,
        }

        response = self.client.put("/api/v1/places/{}".format(place_id), json=update_payload)
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("message"), "Place updated successfully")

# ----------------------------------------------
# PUT /api/v1/places/<id> — invalid update title
# ----------------------------------------------

    def test_update_place_invalid_title(self):
        response = self.client.post("/api/v1/places/", json={
            "title": "Valid Title",
            "description": "Desc",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
        })
        place_id = response.json["id"]

        # Title too short
        payload_short = dict(response.json)
        payload_short.update({"title": "A"})
        resp_short = self.client.put("/api/v1/places/{}".format(place_id), json=payload_short)
        self.assertEqual(resp_short.status_code, 400)
        self.assertEqual(resp_short.json.get("error"), "Invalid input data")

        # Title too long (>100 chars)
        payload_long = dict(response.json)
        payload_long.update({"title": "X" * 101})
        resp_long = self.client.put("/api/v1/places/{}".format(place_id), json=payload_long)
        self.assertEqual(resp_long.status_code, 400)
        self.assertEqual(resp_long.json.get("error"), "Invalid input data")

    def test_update_place_invalid_coordinates(self):
        response = self.client.post("/api/v1/places/", json={
            "title": "Coord Test",
            "description": "Desc",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
        })
        place_id = response.json["id"]

        # Invalid latitude
        payload_lat = dict(response.json)
        payload_lat.update({"latitude": 100.0})
        resp_lat = self.client.put("/api/v1/places/{}".format(place_id), json=payload_lat)
        self.assertEqual(resp_lat.status_code, 400)
        self.assertEqual(resp_lat.json.get("error"), "Invalid input data")

        # Invalid longitude
        payload_lon = dict(response.json)
        payload_lon.update({"longitude": -200.0})
        resp_lon = self.client.put("/api/v1/places/{}".format(place_id), json=payload_lon)
        self.assertEqual(resp_lon.status_code, 400)
        self.assertEqual(resp_lon.json.get("error"), "Invalid input data")

# -----------------------
# GET /api/v1/places/<id>
# -----------------------

    def test_get_place_by_id(self):
        place = self.client.post("/api/v1/places/", json={
            "title": "Single Place",
            "description": "Description",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id
        }).json

        place_id = place["id"]

        data = self.client.get(f"/api/v1/places/{place_id}").json

        self.assertEqual(data["id"], place_id)
        self.assertEqual(data["title"], "Single Place")
        self.assertEqual(data["owner"]["id"], self.user_id)

if __name__ == "__main__":
    unittest.main()