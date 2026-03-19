CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) DEFAULT UUID,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id)
)

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) DEFAULT UUID,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36)
    PRIMARY KEY(id)
    FOREIGN KEY (owner_id) REFERENCES users(id)
)

CREATE TABLE IF NOT EXISTS review (
    id CHAR(36) DEFAULT UUID,
    text TEXT,
    rating INT(1, 5),
    user_id CHAR(36),
    place_id CHAR(36),
    PRIMARY KEY(id),
    CONSTRAINT there_s_place_and_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    FOREIGN KEY (place_id) REFERENCES places(id)
)

CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) DEFAULT UUID,
    name VARCHAR(255) UNIQUE
)

INSERT INTO users
VALUES (
    36c9050e-ddd3-4c3b-9731-9f487208bbc1,
    admin@hbnb.io,
    Admin,
    HBnB,
    $2a$12$iIY0XSc0TztcyhkfttsGtO/gUTorunCzu/YE8CpwxwD2wvHimahZ6,
    TRUE
)

INSERT INTO amenities (name)
VALUES (
    'Wifi'
)

INSERT INTO amenities (name)
VALUES (
    'Swimming Pool'
)

INSERT INTO amenities (name)
VALUES (
    'Air Conditioning'
)