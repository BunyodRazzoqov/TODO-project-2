import bcrypt


from typing import Optional


class Response:
    def __init__(self, data: str, status_code: int):
        self.data = data
        self.status_code = status_code


def hash_password(raw_password: Optional[str] = None):
    assert raw_password, 'Raw password cannot be none'
    raw_password = raw_password.encode()
    return bcrypt.hashpw(raw_password, salt=bcrypt.gensalt(4)).decode()


def match_password(raw_password: Optional[str] = None,
                   encoded_password: Optional[str] = None):
    assert raw_password, 'Raw password cannot be none'
    assert encoded_password, 'Encoded password cannot be none'
    return bcrypt.checkpw(raw_password.encode(), encoded_password.encode())

