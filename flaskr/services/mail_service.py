from flask_mail import Message, Mail
from flask import current_app, render_template, url_for
from flaskr.services.token_service import generate_confirmation_token


def send_email(msg):
    try:
        mail = Mail(current_app.app_context().app)
        mail.send(msg)
        print("success")
        return 'Your message has been sent!'
    except Exception as e:
        print(e)
        return "Your message was not able to send."


class MailService(object):
    """docstring for MailService."""

    # load_dotenv()

    def __init__(self):
        super(MailService, self).__init__()
        self.EMAIL_FROM = current_app.app_context().app.config['MAIL_USERNAME']
        self.TO_EMAIL = current_app.app_context().app.config['TO_EMAIL']
        self.SEND_AS_EMAIL = current_app.app_context().app.config['MAIL_DEFAULT_SENDER']

    def send_testimonial_request(self, email):
        token = generate_confirmation_token(email)
        matching_url = url_for("blueprint.testimonial_form", token=token, _external=True)

        email_subject = "Brandon is requesting to post your experience!"
        email_body = render_template("testimonial_request.html", matching_url=matching_url)
        msg = Message(
            subject=email_subject,
            sender=self.SEND_AS_EMAIL,
            recipients=[email],
            html=email_body
        )

        send_email(msg)
        return

    def send_testimonial_email(self, name, email, message, town):
        email_subject = "You have a new testimonial!"
        email_body = render_template("testimonial_email.html", name=name, email=email, message=message,
                                     town=town, url=url_for("blueprint.login", _external=True))
        msg = Message(
            subject=email_subject,
            sender=self.SEND_AS_EMAIL,
            recipients=[self.TO_EMAIL],
            html=email_body
        )

        send_email(msg)
        return

    def testimonial_receipt(self, name, email, message, town):
        email_subject = "You're testimonial has been received!"
        email_body = render_template("testimonial_email_receipt.html", name=name, email=email, message=message,
                                     town=town, url=url_for("blueprint.home", _external=True))

        msg = Message(
            subject=email_subject,
            sender=self.SEND_AS_EMAIL,
            recipients=[email],
            html=email_body
        )

        send_email(msg)
        return
