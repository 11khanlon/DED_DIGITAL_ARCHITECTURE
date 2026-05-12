-- =========================================================
-- PROJECT MODULE
-- =========================================================

CREATE TABLE Project (
    project_id VARCHAR(100) PRIMARY KEY,
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
    maintenance_date TIMESTAMP
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

--

-- =========================================================
-- PROCESS PLAN MODULE
-- =========================================================

CREATE TABLE ProcessPlan (
    process_plan_id VARCHAR(100) PRIMARY KEY,

    strategy VARCHAR(255),

    nominal_laser_power FLOAT,
    nominal_scan_speed FLOAT,
    nominal_hatch_spacing FLOAT
);

-- =========================================================
-- MATERIAL FORM MODULE
-- =========================================================

CREATE TABLE MaterialForm (
    material_form_id VARCHAR(100) PRIMARY KEY,

    form_type VARCHAR(100)
);

-- =========================================================
-- MATERIAL CERTIFICATION MODULE
-- =========================================================

CREATE TABLE MaterialCertification (
    certification_id VARCHAR(100) PRIMARY KEY,

    certification_type VARCHAR(255),
    certification_date TIMESTAMP,
    standard VARCHAR(255),
    lot_number VARCHAR(255)
);

-- =========================================================
-- MATERIAL MODULE
-- =========================================================

CREATE TABLE Material (

    material_id VARCHAR(100) PRIMARY KEY,

    material_form_id VARCHAR(100)
        REFERENCES MaterialForm(material_form_id),

    certification_id VARCHAR(100)
        REFERENCES MaterialCertification(certification_id),

    material_name VARCHAR(255),

    alloy VARCHAR(255),

    supplier VARCHAR(255),

    lot_number VARCHAR(255),

    manufacturer VARCHAR(255),

    material_standard VARCHAR(255),

    received_date TIMESTAMP,

    expiry_date TIMESTAMP,

    reuse_count INT,

    recycled BOOLEAN
);

-- =========================================================
-- POWDER CHARACTERISTICS MODULE
-- =========================================================

CREATE TABLE MaterialParameter (

    material_parameter_id VARCHAR(100) PRIMARY KEY,

    parameter_name VARCHAR(255),

    parameter_category VARCHAR(255),

    unit VARCHAR(100),

    data_type VARCHAR(100),

    physical_meaning TEXT
);

-- =========================================================
-- MATERIAL THERMAL PROPERTIES MODULE
-- =========================================================

CREATE TABLE MaterialProperty (

    property_id VARCHAR(100) PRIMARY KEY,

    material_id VARCHAR(100)
        REFERENCES Material(material_id),

    material_parameter_id VARCHAR(100)
        REFERENCES MaterialParameter(material_parameter_id),

    value_numeric FLOAT,

    value_text TEXT,

    measurement_date TIMESTAMP,

    quality_flag VARCHAR(100)
);


-- =========================================================
-- Substrate information
CREATE TABLE Substrate (
    substrate_id VARCHAR(100) PRIMARY KEY,
    material_id VARCHAR(100) REFERENCES Material(material_id),
    thickness_mm FLOAT,
    width_mm FLOAT,
    height_mm FLOAT
);


---Build geometry--- 

CREATE TABLE BuildGeometry (

    build_geometry_id VARCHAR(100) PRIMARY KEY,

    geometry_name VARCHAR(255),

    cad_file_location TEXT,

    stl_file_location TEXT,

    native_cad_format VARCHAR(100),

    geometry_version VARCHAR(100),

    checksum VARCHAR(255),

    units VARCHAR(50),

    bounding_box_x FLOAT,
    bounding_box_y FLOAT,
    bounding_box_z FLOAT,

    part_count INT
);
-- =========================================================
-- BUILD GEOMETRY MODULE
-- =========================================================

CREATE TABLE Build (

    build_id VARCHAR(100) PRIMARY KEY,

    project_id VARCHAR(100)
        REFERENCES Project(project_id),

    machine_id VARCHAR(100)
        REFERENCES AMMachine(machine_id),

    operator_id VARCHAR(100)
        REFERENCES Person(person_id),

    process_plan_id VARCHAR(100)
        REFERENCES ProcessPlan(process_plan_id),

    build_geometry_id VARCHAR(100)
        REFERENCES BuildGeometry(build_geometry_id),

    feedstock_material_id VARCHAR(100)
        REFERENCES Material(material_id),

    substrate_material_id VARCHAR(100)
        REFERENCES Material(material_id),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    build_status VARCHAR(100),

    build_type VARCHAR(255),

    layer_count INT,

    notes TEXT
);



-- =========================================================
-- GEOMETRY REGION MODULE
-- =========================================================

CREATE TABLE GeometryRegion (
    region_id VARCHAR(100) PRIMARY KEY,

    build_geometry_id VARCHAR(100)
        REFERENCES BuildGeometry(build_geometry_id),

    region_name VARCHAR(255),
    region_type VARCHAR(255),

    mesh_subset TEXT,

    criticality_level VARCHAR(100)
);



-- =========================================================
-- PARAMETER MODULE
-- =========================================================

CREATE TABLE BuildParameter (
     id SERIAL PRIMARY KEY,
    build_id VARCHAR,
    parameter_id VARCHAR,
    value_text TEXT,
    value_numeric DOUBLE PRECISION,
    unit VARCHAR,
    description TEXT,
    source VARCHAR
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
    part_id VARCHAR(100) PRIMARY KEY,

    build_id VARCHAR(100) REFERENCES Build(build_id),

    part_name VARCHAR(255),

    serial_number VARCHAR(255),

    orientation VARCHAR(255),

    location_in_build VARCHAR(255)
);

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
-- TEST RESULT MODULE
-- =========================================================

CREATE TABLE TestResult (
    result_id VARCHAR(100) PRIMARY KEY,

    tic_id VARCHAR(100) REFERENCES TICInspection(tic_id),

    measurement_type VARCHAR(255),

    value FLOAT,

    unit VARCHAR(100),

    spatial_coordinate VARCHAR(255),

    defect_label VARCHAR(255)
);


---
CREATE TABLE BASE (
    base_id VARCHAR(100) PRIMARY KEY,
    org_id VARCHAR(100) REFERENCES ORGANIZATION(org_id),
    person_id VARCHAR(100) REFERENCES PERSON(person_id),
    qualification_id VARCHAR(100) REFERENCES QUALIFICATION(qualification_id),
    base_name VARCHAR(255),
    base_description TEXT
)

CREATE TABLE ORGANIZATION (
    org_id VARCHAR(100) PRIMARY KEY,
    org_name VARCHAR(255),
    org_location VARCHAR(255), 
    org_description TEXT,
)

CREATE TABLE PERSON (
     person_id VARCHAR(100) PRIMARY KEY,

    organization_id VARCHAR(100)
        REFERENCES Organization(organization_id),

    first_name VARCHAR(255),

    last_name VARCHAR(255),

    person_description TEXT

)

CREATE TABLE QUALIFICATION (
    qualification_id VARCHAR(100) PRIMARY KEY,

        person_id VARCHAR(100)
            REFERENCES Person(person_id),

        qualification_type VARCHAR(255),

        qualification_level VARCHAR(255),

        certification_date TIMESTAMP,

        expiration_date TIMESTAMP,

        issuing_organization VARCHAR(255)

)