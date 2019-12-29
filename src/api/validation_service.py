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

        return binascii.hexlify(salt), binascii.hexlify(password_hash)

    @classmethod
    def validate_hash(cls, input_password: str, password: str, salt: str) -> bool:
        """Return boolean comparison of input password and passed value"""

        salt = binascii.unhexlify(salt)
        password_hash = hashlib.pbkdf2_hmac("sha512", input_password.encode("utf-8"), salt, 100000)

        return hmac.compare_digest(password, binascii.hexlify(password_hash))

