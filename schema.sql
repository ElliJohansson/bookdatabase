CREATE TABLE books (

    id SERIAL PRIMARY KEY,
    name TEXT,
    year INT,
    author TEXT,
    synopsis TEXT

);

CREATE TABLE users (

    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);