-- =========================================================
-- TIC INSPECTION MODULE
-- =========================================================

CREATE TABLE TICInspection (
    tic_id VARCHAR(100) PRIMARY KEY,

    part_id VARCHAR(100) REFERENCES Part(part_id),

    method VARCHAR(255),

    inspection_date TIMESTAMP,

    operator VARCHAR(255),

    region VARCHAR(255)
);


-- =========================================================
-- TIC EVENT MODULE
-- =========================================================

CREATE TABLE TICEvent (
    event_id VARCHAR(100) PRIMARY KEY,

    build_id VARCHAR(100)
    REFERENCES Build(build_id),

    system_id VARCHAR(100)
    REFERENCES System(system_id),

    parameter_id VARCHAR(100)
    REFERENCES Parameter(parameter_id),

    tic_id VARCHAR(100)
    REFERENCES TICInspection(tic_id),

    timestamp_utc TIMESTAMP,

    x_coord FLOAT,
    y_coord FLOAT,
    z_coord FLOAT,

    layer_number INT,

    value_numeric FLOAT,

    value_text TEXT,

    quality_flag VARCHAR(100),

    state_scope VARCHAR(255)
);



