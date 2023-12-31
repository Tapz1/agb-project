
CREATE TABLE IF NOT EXISTS testimonials (
    testimonial_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    town TEXT NOT NULL,
    is_approved INTEGER DEFAULT 0 NOT NULL,
    project_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_path TEXT NOT NULL,
    owners_email TEXT,
    town TEXT NOT NULL,
    date TEXT NOT NULL,
    testimonial_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY,
    date_uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_path TEXT NOT NULL,
    filename TEXT NOT NULL,
    project_name TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    isChecked INTEGER DEFAULT 0 NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

