import requests
from faker import Faker
from random import choice, randint

url = "http://localhost:5000/api/v1"

try:
    fake = Faker()
    req = requests.post(
        f"{url}/users",
        json={
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email()
            })
    if req.status_code == 201:
        user = req.json()
    else:
        print("Failed to create user")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

try:
    amenties = ['Wi-fi', 'Netflix', 'Parking', 'Piscine', 'Billard', 'Baby-Foot']
    req = requests.post(
        f"{url}/amenities",
        json={
            'name': choice(amenties)
        }
    )
    if req.status_code == 201:
        amenity = req.json()
    else:
        print("Failed to create amenity")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

try:
    req = requests.post(
        f"{url}/places",
        json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user['id'],
            "amenities": []
        }
    )
    if req.status_code == 201:
        place = req.json()
    else:
        print("Failed to create place")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

try:
    rate = randint(1, 5)

    word = 'good'
    if rate < 3:
        word = 'bad'
    if rate == 5:
        word = 'very good'

    req = requests.post(
        f"{url}/reviews",
        json={
            'text': f'This rental is {word}',
            'rating': rate,
            'place_id': place['id'],
            'user_id': user['id']
        }
    )
    if req.status_code == 201:
        review = req.json()
    else:
        print("Failed to create review")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

try:
    req = requests.put(
        f"{url}/places/{place['id']}",
        json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": [
                amenity['id']
            ],
            "owner_id": user['id']
        }
    )
    if req.status_code == 200:
        updated_place = req.json()
    else:
        print("Failed to update place")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

try:
    req = requests.get(
        f"{url}/places/{place['id']}"
    )

    if req.status_code == 200:
        fetch_place = req.json()
    else:
        print("Failed to fetch place")
        print(req.status_code, req.text)
except Exception as e:
    print(e)

print("--------- Create user ---------\n")
print(user)
print("\n--------- Create amenity ---------\n")
print(amenity)
print("\n--------- Create place ---------\n")
print(place)
print("\n--------- Create review ---------\n")
print(review)
print("\n--------- Update place ---------\n\n")
print(updated_place)
print("\n--------- Fetch place ---------\n")
print(fetch_place)
print("\n-------------------------------")
