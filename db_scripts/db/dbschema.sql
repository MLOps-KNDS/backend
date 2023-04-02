-- IMPORTANT!!: On edit, compare this file with the db/dbdelete.sql file

-- ml model table
CREATE table model (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) NOT NULL
);
