
from flask import g
from flask_httpauth import HTTPBasicAuth
from project.models.auth_model import User

auth = HTTPBasicAuth()


# Verifies credentials
@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query_filtered_by(email=email_or_token)[0]
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
