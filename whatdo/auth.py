import google.auth.transport.requests
import google.oauth2.id_token


def read_google_token(token, client_id):
    try:
        idinfo = google.oauth2.id_token.verify_oauth2_token(
            token, google.auth.transport.requests.Request(), client_id)
    except ValueError:
        return None  # Invalid token
    valid_iss = {'accounts.google.com', 'https://accounts.google.com'}
    if idinfo['iss'] not in valid_iss:
        return None  # Invalid issuer
    return idinfo


class GoogleUser:

    def __init__(self, idinfo):
        self.id = idinfo['sub']
        self.email = idinfo.get('email')
        self.email_verified = idinfo.get('email_verified')
        self.name = idinfo.get('name')
        self.picture = idinfo.get('picture')
        self.given_name = idinfo.get('given_name')
        self.family_name = idinfo.get('family_name')
        self.locale = idinfo.get('locale')

    @classmethod
    def from_token(cls, token, client_id):
        idinfo = read_google_token(token, client_id)
        if not idinfo:
            raise ValueError('Invalid token')
        return cls(idinfo)
