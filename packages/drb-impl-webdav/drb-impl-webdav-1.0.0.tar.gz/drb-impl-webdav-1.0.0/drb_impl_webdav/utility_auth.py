from requests.auth import AuthBase


class CertAuth(AuthBase):

    def __init__(self, username: str,
                 password: str,
                 cert_path: str,
                 key_path: str
                 ):
        self.username = username
        self.password = password
        self.cert_path = cert_path
        self.key_path = key_path


class TokenAuth(AuthBase):

    def __init__(self, token: str):
        self.token = token
