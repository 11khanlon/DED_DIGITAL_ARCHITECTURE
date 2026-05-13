-- =========================================================
-- MACHINE MODULE
-- =========================================================

CREATE TABLE AMSystem (
    am_system_id VARCHAR(100) PRIMARY KEY,
    am_system_name VARCHAR(255),
    am_system_facility VARCHAR(255),
    am_system_location TEXT, -- globalAddressFormat (ISO 19160)

    am_machine_name VARCHAR(255),
    am_machine_serial_number VARCHAR(255),
    am_machine_model_name VARCHAR(255),

    am_system_process_type VARCHAR(100), -- ENUM ASTM 52900

    am_machine_firmware_version VARCHAR(255),

    am_machine_acceptance_date DATE,

    am_system_last_cleanout_date DATE

    -- processable_raw_materials TEXT[], stringArray

    -- am_system_software TEXT[]  stringArray (software IDs + versions)
);


CREATE TABLE AMSystem_Organization (
    am_system_id VARCHAR(100),
    organization_id VARCHAR(100),
    relationship_type VARCHAR(50), -- Manufacturer / Sponsor / Facility Owner
    PRIMARY KEY (am_system_id, organization_id, relationship_type)
);

CREATE TABLE AMSystem_Performance (
    am_system_id VARCHAR(100) PRIMARY KEY,

    max_build_rate_cm3h DOUBLE PRECISION,
    min_layer_thickness_um DOUBLE PRECISION,
    max_layer_thickness_um DOUBLE PRECISION,
    total_build_volume_mm3 DOUBLE PRECISION
);

CREATE TABLE InSituMonitoringSystem (
    in_situ_system_id VARCHAR(100) PRIMARY KEY,
    model_name VARCHAR(255),
    manufacturer_id VARCHAR(100),
    sensing_type VARCHAR(100),

    --location ENUM('TOP','SIDE','COAXIAL','OTHER'),

    sampling_rate_hz DOUBLE PRECISION,

    last_calibration_date DATE
);

CREATE TABLE AMSystem_Calibration (
    calibration_id VARCHAR(100) PRIMARY KEY,
    am_system_id VARCHAR(100),

    operator_person_id VARCHAR(100),

    calibration_date DATE,
    calibration_result VARCHAR(10), -- Pass/Fail

    calibration_notes TEXT,
    calibration_report_uri TEXT
);

-- =========================================================
-- SYSTEM MODULE
-- =========================================================

CREATE TABLE System (
    system_id VARCHAR(100) PRIMARY KEY,
    machine_id VARCHAR(100)
        REFERENCES AMSystem(am_system_id),
    parent_system_id VARCHAR(100)
        REFERENCES System(system_id),

    system_name VARCHAR(255),
    system_type VARCHAR(255),
    manufacturer VARCHAR(255)
);
