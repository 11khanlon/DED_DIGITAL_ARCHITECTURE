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