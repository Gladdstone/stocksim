# dependencies
import traceback
import psycopg2 as psycopg

# LOCAL
from models.User import User
from api.validation_service import ValidationService
from settings import ENV, HOST, PORT, PSQL_DATABASE, PSQL_USER, PSQL_PASSWORD

class UserController:

    conn_config = (f"host={HOST} port={PORT} dbname={PSQL_DATABASE} user={PSQL_USER} password={PSQL_PASSWORD}")

    @classmethod
    def findByEmail(cls, email: str) -> User:
        connection = None
        user = None
        try:
            connection = psycopg.connect(cls.conn_config)
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE email='{email}';")
            row = cursor.fetchone()

            if(row is None):
                return None

            user = User(row[0], row[1])

            cursor.close()
        except psycopg.OperationalError as error:
            if(ENV == "development"):
                print(f"FIND_BY_EMAIL: unable to establish connection at: {HOST}:{PORT}")
                print(traceback.format_exc())
            raise ConnectionError
        except psycopg.Error as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"FIND_BY_EMAIL: {error.pgcode} - {error.pgerror}")
            raise
        except Exception as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"FIND_BY_EMAIL: unknown failure")
                print(traceback.format_exc())
            raise

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
            connection = psycopg.connect(cls.conn_config)

            print(f"REGISTRATION: connection established at: {HOST}:{PORT}")

            cursor = connection.cursor()
            vs = ValidationService()

            salt, password_hash = vs.__hash(password)

            cursor.execute(f"INSERT INTO UserTable(email) VALUES('{email}');")
            cursor.execute(f"INSERT INTO LoginData(user_id, password, salt) VALUES((SELECT id FROM UserTable WHERE email='{email}'), {psycopg.Binary(password_hash)}, {psycopg.Binary(salt)});")
            
            connection.commit()
            cursor.close()
        except psycopg.OperationalError as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"REGISTRATION: unable to establish connection at: {HOST}:{PORT}")
                print(traceback.format_exc())
            raise ConnectionError
        except psycopg.Error as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"REGISTRATION: {error.pgcode} - {error.pgerror}")
            raise
        except Exception as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"REGISTRATION: unknown failure")
                print(traceback.format_exc())
            raise

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

            cursor.execute(f"UPDATE UserData SET archived=TRUE WHERE id={user_id};")

            connection.commit()
            cursor.close()
        except psycopg.DatabaseError as error:
            print(error)
            return {"Error": "Unable to archive user"}  #TODO
        finally:
            if(connection is not None):
                connection.close()
            return {"message": "User successfully archived"}    # TODO

    """Logs in user
    Calls hash validation function and creates a new authenticated user object on success
    """
    @classmethod
    def login(cls, email: str, password: str) -> bool:
        connection = None
        try:
            connection = psycopg.connect(cls.conn_config)

            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM UserTable WHERE email='{email}';")
            row = cursor.fetchone()

            if(row is None):
                return False

            # validate the password with salt
            cursor.execute(f"SELECT password, salt FROM LoginData WHERE user_id={row[0]};")
            row = cursor.fetchone()
            dbPassword = row[0]
            salt = row[1]

            cursor.close()

            vs = ValidationService()

            if(vs.__validate_hash(password, dbPassword, salt)):
                user = User(row[0], email)
                user.authenticate()
                return True
            
        except psycopg.OperationalError as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"LOGIN: unable to establish connection at: {HOST}:{PORT}")
                print(traceback.format_exc())
            raise ConnectionError
        except psycopg.Error as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"LOGIN: {error.pgcode} - {error.pgerror}")
            raise
        except Exception as error:
            connection.rollback()
            if(ENV == "development"):
                print(f"LOGIN: unknown failure")
                print(traceback.format_exc())
            raise

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
