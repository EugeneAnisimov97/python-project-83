CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE url_checks  (
    id SERIAL PRIMARY KEY,
    url_id bigint  REFERENCES urls (id),
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description text,
    created_at TIMESTAMP
);