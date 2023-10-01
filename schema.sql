CREATE TABLE books (

    id SERIAL PRIMARY KEY,
    name TEXT,
    year INT,
    author TEXT,
    synopsis TEXT,
    cover TEXT

);

CREATE TABLE users (

    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    is_admin BOOLEAN

);

CREATE TABLE genres (

    id SERIAL PRIMARY KEY,
    name TEXT

);

CREATE TABLE book_genres (

    book_id INT REFERENCES books(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (book_id, genre_id)
    
);

INSERT INTO genres (name) VALUES
('Action & Adventure'),
('Art & Photography'),
('Biography/Autobiography'),
('Children´s Literature'),
('Cookbook'),
('Essay'),
('Fantasy'),
('Fiction'),
('Graphic Novel'),
('History'),
('Horror'),
('Humor'),
('Mystery'),
('Non-Fiction'),
('Philosophy'),
('Poetry'),
('Parenting'),
('Religion & Spirituality'),
('Romance'),
('Sci-Fi'),
('Self-Help'),
('Short Story'),
('Thriller'),
('Travel'),
('True Crime');