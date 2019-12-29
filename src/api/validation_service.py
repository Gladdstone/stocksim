"""
Handles validation services.
Performs new password hashing and hash validation.

hash(str) -> (bytes, bytes)
validate_hash(str, str, str) -> bool
"""

import binascii
import hashlib
import hmac
import os

class ValidationService():

    @classmethod
    def hash(cls, password: str) -> (bytes, bytes):
        """secure password with sha512
        Return salt and hashed password as tuple
        """

        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        password_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)

        return cls.__hex_encode(salt), cls.__hex_encode(password_hash)

    @staticmethod
    def validate_hash(input_password: str, password: str, salt: str) -> bool:
        """Return boolean comparison of input password and passed value"""

        return hmac.compare_digest(password, hashlib.pbkdf2_hmac("sha512", input_password.encode("utf-8"), salt, 100000))

    @staticmethod
    def __hex_encode(value: str) -> bytes:
        """Return hex encoding of string value"""

        return "0x".encode("ascii") + binascii.hexlify(value)
