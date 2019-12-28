# dependencies
import binascii, hashlib, os
import psycopg2 as psycopg

# LOCAL
from models import User
from settings import HOST, PSQL_DATABASE, PSQL_USER, PSQL_PASSWORD

class UserController:

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
    @staticmethod
    def registration(email: str, password: str):
        connection = None
        try:
            connection = psycopg.connect(host=HOST, database=PSQL_DATABASE, user=PSQL_USER, password=PSQL_PASSWORD)

            if connection.is_connected():
                cursor = connection.cursor()

                hashedPassword, salt = hash(password)

                cursor.execute(f"INSERT INTO UserTable(email) VALUES('{email}');")
                cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id FROM UserTable WHERE email='{email}'), '{hashedPassword}', '{salt}');")
                
                cursor.close()
                connection.commit()
        except psycopg.DatabaseError as error:
            return error
        finally:
            if(connection is not None):
                connection.close()

            return "User successfully created"

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
    def __hash(self, password: str):
        salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
        hashedValue = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 10000)

        return (salt + binascii.hexlify(hashedValue)), salt

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
