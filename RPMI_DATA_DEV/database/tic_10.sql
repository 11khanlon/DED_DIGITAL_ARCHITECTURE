-- =========================================================
-- TIC INSPECTION MODULE
-- =========================================================

CREATE TABLE TIC (
    tic_id VARCHAR(100) PRIMARY KEY,

    tic_name VARCHAR(255),
    tic_type VARCHAR(255),
    tic_standard VARCHAR(255),

    procedure_doc_uri TEXT,

    preparation_conditions TEXT,

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    location TEXT,

    notes TEXT,

    operator_person_id VARCHAR(100),  -- REFERENCES Person(person_id)
    point_of_contact_person_id VARCHAR(100), -- REFERENCES Person(person_id)

    vendor_org_id VARCHAR(100), -- REFERENCES Organization(organization_id)

    equipment_id VARCHAR(100),  -- non-AM equipment reference
    software_id VARCHAR(100),

    is_destructive BOOLEAN,

    pass_fail VARCHAR(50),

    test_duration INTERVAL,

    temperature_c FLOAT,
    temperature_control_method TEXT,
    temperature_measurement_location TEXT,

    humidity_percent FLOAT,

    ancillary_feedstock_id VARCHAR(100) -- REFERENCES Material/material_id or GasStock
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
    specimen_description TEXT,

    extraction_method TEXT,
    sampling_location TEXT,

    deviation_notes TEXT,

    orientation_x FLOAT,
    orientation_y FLOAT,
    orientation_z FLOAT,

    test_location TEXT,

    post_process_info TEXT,

    post_process_process_id VARCHAR(100) -- REFERENCES Process(process_id)
);


CREATE TABLE TICIndication (
    indication_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TIC(tic_id),

    pass_fail_flag VARCHAR(50),  -- Pass / Fail / Informational

    indication_type TEXT,

    size_micrometer FLOAT,

    location_x FLOAT,
    location_y FLOAT,
    location_z FLOAT,

    report_uri TEXT,

    notes TEXT
);


