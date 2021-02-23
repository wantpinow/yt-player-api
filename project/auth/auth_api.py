from flask import Flask, Blueprint, request, current_app
from flask_restful import Api, Resource, url_for, fields, reqparse
import project.models as models
from project import db
import project.auth.auth_util as auth_util

### https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/

# Create API Blueprint
app = Flask(__name__)
auth_blueprint = Blueprint('auth', __name__,
                              url_prefix="/auth")
api = Api(auth_blueprint)


# Register User API
register_user_parser = reqparse.RequestParser()
register_user_parser.add_argument('username')
register_user_parser.add_argument('password')
class RegisterUser(Resource):
    def post(self):
        args = register_user_parser.parse_args()
        return auth_util.register_user(
            args,
            dump_schema=True)


# Login User API
login_user_parser = reqparse.RequestParser()
login_user_parser.add_argument('username')
login_user_parser.add_argument('password')
class LoginUser(Resource):
    def post(self):
        args = login_user_parser.parse_args()
        login_token = auth_util.login_user(args)
        if auth_util.login_user(args):
            return login_token, 200
        else:
            return { 'message': 'Invalid credentials', 'authenticated': False }, 401 


class TestLoggedIn(Resource):
    @auth_util.token_required
    def get(self, user):
        return "SUCCESS!!"

class TestFoo(Resource):
    def get(self):
        return "Another Test 1234"

# Define Endpoints
api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')
api.add_resource(TestLoggedIn, '/test_logged_in')
api.add_resource(TestFoo, '/test')


