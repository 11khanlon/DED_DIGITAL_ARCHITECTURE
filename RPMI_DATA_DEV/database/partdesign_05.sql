
-- =============== Build geometry==========================
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

CREATE TABLE PartDesign (
    part_design_id VARCHAR(100) PRIMARY KEY,
    part_design_CAD_file VARCHAR(255), 
    part_geometry VARCHAR(255) REFERENCES BuildGeometry(build_geometry_id)

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
