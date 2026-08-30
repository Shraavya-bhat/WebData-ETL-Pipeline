CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    openlibrary_key VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255),
    author VARCHAR(255),
    year INTEGER
);
