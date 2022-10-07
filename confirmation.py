from itsdangerous import URLSafeTimedSerializer
import os

EMAIL_VERIFICATION_SALT = "rT9djSALTkkSo"
PASSWORD_RECOVERY_SALT = "hfjfJfhf786Jkd00"
SECRET = os.environ.get('SECRET_KEY')

def generate_confirmation_token(email, type="EMAIL_VERIFICATION"):
    serializer = URLSafeTimedSerializer(SECRET)
    salt = EMAIL_VERIFICATION_SALT
    if type == "PASSWORD_RECOVERY": salt = PASSWORD_RECOVERY_SALT
    return serializer.dumps(email, salt=salt)

def confirm_token(token, type="EMAIL_VERIFICATION", expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET)
    salt = EMAIL_VERIFICATION_SALT
    if type == "PASSWORD_RECOVERY": salt = PASSWORD_RECOVERY_SALT
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return False
    return email
