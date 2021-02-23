from flask import Flask, Blueprint, request
from flask_restful import Api, Resource, url_for, fields, reqparse
import project.models as models
from project import db
import project.content.content_util as content_util
import project.content.youtube_util as youtube_util

# Create API Blueprint
app = Flask(__name__)
content_blueprint = Blueprint('content', __name__,
                              url_prefix="/content")
api = Api(content_blueprint)


# User API
class GetUser(Resource):
    def get(self, user_id):
        return content_util.get_user(user_id, dump_schema=True)


class GetAllUsers(Resource):
    def get(self):
        return content_util.get_all_users(dump_schema=True)


new_user_parser = reqparse.RequestParser()
new_user_parser.add_argument('name')


class AddUser(Resource):
    def post(self):
        args = new_user_parser.parse_args()
        return content_util.add_user(
            args,
            dump_schema=True)


# Video API
class GetVideo(Resource):
    def get(self, video_id):
        return content_util.get_video(video_id, dump_schema=True)


class GetAllVideos(Resource):
    def get(self):
        return content_util.get_all_videos(dump_schema=True)


new_video_parser = reqparse.RequestParser()
new_video_parser.add_argument('title')
new_video_parser.add_argument('author')
new_video_parser.add_argument('url')
new_video_parser.add_argument('thumbnail_url')
new_video_parser.add_argument('user_id')
new_video_parser.add_argument('youtube_id')

class AddVideo(Resource):
    def post(self):
        args = new_video_parser.parse_args()
        return content_util.add_video(
            args,
            dump_schema=True)

class GetYouTubeMetadata(Resource):
    def get(self, youtube_id):
        return youtube_util.get_video_metadata(youtube_id)

# Define Endpoints
api.add_resource(GetUser, '/user/<int:user_id>')
api.add_resource(GetAllUsers, '/users')
api.add_resource(AddUser, '/user')

api.add_resource(GetVideo, '/video/<int:video_id>')
api.add_resource(GetAllVideos, '/videos')
api.add_resource(AddVideo, '/video')

api.add_resource(GetYouTubeMetadata, '/video/metadata/<string:youtube_id>')