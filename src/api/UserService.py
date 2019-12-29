from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import json

# LOCAL
from controllers.UserController import UserController
from models import User

parser = reqparse.RequestParser()
parser.add_argument("username", help="This field cannot be blank", required=False)
parser.add_argument("password", help="This field cannot be blank", required=False)
parser.add_argument("email", help="This field can be blank", required=False)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()["credentials"]
        email = data["email"]
        password = data["password"]
        
        userController = UserController()

        # validate that user email doesn't already exist
        if(userController.findByEmail(email) != None):
            return {"error": f"User {email} already exists"}

        try:
            message = userController.registration(email, password)
            access_token = create_access_token(identity = email)
            refresh_token = create_refresh_token(identity = email)

            if(message != "") :
                return {
                    "message": message,
                    "user": email,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }

        except:
            return {"error": "Something went wrong"}

        return {"error": "Something went wrong"}

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        userController = UserController()

        try:
            if (userController.findByEmail(email)) == None:
                return {"message": f"User {email} doesn't exist"}

            if userController.login(email, password) == True:
                access_token = create_access_token(identity = email)
                refresh_token = create_refresh_token(identity = email)

                return {
                    "message": f"Logged in as {email}",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            else:
                return {"message": "Username or password is incorrect."}

        except:
            return {"message": "Something went wrong, please try again"}

class UserInfo(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        userController = UserController()
        user_info = userController.findByUsername(data["username"])
        return user_info.__dict__

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        return {"message": "User logout access"}

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):

        return {"message": "User logout refresh"}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity = user)
        return {"access_token": access_token}

class GetBalanceHistory(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        userController = UserController()

        user = userController.findByUsername(data["username"])
        history = userController.getUserBalanceHistory(user.getUserId)

        return history
