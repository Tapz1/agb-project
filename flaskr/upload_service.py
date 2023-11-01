from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_project(project_name, project_path, owners_email, town, date):
    conn = get_db_connection()

    cur = conn.cursor()
    insert_sql = "INSERT INTO projects (project_name, project_path, owners_email, town, date) " \
                 "VALUES(:project_name, :project_path, :owners_email, :town, :date)"
    cur.execute(insert_sql, {'project_name': project_name, 'project_path': project_path, 'owners_email': owners_email, 'town': town, 'date': date})

    conn.commit()
    cur.close()
    #conn.close()


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


def get_project_id(project_name):
    conn = get_db_connection()

    cur = conn.cursor()

    project_id = cur.execute("SELECT project_id FROM projects WHERE project_name = ?", [project_name]).fetchall()
    print(f"acquired project_id = {project_id}")

    cur.close()
    return project_id


def delete_project_row(project_id):
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("DELETE FROM projects WHERE project_id = ?", [project_id])
    conn.commit()

    cur.close()
    conn.close()

