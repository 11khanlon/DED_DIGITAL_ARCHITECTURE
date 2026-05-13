-- =========================================================
-- MACHINE MODULE
-- =========================================================

CREATE TABLE AMMachine (

    machine_id VARCHAR(100) PRIMARY KEY,
    equipment_name VARCHAR(255),
    manufacturer_name VARCHAR(255),
    machine_model VARCHAR(255),
    process_type VARCHAR(255),
    laser_type VARCHAR(255),
    controller_name VARCHAR(255),
    nozzle_type VARCHAR(255),
    heat_source VARCHAR(255),
    deposition_type VARCHAR(255),
    location VARCHAR(255),
    build_volume_x_mm FLOAT,
    build_volume_y_mm FLOAT,
    build_volume_z_mm FLOAT,
    last_calibration_date TIMESTAMP,
    maintenance_date TIMESTAMP,
    sampling_rate_Hz FLOAT
);

-- =========================================================
-- SYSTEM MODULE
-- =========================================================

CREATE TABLE System (
    system_id VARCHAR(100) PRIMARY KEY,
    machine_id VARCHAR(100)
        REFERENCES AMMachine(machine_id),
    parent_system_id VARCHAR(100)
        REFERENCES System(system_id),

    system_name VARCHAR(255),
    system_type VARCHAR(255),
    manufacturer VARCHAR(255)
);
