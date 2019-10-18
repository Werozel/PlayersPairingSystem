import hashlib, binascii
from constants.config import salt


def hash(s: str):
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', str.encode(s), str.encode(salt), 2**17)).decode()
