from jose import jwt
from datetime import datetime
from calendar import timegm

class InvalidTokenError(Exception):
    """Raised when the token is invalid"""
    pass

class JWT:
    def __init__(self, secret, expiredInSeconds = None):
        self.secret = secret
        self.expiredInSeconds = expiredInSeconds or 86400

    def create_token(self, session):
        # expiry_time = round(time.time()) + self.expiredInSeconds
        expiry_time = timegm(datetime.utcnow().utctimetuple()) + self.expiredInSeconds
        session['exp'] = expiry_time
        return jwt.encode(session, self.secret, algorithm='HS256')

    def session(self, token):
        try: 
            return jwt.decode(token, self.secret, algorithms=['HS256'])
        except (jwt.JWTError, jwt.ExpiredSignatureError, jwt.JWTClaimsError):
            raise InvalidTokenError
