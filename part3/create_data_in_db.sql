CREATE TABLE IF NOT EXISTS users (
    id CHAR(36),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36),
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    PRIMARY KEY(id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS review (
    id CHAR(36),
    text TEXT,
    rating INT(1, 5),
    user_id CHAR(36),
    place_id CHAR(36),
    PRIMARY KEY(id),
    CONSTRAINT there_s_place_and_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    FOREIGN KEY (place_id) REFERENCES places(id)
);

CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36),
    name VARCHAR(255) UNIQUE
);

INSERT INTO users (
    `id`,
    `email`,
    `first_name`,
    `last_name`,
    `password`,
    `is_admin`,
    `created_at`,
    `updated_at`
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.com',
    'Admin',
    'HBnB',
    '$2a$12$iIY0XSc0TztcyhkfttsGtO/gUTorunCzu/YE8CpwxwD2wvHimahZ6',
    TRUE,
    '2026-04-12 20:55:29.192164',
    '2026-04-12 20:55:29.192164'
);

INSERT INTO amenities (
    id,
    name
)
VALUES (
    '95a2224b-4b5c-40b3-a727-f32d309575fd',
    'Wifi'
);

INSERT INTO amenities (
    id,
    name
)
VALUES (
    '90db30b4-08b0-43bc-8cc8-c8148924653f',
    'Swimming Pool'
);

INSERT INTO amenities (
    id,
    name
)
VALUES (
    '462cf7f9-c53e-4bf6-bf96-3c990a5c78a4',
    'Air Conditioning'
);