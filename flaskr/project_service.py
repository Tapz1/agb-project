from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_project(project_id, project_name, project_path, owners_email, town, date):
    db = get_db_connection()

    cur = db.cursor()
    insert_sql = "INSERT INTO projects (project_id, project_name, project_path, owners_email, town, date) " \
                 "VALUES(:project_id, :project_name, :project_path, :owners_email, :town, :date)"
    cur.execute(insert_sql, {'project_id': project_id, 'project_name': project_name, 'project_path': project_path, 'owners_email': owners_email, 'town': town, 'date': date})

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


def get_project_id(project_name):
    db = get_db_connection()

    cur = db.cursor()

    project_id = cur.execute("SELECT project_id FROM projects WHERE project_name = ?", [project_name]).fetchone()[0]

    # print(project_id)
    cur.close()
    return project_id


def get_project_item_db(project_id, item):
    db = get_db_connection()

    cur = db.cursor()

    project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_id = ?", [project_id]).fetchone()[0]

    # print(project_item)
    cur.close()
    return project_item


def get_project_item_by_name_db(project_name, item):
    db = get_db_connection()

    cur = db.cursor()

    project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_name = ?", [project_name]).fetchone()[0]

    # print(project_item)
    cur.close()
    return project_item


def get_project_item_by_id_db(project_id, item):
    db = get_db_connection()

    cur = db.cursor()

    project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_id = ?", [project_id]).fetchone()[0]

    # print(project_item)
    cur.close()
    return project_item


def get_multiple_project_items_db(item):
    db = get_db_connection()

    cur = db.cursor()
    print(f"getting {item}s")
    items = list(cur.execute(f"SELECT DISTINCT({item}) FROM projects").fetchall())

    cur.close()
    return items


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

    project_path = list(cur.execute("SELECT project_id FROM projects WHERE owners_email = ?", [email]).fetchone())

    cur.close()
    # print(f"project id from db: {project_path[0]}")

    return project_path[0]


def project_exists(email):
    db = get_db_connection()

    cur = db.cursor()

    count = cur.execute("SELECT COUNT(*) FROM projects WHERE owners_email = ?", [email]).fetchone()[0]
    # print(f"project exists count: {count}")
    cur.close()

    return count


def get_limited_projects(limit):
    db = get_db_connection()

    cur = db.cursor()

    project = list(cur.execute("SELECT * FROM projects ORDER BY date desc LIMIT ?", [limit]).fetchall())

    cur.close()

    return project
