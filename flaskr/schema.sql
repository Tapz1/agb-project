
CREATE TABLE IF NOT EXISTS testimonials (
    testimonial_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    town TEXT NOT NULL,
    is_approved INTEGER DEFAULT 0 NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    project_id INTEGER
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    project_path TEXT NOT NULL,
    owners_email TEXT,
    town TEXT NOT NULL,
    date TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_path TEXT NOT NULL,
    filename TEXT NOT NULL,
    project_name TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
)