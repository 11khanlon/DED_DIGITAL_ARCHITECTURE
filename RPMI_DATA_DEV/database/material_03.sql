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