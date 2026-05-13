-- =========================================================
-- BUILD GEOMETRY MODULE
-- =========================================================

CREATE TABLE Build (

    build_id VARCHAR(100) PRIMARY KEY,

    project_id VARCHAR(100)
        REFERENCES Project(project_id),

    amsystem_id VARCHAR(100)
        REFERENCES AMSystem(am_system_id),

    material_id VARCHAR(255)
        REFERENCES Material(material_id),
    
    parameter_id VARCHAR(100)
    REFERENCES Parameter(parameter_id),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    build_status VARCHAR(100),

    build_type VARCHAR(255),

    layer_count INT,

    notes TEXT
);
