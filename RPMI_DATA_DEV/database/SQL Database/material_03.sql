-- =========================================================
-- MATERIAL MODULE
-- =========================================================

CREATE TABLE Material (
    material_id VARCHAR(100) PRIMARY KEY,
    material_name VARCHAR(255),
    generic_material_type VARCHAR(50),  -- Ceramic / Metal / Polymer / etc
    specific_material_type VARCHAR(50), -- Aluminum / Titanium / etc
    material_grade VARCHAR(255),
    material_product_specification TEXT  -- URI
);

-- =========================================================
-- MATERIAL STOCK MODULE
-- =========================================================
CREATE TABLE MaterialStock (
    material_stock_id VARCHAR(100) PRIMARY KEY,

    material_id VARCHAR(100)
        REFERENCES Material(material_id),

    manufacturing_lot VARCHAR(255),

    purchase_order_number VARCHAR(255),

    stock_quantity_kg DOUBLE PRECISION,

    stock_form VARCHAR(50), -- Bulk / Wire / Powder / Liquid

    stock_owner VARCHAR(100),

    stock_location TEXT, -- ISO 19160 globalAddressFormat

    stock_storage_environment TEXT,

    stock_certification_date DATE,

    stock_certificate_uri TEXT
);


-- =========================================================
-- Material Characterization Module
-- =========================================================

CREATE TABLE MaterialCharacterization (
    characterization_id VARCHAR(100) PRIMARY KEY,

    material_stock_id VARCHAR(100)
        REFERENCES MaterialStock(material_stock_id),

    chemistry_characterization_uri TEXT,
    mechanical_characterization_uri TEXT,
    nde_characterization_uri TEXT
);

-- =========================================================
-- MATERIAL FEEDSTOCK MODULE
-- =========================================================

CREATE TABLE Feedstock (
    feedstock_id VARCHAR(100) PRIMARY KEY,

    material_stock_id VARCHAR(100)
        REFERENCES MaterialStock(material_stock_id),

    --source_stock_ids TEXT[] stringArray

    source_stock_quantity_kg DOUBLE PRECISION,

    feedstock_preparation_date DATE,

    ingot_id VARCHAR(255)
);

