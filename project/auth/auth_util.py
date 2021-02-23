from project import db
import project.models as models
from flask import jsonify, current_app, request
from datetime import datetime, timedelta
from functools import wraps
import jwt
import sqlalchemy


# Get all schemas from models.py
user_schema = models.UserSchema()


# User API helper functions
def get_user(user_id, dump_schema=False):
    user = models.User.query.filter_by(id=user_id).first()
    return user_schema.dump(user) if dump_schema else user

def get_all_users(dump_schema=False):
    users = models.User.query.all()
    return [user_schema.dump(user) for user in users] if dump_schema else user

def register_user(args, dump_schema=False):
    try:
        new_user = models.User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        return get_user(new_user.id, dump_schema=dump_schema), 200
    except sqlalchemy.exc.IntegrityError:
        return {
            'message': 'Error. Username already exists.'
        }, 400
    except Exception as e:
        return {
            'message': 'Unknown Error. Could not register user.',
            'error': e
        }, 500

def login_user(args):
    username = args['username']
    password = args['password']
    user = models.User.authenticate(username=username, password=password)

    if not user:
        return False

    token = jwt.encode({
        'sub': user.username,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])

    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return { 'token': token, 'user': get_user(user.id, dump_schema=True)}

# Decorator functions
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registration / authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        user_not_found_msg = {
            'message': 'Invalid token. User not found.',
            'authenticated': False
        }
        if len(auth_headers) != 2:
            return invalid_msg, 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = models.User.query.filter_by(username=data['sub']).first()
            if not user:
                return user_not_found_msg, 401
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            print(e, "ex")
            return expired_msg, 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e, "iv")
            return invalid_msg, 401

    return _verify