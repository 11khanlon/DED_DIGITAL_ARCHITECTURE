-- =========================================================
-- BUILD GEOMETRY MODULE
-- =========================================================

CREATE TABLE Build (

    build_id VARCHAR(100) PRIMARY KEY,

    project_id VARCHAR(100)
        REFERENCES Project(project_id),

    machine_id VARCHAR(100)
        REFERENCES AMMachine(machine_id),

    process_plan_id VARCHAR(100)
        REFERENCES ProcessPlan(process_plan_id),

    build_geometry_id VARCHAR(100)
        REFERENCES BuildGeometry(build_geometry_id),

    feedstock_material_id VARCHAR(100)
        REFERENCES Material(material_id),

    base_id VARCHAR(100)
        REFERENCES Base(base_id),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    build_status VARCHAR(100),

    build_type VARCHAR(255),

    layer_count INT,

    notes TEXT
);
