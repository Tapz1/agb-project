from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def get_all_images():
    try:
        db = get_db_connection()

        cur = db.cursor()

        images = list(cur.execute("SELECT * FROM images").fetchall())

        cur.close()

    except Exception as e:
        print("Could not get all images from db")
        print(e)
        return False

    return images


def get_checked_images_db():
    try:
        db = get_db_connection()

        cur = db.cursor()

        images = list(cur.execute("SELECT * FROM images WHERE isChecked = 1").fetchall())

        cur.close()
    except Exception as e:
        print("Could not get checked images in db")
        print(e)
        return False

    return images


def get_images_from_project(project_id):
    try:
        db = get_db_connection()

        cur = db.cursor()

        images = list(cur.execute("SELECT * FROM images WHERE project_id = ?", [project_id]).fetchall())

        cur.close()
    except Exception as e:
        print(f"Could not get images where project_id = {project_id}")
        print(e)
        return False

    return images


def get_project_thumbnail(project_id):
    try:
        db = get_db_connection()

        cur = db.cursor()

        thumbnail = list(cur.execute("SELECT * FROM images WHERE project_id = ? ORDER BY date_uploaded LIMIT 1", [project_id]).fetchone())

        cur.close()

        return thumbnail[2]
    except Exception as e:
        print("Could not get project for thumbnail")
        print(e)
        return False


def add_image_db(image_id, image_path, filename, project_name, project_id):
    try:
        db = get_db_connection()
        cur = db.cursor()

        insert_sql = "INSERT INTO images (image_id, image_path, filename, project_name, project_id) " \
                     "VALUES(:image_id, :image_path, :filename, :project_name, :project_id)"
        cur.execute(insert_sql,
                    {'image_id': image_id, 'image_path': image_path, 'filename': filename, 'project_name': project_name, 'project_id': project_id})

        db.commit()
        cur.close()
    except Exception as e:
        print("Could not add the image to db")
        print(e)
        return False

def delete_image_db(image_id):
    try:
        db = get_db_connection()

        cur = db.cursor()

        cur.execute("DELETE FROM images WHERE image_id = ?", [image_id])
        db.commit()

        cur.close()
        db.close()
    except Exception as e:
        print("Could not delete the image from image db")
        print(e)
        return False


def get_image_by_name(filename):
    try:
        db = get_db_connection()

        cur = db.cursor()

        thumbnail = list(cur.execute("SELECT * FROM images WHERE filename = ?", [filename]).fetchone())

        cur.close()

        return thumbnail
    except Exception as e:
        print("Could not get images by filename")
        print(e)
        return False


def update_check_db(image_id, isChecked):
    try:
        db = get_db_connection()
        cur = db.cursor()

        print("isCheck value: " + isChecked)
        cur.execute("UPDATE images SET isChecked = ? WHERE image_id = ?", (isChecked, image_id))
        db.commit()

        cur.close()
        db.close()
    except Exception as e:
        print("Could not set check status in db")
        print(e)
        return False

def edit_image_project_info(project_id, project_name, project_path):
    """for updating project info on the image db side"""
    try:
        db = get_db_connection()
        cur = db.cursor()

        cur.execute(f"UPDATE images SET project_name = ?, image_path = '{project_path}\\' || filename WHERE project_id = ?", [project_name, project_id])

        # TODO: testing commented out
        #check_images = list(cur.execute("SELECT * FROM images WHERE project_id = ?", [project_id]).fetchall())
        #print("checking if images updated...")
        #for image in check_images:
        #    print(f"image_path: {image[2]}")
        #    print(f"filename: {image[3]}")

        db.commit()
        cur.close()
    except Exception as e:
        print("Could not update the image db with new project info")
        print(e)
        return False

