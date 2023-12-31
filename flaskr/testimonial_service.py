from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_testimonial(testimonial_id, name, email, message, town):
    db = get_db_connection()

    cur = db.cursor()
    insert_sql = "INSERT INTO testimonials (testimonial_id, name, email, message, town) " \
                 "VALUES(:testimonial_id, :name, :email, :message, :town)"
    cur.execute(insert_sql, {'testimonial_id': testimonial_id, 'name': name, 'email': email, 'message': message, 'town': town})

    db.commit()
    cur.close()


def get_all_approved():
    db = get_db_connection()

    cur = db.cursor()
    testimonials = list(cur.execute(
        "SELECT * FROM testimonials WHERE is_approved = TRUE ORDER BY created desc").fetchall())

    cur.close()
    # conn.close() # can't close connection since need to run paginate_approved

    return testimonials


def paginate_approved(limit, offset):
    db = get_db_connection()

    cur = db.cursor()
    testimonials = list(cur.execute(
        "SELECT * FROM testimonials WHERE is_approved = TRUE ORDER BY created desc LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall())

    cur.close()
    db.close()

    return testimonials


def get_limited_approved(limit):
    """for home page highlights"""
    db = get_db_connection()
    cur = db.cursor()

    testimonials = list(cur.execute(
        "SELECT name, message, town FROM testimonials WHERE is_approved = TRUE ORDER BY created asc LIMIT ?", [limit]).fetchall())
    cur.close()
    db.close()

    return testimonials


def get_all_pending():
    db = get_db_connection()
    cur = db.cursor()

    pending_testimonials = list(cur.execute("SELECT * FROM testimonials WHERE is_approved = FALSE").fetchall())
    cur.close()
    #conn.close()

    return pending_testimonials


def update_approval(testimonial_id):
    db = get_db_connection()
    cur = db.cursor()

    cur.execute("UPDATE testimonials SET is_approved = 1 WHERE testimonial_id = ?", [testimonial_id])
    db.commit()

    cur.close()
    db.close()
    return


def delete_entry(testimonial_id):
    db = get_db_connection()
    cur = db.cursor()

    cur.execute("DELETE FROM testimonials WHERE testimonial_id = ?", [testimonial_id])
    db.commit()

    cur.close()
    db.close()
    return


def add_project_id(project_id, testimonial_id):
    db = get_db_connection()
    cur = db.cursor()

    cur.execute("UPDATE testimonials SET project_id = ? WHERE testimonial_id = ?", (project_id, testimonial_id))
    db.commit()

    cur.close()

    return


def get_testimonial_id_by_email(email):
    db = get_db_connection()

    cur = db.cursor()

    testimonial_id = list(cur.execute("SELECT testimonial_id FROM testimonials WHERE email = ?", [email]).fetchone())

    cur.close()

    return testimonial_id[0]
