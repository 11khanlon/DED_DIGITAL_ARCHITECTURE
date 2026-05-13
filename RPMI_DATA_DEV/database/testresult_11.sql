-- =========================================================
-- TEST RESULT MODULE
-- =========================================================

CREATE TABLE TestResult (
    result_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TIC(tic_id),

    measurement_type VARCHAR(255),

    value FLOAT,

    unit VARCHAR(100),

    spatial_coordinate VARCHAR(255),

    defect_label VARCHAR(255)
);


