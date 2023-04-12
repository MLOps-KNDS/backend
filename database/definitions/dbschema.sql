-- IMPORTANT!!: When editing, compare this file with the db/dbdelete.sql file

-- ml model table
CREATE table model (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    model_type VARCHAR(255),
    model_path VARCHAR(255) NOT NULL,
    model_version VARCHAR(255),
    training_params VARCHAR(255) -- any additional parameters used during training, such as learning rate or batch size
);

-- AB test table
CREATE table ab_test (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    a_model_id INTEGER NOT NULL REFERENCES model(id),
    b_model_id INTEGER NOT NULL REFERENCES model(id)
);
