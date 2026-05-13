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
    project_creator VARCHAR(255)
        REFERENCES ORGANIZATION(org_id), 
    project_sponsor VARCHAR(255)
        REFERENCES ORGANIZATION(org_id),
    project_start_date TIMESTAMP,
    project_end_date TIMESTAMP,
    project_builds VARCHAR(255) 
        REFERENCES (Build(build_id))

    description TEXT
);

CREATE TABLE PERSON (
    person_id VARCHAR(100) PRIMARY KEY,
    organization_id VARCHAR(100)
        REFERENCES Organization(org_id),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    person_description TEXT

);

CREATE TABLE QUALIFICATION (
    qualification_id VARCHAR(100) PRIMARY KEY,
        person_id VARCHAR(100)
            REFERENCES Person(person_id),
        qualification_type VARCHAR(255),
        qualification_level VARCHAR(255),
        certification_date TIMESTAMP,
        expiration_date TIMESTAMP,

        issuing_organization VARCHAR(255)

);

CREATE TABLE BASE (
    base_id VARCHAR(100) PRIMARY KEY,
    org_id VARCHAR(100) REFERENCES ORGANIZATION(org_id),
    person_id VARCHAR(100) REFERENCES PERSON(person_id),
    qualification_id VARCHAR(100) REFERENCES QUALIFICATION(qualification_id),
    base_name VARCHAR(255),
    base_description TEXT
);
