-- =========================================================
-- PROCESS PLAN MODULE
-- =========================================================

CREATE TABLE ProcessControl (
    process_id VARCHAR(100) PRIMARY KEY,

    am_system_id VARCHAR(100),
    built_part_id VARCHAR(100) REFERENCES BuiltPart(built_part_id),

    --feedstock_ids TEXT[],   Process Feedstock

    --in_situ_monitoring_system_ids TEXT[],

    build_platform_id VARCHAR(100),

    build_platform_configuration TEXT,

    build_platform_position_mm FLOAT,

    purge_gas_id VARCHAR(100),

    platform_leveling_method TEXT,

    build_id VARCHAR(100),

    chamber_dew_point_limit_c FLOAT,

    chamber_oxygen_limit_ppm FLOAT,

    chamber_atmosphere VARCHAR(100), -- enum

    layer_thickness_um FLOAT

    -- post_process_ids TEXT[],

    --process_sequence TEXT[]  ordered Process/PostProcess IDs
);

CREATE TABLE ProcessData (
    process_data_id VARCHAR(100) PRIMARY KEY,

    process_id VARCHAR(100)
        REFERENCES ProcessControl(process_id),

    process_duration INTERVAL,

    process_location TEXT, -- ISO 19160 globalAddressFormat

    process_start_time TIMESTAMP,
    process_end_time TIMESTAMP,

    feedstock_used_kg FLOAT,
    feedstock_top_up_kg FLOAT,
    feedstock_recovered_kg FLOAT,

    material_feed_speed_kg_h FLOAT,

    chamber_dew_point_c FLOAT,
    chamber_pressure_pa FLOAT,
    chamber_temperature_c FLOAT,

    gas_line_pressure_pa FLOAT,

    process_log TEXT,
    process_events TEXT,
    process_alarms TEXT
);

CREATE TABLE ProcessMonitoringData (
    monitoring_id VARCHAR(100) PRIMARY KEY,

    process_id VARCHAR(100) REFERENCES ProcessControl(process_id),

    monitoring_data_type VARCHAR(50), -- Single / TimeSeries / Image / Video

    sampling_rate_hz FLOAT,

    timestamp TIMESTAMP,

    layer_number INT,

    in_situ_system_id VARCHAR(100)
);