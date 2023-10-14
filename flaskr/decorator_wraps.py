from flask import session, flash, redirect, url_for
from functools import wraps


class DecoratorWraps():

    def is_logged_in(f):
        """checks if user logged in"""

        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('Not authorized', 'danger')
                return redirect(url_for('blueprint.home'))

        return wrap

    def only_whenNotLoggedIn(f):
        """only allows access if user isn't logged in"""
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' not in session:
                return f(*args, **kwargs)
            else:
                flash("You're already logged in!", 'danger')
                return redirect(url_for('blueprint.home'))
        return wrap
