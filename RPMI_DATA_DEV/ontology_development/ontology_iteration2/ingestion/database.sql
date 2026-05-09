-- =========================================================
-- PROJECT MODULE
-- =========================================================

CREATE TABLE Project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    customer VARCHAR(255),
    qualification_level VARCHAR(100),
    program_name VARCHAR(255),
    description TEXT
);

-- =========================================================
-- MACHINE MODULE
-- =========================================================

CREATE TABLE AMMachine (
    machine_id SERIAL PRIMARY KEY,
    manufacturer_id INT,
    machine_model VARCHAR(255),
    serial_number VARCHAR(255),
    process_type VARCHAR(100),
    installation_date TIMESTAMP,
    location VARCHAR(255)
);

-- =========================================================
-- SYSTEM MODULE
-- =========================================================

CREATE TABLE System (
    system_id SERIAL PRIMARY KEY,
    machine_id INT REFERENCES AMMachine(machine_id),

    system_name VARCHAR(255),
    system_type VARCHAR(255),
    manufacturer VARCHAR(255),
    firmware_version VARCHAR(255),

    sampling_rate FLOAT,
    coordinate_frame VARCHAR(255)
);

-- =========================================================
-- PROCESS PLAN MODULE
-- =========================================================

CREATE TABLE ProcessPlan (
    process_plan_id SERIAL PRIMARY KEY,

    strategy VARCHAR(255),

    nominal_laser_power FLOAT,
    nominal_scan_speed FLOAT,
    nominal_hatch_spacing FLOAT
);

-- =========================================================
-- MATERIAL FORM MODULE
-- =========================================================

CREATE TABLE MaterialForm (
    material_form_id SERIAL PRIMARY KEY,

    form_type VARCHAR(100)
);

-- =========================================================
-- MATERIAL CERTIFICATION MODULE
-- =========================================================

CREATE TABLE MaterialCertification (
    certification_id SERIAL PRIMARY KEY,

    certification_type VARCHAR(255),
    certification_date TIMESTAMP,
    standard VARCHAR(255),
    lot_number VARCHAR(255)
);

-- =========================================================
-- MATERIAL MODULE
-- =========================================================

CREATE TABLE Material (
    material_id SERIAL PRIMARY KEY,

    material_form_id INT REFERENCES MaterialForm(material_form_id),
    certification_id INT REFERENCES MaterialCertification(certification_id),

    material_name VARCHAR(255),
    material_standard VARCHAR(255),
    manufacturer VARCHAR(255),

    material_state_id INT
);

-- =========================================================
-- POWDER CHARACTERISTICS MODULE
-- =========================================================

CREATE TABLE PowderCharacteristics (
    powder_characteristics_id SERIAL PRIMARY KEY,

    material_id INT REFERENCES Material(material_id),

    particle_size_d10 FLOAT,
    particle_size_d50 FLOAT,
    particle_size_d90 FLOAT,

    sphericity FLOAT,
    flowability FLOAT,
    apparent_density FLOAT
);

-- =========================================================
-- MATERIAL THERMAL PROPERTIES MODULE
-- =========================================================

CREATE TABLE MaterialThermalProperties (
    thermal_property_id SERIAL PRIMARY KEY,

    material_id INT REFERENCES Material(material_id),

    thermal_conductivity FLOAT,
    specific_heat FLOAT,
    melting_temp FLOAT,
    cte FLOAT
);

-- =========================================================
-- BUILD GEOMETRY MODULE
-- =========================================================

CREATE TABLE BuildGeometry (
    build_geometry_id SERIAL PRIMARY KEY,

    geometry_name VARCHAR(255),

    cad_file_location TEXT,
    stl_file_location TEXT,

    native_cad_format VARCHAR(100),
    geometry_version VARCHAR(100),

    checksum VARCHAR(255),
    units VARCHAR(50),

    bounding_box VARCHAR(255),

    part_count INT
);

-- =========================================================
-- GEOMETRY REGION MODULE
-- =========================================================

CREATE TABLE GeometryRegion (
    region_id SERIAL PRIMARY KEY,

    build_geometry_id INT REFERENCES BuildGeometry(build_geometry_id),

    region_name VARCHAR(255),
    region_type VARCHAR(255),

    mesh_subset TEXT,

    criticality_level VARCHAR(100)
);

-- =========================================================
-- BUILD MODULE (CENTRAL NODE)
-- =========================================================

CREATE TABLE Build (
    build_id SERIAL PRIMARY KEY,

    project_id INT REFERENCES Project(project_id),
    machine_id INT REFERENCES AMMachine(machine_id),

    feedstock_material_id INT REFERENCES Material(material_id),
    substrate_material_id INT REFERENCES Material(material_id),

    process_plan_id INT REFERENCES ProcessPlan(process_plan_id),

    organization_id INT,
    operator_id INT,

    build_geometry_id INT REFERENCES BuildGeometry(build_geometry_id),

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    build_status VARCHAR(100)
);

-- =========================================================
-- PARAMETER MODULE
-- =========================================================

CREATE TABLE Parameter (
    parameter_id SERIAL PRIMARY KEY,

    parameter_name VARCHAR(255),
    parameter_type VARCHAR(255),

    unit VARCHAR(100),

    physical_meaning TEXT,

    data_type VARCHAR(100)
);

-- =========================================================
-- TIC EVENT MODULE
-- =========================================================

CREATE TABLE TICEvent (
    event_id SERIAL PRIMARY KEY,

    build_id INT REFERENCES Build(build_id),

    system_id INT REFERENCES System(system_id),

    parameter_id INT REFERENCES Parameter(parameter_id),

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

-- =========================================================
-- PART MODULE
-- =========================================================

CREATE TABLE Part (
    part_id SERIAL PRIMARY KEY,

    build_id INT REFERENCES Build(build_id),

    part_name VARCHAR(255),

    serial_number VARCHAR(255),

    orientation VARCHAR(255),

    location_in_build VARCHAR(255)
);

-- =========================================================
-- TIC INSPECTION MODULE
-- =========================================================

CREATE TABLE TICInspection (
    tic_id SERIAL PRIMARY KEY,

    part_id INT REFERENCES Part(part_id),

    method VARCHAR(255),

    inspection_date TIMESTAMP,

    operator VARCHAR(255),

    region VARCHAR(255)
);

-- =========================================================
-- TEST RESULT MODULE
-- =========================================================

CREATE TABLE TestResult (
    result_id SERIAL PRIMARY KEY,

    tic_id INT REFERENCES TICInspection(tic_id),

    measurement_type VARCHAR(255),

    value FLOAT,

    unit VARCHAR(100),

    spatial_coordinate VARCHAR(255),

    defect_label VARCHAR(255)
);