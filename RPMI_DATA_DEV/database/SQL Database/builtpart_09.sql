-- =========================================================
-- PART MODULE
-- =========================================================

CREATE TABLE BuiltPart (
    built_part_id VARCHAR(100) PRIMARY KEY,

    build_producing_this_part VARCHAR(100) REFERENCES Build(build_id),

    --built_part_process VARCHAR(255) REFERENCES Process(process_id),

    part_location_on_build VARCHAR(255),

    part_orientation VARCHAR(255),

    design_of_this_part VARCHAR(100)
    REFERENCES PartDesign(part_design_id)

   
    
);