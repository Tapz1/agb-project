from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_project(name, project_path, owners_email, town, date):
    conn = get_db_connection()

    cur = conn.cursor()
    insert_sql = "INSERT INTO projects (project_name, project_path, owners_email, town, date) " \
                 "VALUES(:name, :project_path, :owners_email, :town, :date)"
    cur.execute(insert_sql, {'project_name': name, 'project_path': project_path, 'owners_email': owners_email, 'town': town, 'date': date})

    conn.commit()
    cur.close()
    conn.close()


def get_projects():
    conn = get_db_connection()

    cur = conn.cursor()

    projects = list(cur.execute("SELECT * FROM projects").fetchall())

    cur.close()
    return projects


def get_project_names():
    conn = get_db_connection()

    cur = conn.cursor()

    projects = list(cur.execute("SELECT name FROM projects").fetchall())

    cur.close()
    return projects
