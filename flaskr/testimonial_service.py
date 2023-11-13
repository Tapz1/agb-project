from flaskr.db import get_db


def get_db_connection():
    db = get_db()
    return db


def add_testimonial(name, email, message, town):
    conn = get_db_connection()

    cur = conn.cursor()
    insert_sql = "INSERT INTO testimonials (name, email, message, town) " \
                 "VALUES(:name, :email, :message, :town)"
    cur.execute(insert_sql, {'name': name, 'email': email, 'message': message, 'town': town})

    conn.commit()
    cur.close()
    conn.close()


def get_all_approved():
    conn = get_db_connection()

    cur = conn.cursor()
    testimonials = list(cur.execute(
        "SELECT * FROM testimonials WHERE is_approved = TRUE ORDER BY created desc").fetchall())

    cur.close()
    # conn.close() # can't close connection since need to run paginate_approved

    return testimonials


def paginate_approved(limit, offset):
    conn = get_db_connection()

    cur = conn.cursor()
    testimonials = list(cur.execute(
        "SELECT * FROM testimonials WHERE is_approved = TRUE ORDER BY created desc LIMIT ? OFFSET ?",
        (limit, offset)
    ).fetchall())

    cur.close()
    conn.close()

    return testimonials


def get_limited_approved():
    """for home page highlights"""
    conn = get_db_connection()
    cur = conn.cursor()

    testimonials = list(cur.execute(
        "SELECT name, message, town FROM testimonials WHERE is_approved = TRUE ORDER BY created asc LIMIT 2").fetchall())
    cur.close()
    conn.close()

    return testimonials


def get_all_pending():
    conn = get_db_connection()
    cur = conn.cursor()

    pending_testimonials = list(cur.execute("SELECT * FROM testimonials WHERE is_approved = FALSE").fetchall())
    cur.close()
    #conn.close()

    return pending_testimonials


def update_approval(testimonial_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE testimonials SET is_approved = 1 WHERE testimonial_id = ?", [testimonial_id])
    conn.commit()

    cur.close()
    conn.close()
    return


def delete_entry(testimonial_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM testimonials WHERE testimonial_id = ?", [testimonial_id])
    conn.commit()

    cur.close()
    conn.close()
    return


def add_project_id(project_id, testimonial_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE testimonials SET project_id = ? WHERE testimonial_id = ?", (project_id, testimonial_id))
    conn.commit()

    cur.close()
    conn.close()
    return


def get_testimonial_id_by_email(email):
    conn = get_db_connection()

    cur = conn.cursor()
    testimonials = list(cur.execute(
        "SELECT * FROM testimonials WHERE email = ?", [email]).fetchall())

    cur.close()
    # conn.close() # can't close connection since need to run paginate_approved

    return testimonials
