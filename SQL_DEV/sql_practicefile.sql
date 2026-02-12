-- View all projects
SELECT * FROM projects;

-- Filter active projects
SELECT * FROM projects WHERE status = 'Active';

-- Sort by start date
SELECT * FROM projects ORDER BY start_date DESC;

-- Count projects per owner
SELECT owner, COUNT(*) FROM projects GROUP BY owner;


-- Add a new project
INSERT INTO projects (project_name, owner, start_date, end_date, status)
VALUES ('Test Project 2', 'Alex', '2025-10-10', '2025-11-10', 'Active');

-- Update a project
UPDATE projects SET status = 'Completed' WHERE project_id = 1;

-- Delete a project
DELETE FROM projects WHERE project_id = 4;
