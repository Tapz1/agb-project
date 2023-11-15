from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def get_all_images():
    db = get_db_connection()

    cur = db.cursor()

    images = list(cur.execute("SELECT * FROM images").fetchall())

    cur.close()

    return images


def get_limited_images_db(limit):
    """used for carousel"""
    db = get_db_connection()

    cur = db.cursor()

    images = list(cur.execute("SELECT * FROM images ORDER BY date_uploaded DESC LIMIT ?", [limit]).fetchall())

    cur.close()

    return images


def get_images_from_project(project_id):
    db = get_db_connection()

    cur = db.cursor()

    images = list(cur.execute("SELECT * FROM images WHERE project_id = ?", [project_id]).fetchall())

    cur.close()

    return images


def get_project_thumbnail(project_id):
    db = get_db_connection()

    cur = db.cursor()

    thumbnail = list(cur.execute("SELECT * FROM images WHERE project_id = ? ORDER BY date_uploaded LIMIT 1", [project_id]).fetchone())

    cur.close()

    return thumbnail[2]


def add_image_db(image_path, filename, project_name, project_id):
    db = get_db_connection()
    cur = db.cursor()

    insert_sql = "INSERT INTO images (image_path, filename, project_name, project_id) " \
                 "VALUES(:image_path, :filename, :project_name, :project_id)"
    cur.execute(insert_sql,
                {'image_path': image_path, 'filename': filename, 'project_name': project_name, 'project_id': project_id})

    db.commit()
    cur.close()


def delete_image_db(image_id):
    db = get_db_connection()

    cur = db.cursor()

    cur.execute("DELETE FROM images WHERE image_id = ?", [image_id])
    db.commit()

    cur.close()
    db.close()


def get_image_by_id(image_id):
    db = get_db_connection()

    cur = db.cursor()

    thumbnail = list(cur.execute("SELECT * FROM images WHERE image_id = ?", [image_id]).fetchone())

    cur.close()

    return thumbnail
