import binascii, hashlib, hmac, os

class ValidationService():

    # secure password with sha512
    @classmethod
    def __hash(cls, password: str) -> (bytes, bytes):
        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        password_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)

        return cls.__hex_encode(salt), cls.__hex_encode(password_hash)

    @staticmethod
    def __validate_hash(input_password: str, password: str, salt: str) -> bool:
        return hmac.compare_digest(password,
            hashlib.pbkdf2_hmac("sha512", input_password.encode("utf-8"), salt, 100000))

    @staticmethod
    def __hex_encode(value: str) -> bytes:
        return "0x".encode("ascii") + binascii.hexlify(value)