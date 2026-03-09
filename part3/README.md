# HBNB part2

## Decription
***The aim of this part is to implement the business logic and the presentation logic***

## Business logic layer

1. **the architcture**
![alt text](<../part1/Diagramme de class.drawio.png>)

2. **pattern façade**
    **a little description of the use of the pattern façade**

It is used to be inherited by the other class models, and it implement general functionnalities to all the class

    - HBNBFacade
        - Attributes
            - id
            - created_at
            - updated_at
        - Methods
            - save()
            - update(data)

3. **models**
    - User
    - Place
    - Review
    - Amenity


## Presentation layer

1. **endpoints**
    - Users
        - POST /api/v1/users
        - Get /api/v1/users/{user_id}
    - Places
        - POST /api/v1/places
        - GET /api/v1/places
        - GET /api/v1/places/{place_id}
        - PUT /api/v1/places/{place_id}
    - Reviews
        - POST /api/v1/reviews
        - GET /api/v1/reviews
        - GET /api/v1/reviews/{review_id}
        - PUT /api/v1/reviews/{review_id}
        - DELETE /api/v1/reviews/{review_id}
    - Amenitys
        - POST /api/v1/amenities
        - GET /api/v1/amenities
        - GET /api/v1/amenities/{amenity_id}
        - PUT /api/v1/amenities/{amenity_id}


## Doc swagger

```http://127.0.0.1:5000/api/v1```

## Edge case for the attribute of a class and there instance

- **User:**
  - Ensure that the `first_name`, `last_name`, and `email` attributes are not empty.
  - Ensure that the length of `first_name` and `last_name` is in [3, 50]
  - Ensure that the `email` is in a valid email format.

- **Place:**
  - The `description` should be less than 500 character
  - Ensure that `title` is not empty and is between 3 and 50 char.
  - Ensure that `price` is a positive number.
  - Ensure that `latitude` is between -90 and 90.
  - Ensure that `longitude` is between -180 and 180.
  - Ensure that `user_id` and `amenities_id` are valid entities.

- **Review:**
  - Ensure that `text` is not empty.
  - Ensure that `user_id` and `place_id` reference valid entities.

- **Amenity**
  - Ensure that `name` is not empty and is between 3 and 50 char

## Dependencies

1. **requirements.txt**

use the command : ```pip install -r requirments.txt```

2. **list of dependencies**
    - aniso8601==10.0.1
    - attrs==25.4.0
    - blinker==1.9.0
    - click==8.1.8
    - Flask==3.1.3
    - flask-restx==1.3.2
    - importlib_metadata==8.7.1
    - importlib_resources==6.5.2
    - itsdangerous==2.2.0
    - Jinja2==3.1.6
    - jsonschema==4.25.1
    - jsonschema-specifications==2025.9.1
    - MarkupSafe==3.0.3
    - referencing==0.36.2
    - rpds-py==0.27.1
    - typing_extensions==4.15.0
    - Werkzeug==3.1.6
    - zipp==3.23.0

## Test API (with curl)

### Create user
```
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

### Create amenity
```
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-fi"}'
```

### Create place
```
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": "[REPLACE OWNER_ID]"}'
```

### Create review
```
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great place to stay!", "rating": 5, "user_id": "[REPLACE USER_ID]", "place_id": "[REPLACE PLACE_ID]"}'
```
#### You can also test it on an API tester such as Postman


## Authors

Contributors names and contact info

**Name : email**
- Elliot CHARLET : _charlet.elliot@gmail.com_
- Ilan DEVERSENNE : _ilan.deversenne@holbertonstudents.com_
- Robin BOUVIER : _12229@holbertonstudents.com_

## License

This project is licensed under the [ELLIOT CHARLET and ILAN DEVERSENNE and ROBIN BOUVIER] License