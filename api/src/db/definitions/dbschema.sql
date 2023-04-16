-- IMPORTANT!!: When editing, compare this file with the db/dbdelete.sql file

CREATE SCHEMA core;

CREATE TYPE STATUS AS ENUM ('active', 'inactive');

CREATE TYPE ROLE AS ENUM ('owner', 'admin', 'reader', 'writer');

CREATE TABLE core.model (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by INT NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    updated_by INT NOT NULL,
    image_tag VARCHAR(255),
    source_path VARCHAR(255),
    status STATUS NOT NULL
);

CREATE TABLE core.test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by INT NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    updated_by INT NOT NULL
);

CREATE TABLE core.model_test (
    model_id INT NOT NULL,
    test_id INT NOT NULL,
    PRIMARY KEY (model_id, test_id),
    FOREIGN KEY (model_id) REFERENCES core.model(id),
    FOREIGN KEY (test_id) REFERENCES core.test(id)
);

CREATE TABLE core.pool (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by INT NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    updated_by INT NOT NULL
);

CREATE TABLE core.pool_model (
    pool_id INT NOT NULL,
    model_id INT NOT NULL,
    PRIMARY KEY (pool_id, model_id),
    FOREIGN KEY (pool_id) REFERENCES core.pool(id),
    FOREIGN KEY (model_id) REFERENCES core.model(id)
);

CREATE TABLE core.user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE core.model_user_role (
    model_id INT NOT NULL,
    user_id INT NOT NULL,
    role ROLE NOT NULL,
    PRIMARY KEY (model_id, user_id),
    FOREIGN KEY (model_id) REFERENCES core.model(id),
    FOREIGN KEY (user_id) REFERENCES core.user(id)
);

CREATE TABLE core.test_user_role (
    test_id INT NOT NULL,
    user_id INT NOT NULL,
    role ROLE NOT NULL,
    PRIMARY KEY (test_id, user_id),
    FOREIGN KEY (test_id) REFERENCES core.test(id),
    FOREIGN KEY (user_id) REFERENCES core.user(id)
);

CREATE TABLE core.pool_user_role (
    pool_id INT NOT NULL,
    user_id INT NOT NULL,
    role ROLE NOT NULL,
    PRIMARY KEY (pool_id, user_id),
    FOREIGN KEY (pool_id) REFERENCES core.pool(id),
    FOREIGN KEY (user_id) REFERENCES core.user(id)
);
