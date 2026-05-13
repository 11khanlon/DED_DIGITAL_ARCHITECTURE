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