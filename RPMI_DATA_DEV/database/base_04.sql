---========= Base, organization, person, qualification =========

CREATE TABLE ORGANIZATION (
    org_id VARCHAR(100) PRIMARY KEY,
    org_name VARCHAR(255),
    org_location VARCHAR(255), 
    org_description TEXT
);

CREATE TABLE Project (
    project_id VARCHAR(100) PRIMARY KEY,
    project_name VARCHAR(255),
    project_sponsor VARCHAR(255)
   
);

CREATE TABLE PERSON (
    person_id VARCHAR(100) PRIMARY KEY,
    organization_id VARCHAR(100)
        REFERENCES Organization(org_id),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    person_description TEXT

);


CREATE TABLE BASE (
    base_id VARCHAR(100) PRIMARY KEY,
    org_id VARCHAR(100) REFERENCES ORGANIZATION(org_id),
    person_id VARCHAR(100) REFERENCES PERSON(person_id),
    base_name VARCHAR(255),
    base_description TEXT
);
