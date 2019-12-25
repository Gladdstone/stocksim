#!/usr/bin/env python
"""
Entry point for stocksim api
"""
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from guppy import hpy

# Local
from api import UserService, StockService
from controllers.UserController import UserController
from settings import JWT_SECRET_KEY

# api urls
LOCAL_URL = 'http://localhost:5000'
API_LOGIN = '/login/submit'
API_REGISTER = '/registration'
API_WATCHLIST_ADD = "/watch/add"
API_WATCHLIST_REMOVE = "/watch/remove"
API_REFRESH = "/token/refresh"
API_LOGOUT = "/logout/access"
API_LOGOUT_REFRESH = "/logout/refresh"
API_STOCK_PURCHASE_SELL = "/stock/purchase"
API_STOCK = "/stock"
API_USER_INFO = "/user/info"
ACCESS_COOKIE = 'user_access'
REFRESH_COOKIE = 'user_refresh'
USER_COOKIE = 'user_info'

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

blacklist = set()
jwt = JWTManager(app)
api = Api(app)

# guppy
h = hpy()
print(h.heap())

# called every time client tries to access a secure endpoint
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return UserController.tokenIsBlacklisted(jti)


# User Service
api.add_resource(UserService.UserRegistration, API_REGISTER)
api.add_resource(UserService.UserLogin, API_LOGIN)
api.add_resource(UserService.UserLogoutAccess, API_LOGOUT)
api.add_resource(UserService.UserLogoutRefresh, API_LOGOUT_REFRESH)
api.add_resource(UserService.TokenRefresh, API_REFRESH)
api.add_resource(UserService.UserInfo, API_USER_INFO)
# Stock Service
api.add_resource(StockService.GetStock, API_STOCK)
api.add_resource(StockService.PurchaseAsset, API_STOCK_PURCHASE_SELL)
api.add_resource(StockService.WatchAsset, API_WATCHLIST_ADD)
api.add_resource(StockService.RemoveWatchedAsset, API_WATCHLIST_REMOVE)

if __name__ == "__main__":
    # app.run(host='0.0.0.0')    # Dockerized
    app.run(debug=True)    # Debug
