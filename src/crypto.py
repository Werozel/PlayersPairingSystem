import binascii
import hashlib

from constants.config import salt1, salt2


def hash_password(s: str):
    tmp: str = binascii.hexlify(hashlib.pbkdf2_hmac('md5', str.encode(s), str.encode(salt1), 2**16)).decode()
    return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', str.encode(tmp), str.encode(salt2), 2**16)).decode()
