from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email, secret,  salt):
    serializer = URLSafeTimedSerializer(secret)
    return serializer.dumps(email, salt=salt)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret)
    try:
        email = serializer.loads(
            token,
            salt=salt,
            max_age=expiration
        )
    except:
        return False
    return email
