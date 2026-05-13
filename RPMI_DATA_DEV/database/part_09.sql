-- =========================================================
-- PART MODULE
-- =========================================================

CREATE TABLE Part (
    part_id VARCHAR(100) PRIMARY KEY,

    build_id VARCHAR(100) REFERENCES Build(build_id),

    part_name VARCHAR(255),

    serial_number VARCHAR(255),

    orientation VARCHAR(255),

    location_in_build VARCHAR(255)
);