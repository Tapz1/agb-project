
from flask import render_template, redirect, flash, url_for, request, session, current_app


def gallery():
    session.modified = True


    return render_template("gallery.html")
