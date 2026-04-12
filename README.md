# HBnB - Simple Airbnb Clone
HBnB is a simple Airbnb clone that I built during my training at Holberton School

## Test web app

### For the first time setup (part3)

## Python Requirements (part3)
This project uses the following Python dependencies:

```txt
aniso8601==10.0.1
attrs==25.4.0
bcrypt==5.0.0
blinker==1.9.0
certifi==2026.2.25
charset-normalizer==3.4.4
click==8.1.8
colorama==0.4.6
Faker==37.12.0
Flask==3.1.3
Flask-Bcrypt==1.0.1
flask-cors==6.0.2
Flask-JWT-Extended==4.7.1
flask-restx==1.3.2
Flask-SQLAlchemy==3.1.1
greenlet==3.2.5
idna==3.11
importlib_metadata==8.7.1
importlib_resources==6.5.2
itsdangerous==2.2.0
Jinja2==3.1.6
jsonschema==4.25.1
jsonschema-specifications==2025.9.1
MarkupSafe==3.0.3
PyJWT==2.12.1
referencing==0.36.2
requests==2.32.5
rpds-py==0.27.1
SQLAlchemy==2.0.48
typing_extensions==4.15.0
tzdata==2025.3
urllib3==2.6.3
Werkzeug==3.1.6
zipp==3.23.0
```

### Installation (part3)
To install all dependencies, run:

```bash
pip install -r requirements.txt
```

#### Create database
```bash
python3 create_db.py
```

#### Create default admin user and default amenities (part3)
```bash
sqlite3 instance/development.db < create_data_in_db.sql
```

#### Run api (part3)
```bash
python3 run.py
```

# Default user credentials
```
Email: admin@hbnb.com
Password: admin1234
```

## Credits
I made Parts 1, 2, and 3 of this project in collaboration with [aragoza](https://github.com/aragoza).

---
**Some icons used in this project are from [flaticon.com](https://www.flaticon.com/).**
