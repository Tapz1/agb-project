import logging
import traceback

from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, redirect, flash, request, session, current_app, url_for


@DecoratorWraps.only_whenNotLoggedIn
def login():
    logging.debug("logging in")
    dev_email = current_app.app_context().app.config['DEV_EMAIL']
    client_email = current_app.app_context().app.config['CLIENT_EMAIL']
    admin_password = current_app.app_context().app.config['ADMIN_PASSWORD']

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if password == admin_password and (email.lower() == client_email or email.lower() == dev_email):
            session['logged_in'] = True
            session['email'] = email
            flash('You are now logged in', 'success')
            return redirect(url_for("blueprint.admin_portal"))
        else:
            error = 'Invalid login'
            logging.error(f"{error}")
            flash(error, "danger")
            return render_template('login.html')

    return render_template('login.html', title='Login')


def logout():
    logging.debug("logging out")
    try:
        session.clear()
        flash("You are logged out!", "success")

    except Exception as e:
        error = "Something went wrong"
        logging.error(f"{error}: {e}\n{traceback.format_exception(None, e, e.__traceback__)}")
        flash(error, "danger")
        return render_template("index.html")

    return redirect(request.referrer)
