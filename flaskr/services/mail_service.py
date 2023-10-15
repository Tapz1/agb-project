from flask_mail import Message, Mail
from flask import current_app, render_template, url_for
from flaskr.services.token_service import generate_confirmation_token

EMAIL_FROM = current_app.app_context().app.config['MAIL_USERNAME']
TO_EMAIL = current_app.app_context().app.config['TO_EMAIL']
SEND_AS_EMAIL = current_app.app_context().app.config['MAIL_DEFAULT_SENDER']


def send_email(msg):
    try:
        mail = Mail(current_app.app_context().app)
        mail.send(msg)
        print("success")
        return 'Your message has been sent!'
    except Exception as e:
        print(e)
        return "Your message was not able to send."


def send_testimonial_request( email):
    token = generate_confirmation_token(email)
    matching_url = url_for("blueprint.testimonial_form", token=token, _external=True)

    email_subject = "Brandon is requesting to post your experience!"
    email_body = render_template("testimonial_request.html", matching_url=matching_url)
    msg = Message(
        subject=email_subject,
        sender=SEND_AS_EMAIL,
        recipients=[email],
        html=email_body
    )

    send_email(msg)
    return

