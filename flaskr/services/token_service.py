from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_confirmation_token(email):
    """generates unique token"""
    serializer = URLSafeTimedSerializer(current_app.app_context().app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.app_context().app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=86400): # 24 hrs
    """confirms the token sent back"""
    serializer = URLSafeTimedSerializer(current_app.app_context().app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.app_context().app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        #return True
    except Exception as e:
        print(e)
        return False

    return email
