-- =========================================================
-- TIC INSPECTION MODULE
-- =========================================================

CREATE TABLE TIC (
    tic_id VARCHAR(100) PRIMARY KEY,
    tic_part VARCHAR(100) REFERENCES BUILTPART(built_part_id),

    tic_name VARCHAR(255),
    tic_type VARCHAR(255),

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    
    notes TEXT

    
);


CREATE TABLE TICSequence (
    sequence_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TIC(tic_id),

    sequence_index INT,

    next_tic_id VARCHAR(100) REFERENCES TIC(tic_id)
);


CREATE TABLE TICSpecimen (
    specimen_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TIC(tic_id),

    specimen_model_id VARCHAR(100),

    origin_part_id VARCHAR(100),   -- REFERENCES Part(part_id)
    origin_material_id VARCHAR(100), -- REFERENCES Material(material_id)
    origin_feedstock_id VARCHAR(100),

    specimen_type TEXT,
    specimen_description TEXT


    --post_process_process_id VARCHAR(100)  REFERENCES Process(process_id)
);


CREATE TABLE TICIndication (
    indication_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TIC(tic_id),

    ---pass_fail_flag VARCHAR(50) CHECK (pass_fail_flag IN ('PASS','FAIL','INFORMATIONAL')),
    indication_type TEXT,

    size_micrometer FLOAT,

    location_x FLOAT,
    location_y FLOAT,
    location_z FLOAT,

    report_uri TEXT,

    notes TEXT
);


