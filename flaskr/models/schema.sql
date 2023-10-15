CREATE TABLE IF NOT EXISTS testimonials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    project_fk INTEGER,
    FOREIGN KEY(project_fk) REFERENCES gallery(project_id)
    is_approved INTEGER DEFAULT 0 NOT NULL
);

