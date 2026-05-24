-- =========================================================
-- MACHINE MODULE
-- =========================================================

CREATE TABLE AMSystem_Performance (
    am_system_performance_id VARCHAR(100) PRIMARY KEY,

    max_build_rate_cm3h DOUBLE PRECISION,
    min_layer_thickness_um DOUBLE PRECISION,
    max_layer_thickness_um DOUBLE PRECISION,
    total_build_volume_mm3 DOUBLE PRECISION
);


CREATE TABLE AMSystem (
    am_system_id VARCHAR(100) PRIMARY KEY,
    am_system_name VARCHAR(255),
    am_system_facility VARCHAR(255),
    am_system_location TEXT, -- globalAddressFormat (ISO 19160)
    am_machine_name VARCHAR(255),
    am_machine_serial_number VARCHAR(255),
    am_machine_model_name VARCHAR(255),
    am_system_process_type VARCHAR(100), -- ENUM ASTM 52900
    AMSystem_Performance VARCHAR(100)
        REFERENCES AMSystem_Performance(am_system_performance_id)

    -- processable_raw_materials TEXT[], stringArray

    -- am_system_software TEXT[]  stringArray (software IDs + versions)
);

CREATE TABLE InSituMonitoringSystem (
    in_situ_system_id VARCHAR(100) PRIMARY KEY,
    machine_id VARCHAR(100)
        REFERENCES AMSystem(am_system_id),
    model_name VARCHAR(255),
    manufacturer_id VARCHAR(100),
    sensing_type VARCHAR(100),
    --location ENUM('TOP','SIDE','COAXIAL','OTHER'),
    sampling_rate_hz DOUBLE PRECISION

);

