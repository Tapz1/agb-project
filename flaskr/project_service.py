from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_project(project_name, project_path, owners_email, town, date):
    db = get_db_connection()

    cur = db.cursor()
    insert_sql = "INSERT INTO projects (project_name, project_path, owners_email, town, date) " \
                 "VALUES(:project_name, :project_path, :owners_email, :town, :date)"
    cur.execute(insert_sql, {'project_name': project_name, 'project_path': project_path, 'owners_email': owners_email, 'town': town, 'date': date})

    db.commit()
    cur.close()
    #conn.close()


def get_all_projects(limit, offset, sort_by):
    """paginated"""
    db = get_db_connection()

    cur = db.cursor()
    print(f"sort_by value in db: {sort_by}")
    projects = list(cur.execute(
        f"SELECT * FROM projects ORDER BY date {sort_by}").fetchall())

    paginated_projects = list(cur.execute(
        f"SELECT * FROM projects ORDER BY date {sort_by} LIMIT {limit} OFFSET {offset}"
    ).fetchall())

    cur.close()
    return projects, paginated_projects


def get_projects_by_town(town, limit, offset, sort_by):
    """paginated"""
    db = get_db_connection()

    cur = db.cursor()

    projects = list(cur.execute(
        f"SELECT * FROM projects WHERE town = ? ORDER BY date {sort_by}", [town]
    ).fetchall())

    paginated_projects = list(cur.execute(
        f"SELECT * FROM projects WHERE town = ? ORDER BY date {sort_by} LIMIT {limit} OFFSET {offset}", [town]
    ).fetchall())

    cur.close()
    return projects, paginated_projects


def get_projects_by_email_db(email):
    db = get_db_connection()

    cur = db.cursor()

    projects = cur.execute(
        "SELECT * "
        "FROM projects "
        "WHERE email = ?"
        "INNER JOIN testimonials on testimonials.email = projects.owners_email",
        [email]
    ).fetchall()

    cur.close()
    return projects


def get_project_names():
    db = get_db_connection()

    cur = db.cursor()

    projects = list(cur.execute("SELECT name FROM projects").fetchall())

    cur.close()
    return projects


def get_project_id(project_name):
    db = get_db_connection()

    cur = db.cursor()

    project_id = cur.execute("SELECT project_id FROM projects WHERE project_name = ?", [project_name]).fetchone()[0]

    print(project_id)
    cur.close()
    return project_id


def get_project_name(project_id):
    db = get_db_connection()

    cur = db.cursor()

    project_name = cur.execute("SELECT project_name FROM projects WHERE project_id = ?", [project_id]).fetchone()[0]

    print(project_name)
    cur.close()
    return project_name


def get_project_towns():
    db = get_db_connection()

    cur = db.cursor()
    print("getting towns")
    towns = list(cur.execute("SELECT DISTINCT(town) FROM projects").fetchall())

    cur.close()
    return towns


def delete_project_row(project_id):
    db = get_db_connection()

    cur = db.cursor()

    cur.execute("DELETE FROM images WHERE project_id = ?", [project_id])
    db.commit()
    cur.execute("DELETE FROM projects WHERE project_id = ?", [project_id])
    db.commit()

    cur.close()
    db.close()


def get_project_id_by_email(email):
    db = get_db_connection()

    cur = db.cursor()

    project = list(cur.execute("SELECT * FROM projects WHERE email = ?", [email]).fetchone())

    cur.close()

    return project[0]


def project_exists(email):
    db = get_db_connection()

    cur = db.cursor()

    count = cur.execute("SELECT COUNT(*) FROM projects WHERE email = ?", [email]).fetchone()[0]
    print(f"count: {count}")
    cur.close()

    return count
