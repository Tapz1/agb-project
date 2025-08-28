import logging
import traceback

from flask import redirect, request

from flaskr.db import get_db
import traceback as tb


def get_db_connection():
    db = get_db()
    return db


def add_project(project_id, project_name, project_path, owners_email, town, date):
    """adding project_id, project_name, project_path, owners_email, town, date to db"""

    try:
        db = get_db_connection()

        cur = db.cursor()

        insert_sql = "INSERT INTO projects (project_id, project_name, project_path, owners_email, town, date) " \
                     "VALUES(:project_id, :project_name, :project_path, :owners_email, :town, :date)"
        cur.execute(insert_sql, {'project_id': project_id, 'project_name': project_name, 'project_path': project_path, 'owners_email': owners_email, 'town': town, 'date': date})

        db.commit()
        cur.close()

        return True
    except Exception as e:
        msg = f"Error adding project to db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_all_projects(limit, offset):
    """paginated"""
    try:
        db = get_db_connection()

        cur = db.cursor()
        projects = list(cur.execute(
            f"SELECT * FROM projects").fetchall())

        paginated_projects = list(cur.execute(
            f"SELECT * FROM projects LIMIT {limit} OFFSET {offset}"
        ).fetchall())

        cur.close()
        return projects, paginated_projects
    except Exception as e:
        msg = "Could not retrieve all projects from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_projects_by_town(town, limit, offset):
    """paginated"""
    try:
        db = get_db_connection()

        cur = db.cursor()

        projects = list(cur.execute(
            f"SELECT * FROM projects WHERE town = ?", [town]
        ).fetchall())

        paginated_projects = list(cur.execute(
            f"SELECT * FROM projects WHERE town = ? LIMIT {limit} OFFSET {offset}", [town]
        ).fetchall())

        cur.close()
        return projects, paginated_projects
    except Exception as e:
        msg = "Could not retrieve all projects by town from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_project_id(project_name):
    try:
        db = get_db_connection()

        cur = db.cursor()

        project_id = cur.execute("SELECT project_id FROM projects WHERE project_name = ?", [project_name]).fetchone()[0]

        # print(project_id)
        cur.close()
        return project_id

    except Exception as e:
        msg = f"Could not retrieve project_id from the project_name: {project_name}"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_project_item_db(project_id, item):
    try:
        db = get_db_connection()

        cur = db.cursor()

        project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_id = ?", [project_id]).fetchone()[0]

        # print(project_item)
        cur.close()
        return project_item

    except Exception as e:
        msg = "Could not retrieve project item from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_project_item_by_name_db(project_name, item):
    try:
        db = get_db_connection()

        cur = db.cursor()

        project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_name = ?", [project_name]).fetchone()[0]

        # print(project_item)
        cur.close()
        return project_item

    except Exception as e:
        msg = "Could not retrieve project item by name from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_project_item_by_id_db(project_id, item):
    try:
        db = get_db_connection()

        cur = db.cursor()

        project_item = cur.execute(f"SELECT {item} FROM projects WHERE project_id = ?", [project_id]).fetchone()[0]

        # print(project_item)
        cur.close()
        return project_item

    except Exception as e:
        msg = f"Could not retrieve project item={item} by id from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_project_info(project_id):
    try:
        db = get_db_connection()

        cur = db.cursor()

        project_info = cur.execute(f"SELECT * FROM projects WHERE project_id = ?", [project_id]).fetchone()

        # print(project_item)
        cur.close()
        return project_info

    except Exception as e:
        msg = "Could not retrieve project_info from db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def edit_project_db(project_id, project_name, project_path, owners_email, town, date):
    try:
        db = get_db_connection()
        cur = db.cursor()

        cur.execute("UPDATE projects SET project_name = ?, project_path = ?, owners_email = ?, town = ?, date = ? "
                    "WHERE project_id = ?", [project_name, project_path, owners_email, town, date, project_id])

        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        msg = "Could not update the project in db"
        logging.error(f"{msg}: {e}\n{tb.format_exception(None, e, e.__traceback__)}")
        return False


def get_multiple_project_items_db(item):
    db = get_db_connection()

    cur = db.cursor()
    # print(f"getting {item}s")
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



