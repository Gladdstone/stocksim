# dependencies
import binascii, hashlib, os, traceback
import psycopg2 as psycopg

# LOCAL
from models import User
from settings import HOST, PORT, PSQL_DATABASE, PSQL_USER, PSQL_PASSWORD

class UserController:

    conn_config = {
        'host': HOST,
        'dbname': PSQL_DATABASE,
        'user': PSQL_USER,
        'password': PSQL_PASSWORD,
        'port': PORT
    }

    @staticmethod
    def findByEmail(email: str) -> User:
        connection = None
        user = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE email='{email}';")
            row = cursor.fetchone()

            if(row is None):
                return None

            user = User.User(row[0], row[1])

            cursor.close()

        except psycopg.DatabaseError as error:
            print(error)
            return None
        finally:
            if(connection is not None):
                connection.close()
            return user

    # Add balance to user account
    @staticmethod
    def addBalance(user_id: int, amount: float):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()

            cursor.execute(f"SELECT balance FROM UserTable WHERE id={user_id};")
            row = cursor.fetchone()
            print("addBalance")
            print(row)

            newBalance = row[0] + amount
            cursor.execute(f"UPDATE UserTable SET balance={newBalance} WHERE id={user_id};")
            # TODO - this could be turned into a MySQL procedure
            cursor.execute(f"INSERT INTO UserBalanceHistory (user_id, balance) VALUES({user_id}, {newBalance});")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close
            return {"message": "Add balance successful"}

    # Subtract balance from user account
    @staticmethod
    def subtractBalance(user_id: int, amount: float):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()
            cursor.execute(f"SELECT balance FROM UserTable WHERE id={user_id};")
            row = cursor.fetchone()
            print("subtractBalance")
            print(row)

            newBalance = row[0] - amount
            # TODO - where/how do we want to handle overdrawing?
            cursor.execute(f"UPDATE UserTable SET balance={newBalance};")
            # TODO
            cursor.execute(f"INSERT INTO UserBalanceHistory (user_id, balance) VALUES({user_id}, {newBalance});")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return {"message": "Subtract balance successful"}

    @staticmethod
    def getUserBalanceHistory(user_id):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()

            cursor.execute(f"SELECT balance FROM UserBalanceHistory WHERE user_id={user_id};")
            history = cursor.fetchall()

            cursor.close()
        except psycopg.DatabaseError as error:
            return {"message": "Something went wrong"}
        finally:
            if(connection is not None):
                connection.close()
            return history


    # Adds a new User to the database
    @classmethod
    def registration(cls, email: str, password: str) -> str:
        connection = None
        try:
            connection = psycopg.connect(host=HOST, port=PORT, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            print(f"REGISTRATION: connection established at: {HOST}:{PORT}")

            cursor = connection.cursor()

            salt, password_hash = cls.__hash(password)

            cursor.execute(f"INSERT INTO UserTable(email) VALUES('{email}');")
            cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id FROM UserTable WHERE email='{email}'), {psycopg.Binary(password_hash)}, {psycopg.Binary(salt)});")
            
            connection.commit()
            cursor.close()
        except psycopg.OperationalError as error:
            connection.rollback()
            print(f"REGISTRATION: unable to establish connection at: {HOST}:{PORT}")
            print(traceback.format_exc())
            return "Unable to establish connection"     # TODO - raise a custom exception
        except psycopg.Error as error:
            connection.rollback()
            print(f"REGISTRATION: {error.pgcode} - {error.pgerror}")
            raise
        except:
            connection.rollback()
            print(f"REGISTRATION: unknown failure")
            print(traceback.format_exc())
            return "Unable to complete registration"    # TODO - raise a custom exception

        if(connection is not None):
            connection.close()
            return "User successfully created"

        return ""

    # Marks existing user as archived
    @staticmethod
    def archive(user_id: int):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE id={user_id};")
            row = cursor.fetchone()
            print("archive")
            print(row)

            if(row is not None):
                return {"Error": "Unable to archive user: does note exist"} #TODO

            cursor.execute(f"UPDATE UserData SET archived=TRUE WHERE id={userID};")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
            return {"Error": "Unable to archive user"}  #TODO
        finally:
            if(connection is not None):
                connection.close()
            return {"message": "User successfully archived"}    # TODO

    # secure password with sha512
    @classmethod
    def __hash(cls, password: str) -> (bytes, bytes):
        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        password_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)

        return cls.__hex_encode(salt), cls.__hex_encode(password_hash)

    @staticmethod
    def __hex_encode(value: str) -> bytes:
        return "0x".encode("ascii") + binascii.hexlify(value)

    @staticmethod
    def login(username: str, password: str):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            if connection.is_connected():
                cursor = connection.cursor()

                cursor.execute(f"SELECT * FROM UserTable WHERE username='{username}';")  ### Missing an f before query??
                row = cursor.fetchone()

                if(row is None):
                    return False

                # validate the password with salt
                cursor.execute(f"SELECT password, salt FROM LoginData WHERE user_id = {row[0]};")
                row = cursor.fetchone()
                dbPassword = row[0]
                salt = row[1]

                cursor.close()
                if(password == salt + dbPassword):
                    user = User.User(row[0], username)
                    user.authenticate()
                    return True

            return False
        except psycopg.DatabaseError as error:
            print(error)
            return False

    # separate function
    @staticmethod
    def validate_login(user: User, user_id: str, password: str):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)
            if connection.is_connected():
                cursor = connection.cursor()

                # get the salt and password
                cursor.execute(f"SELECT password, salt FROM LoginData WHERE user_id = {user_id}")
                row = cursor.fetchone()

                dbPassword = row[0]
                salt = row[1]

                hashedPassword, salt = hash(password)
                hashedPassword = salt + hashedPassword

                if(hashedPassword == salt + dbPassword):
                    user.authenticate()
                    return True

            return False
        except psycopg.DatabaseError as error:
            print(error)
            return False


    @staticmethod
    def logout(user: User, tokenId: str):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE id={tokenId};")
            row = cursor.fetchone()
            print("logout")
            print(row)

            if(row is None):
                return False

            cursor.execute(f"INSERT INTO RevokedTokens(jti) VALUES({tokenId});")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
            return False
        finally:
            if(connection is not None):
                connection.close()
            return True

    @staticmethod
    def tokenIsBlacklisted(jti: str):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM RevokedTokens WHERE jti={jti};")
            row = cursor.fetchone()
            print("tokenIsBlacklisted")
            print(row)

            if(row is not None):
                return True

            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
            return True
        finally:
            if(connection is not None):
                connection.close()
            return False
