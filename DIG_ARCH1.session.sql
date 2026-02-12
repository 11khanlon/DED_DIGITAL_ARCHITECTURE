-- See all projects
SELECT * FROM projects;

-- Filter by status
SELECT * FROM projects WHERE status = 'Active';

-- Order by start date descending
SELECT * FROM projects ORDER BY start_date DESC;

-- Count projects per owner
SELECT owner, COUNT(*) FROM projects GROUP BY owner;

-- Insert a new project
INSERT INTO projects (project_name, owner, start_date, end_date, status)
VALUES ('Test Project', 'Alex', '2025-10-05', '2025-11-05', 'Active');

-- Update a project
UPDATE projects SET status = 'Completed' WHERE project_id = 1;
