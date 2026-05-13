CREATE TABLE Parameter (

    parameter_id VARCHAR(100) PRIMARY KEY,

    parameter_name VARCHAR(255),

    parameter_type VARCHAR(255),

    unit VARCHAR(100),

    physical_meaning TEXT,

    data_type VARCHAR(100)
);


-- =========================================================
-- PARAMETER MODULE
-- =========================================================

CREATE TABLE BuildParameter (
    id SERIAL PRIMARY KEY,

    build_id VARCHAR(100)
        REFERENCES Build(build_id),

    parameter_id VARCHAR(100)
        REFERENCES Parameter(parameter_id),

    value_text TEXT,
    value_numeric DOUBLE PRECISION,
    unit VARCHAR(100),
    source VARCHAR(100),
    UNIQUE(build_id, parameter_id, source)
);