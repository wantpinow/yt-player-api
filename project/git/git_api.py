from flask import Flask, Blueprint, request, abort, current_app
from flask_restful import Api, Resource
import project.git.git_util as git_util
import git
import json

### https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/

# Create API Blueprint
app = Flask(__name__)
git_blueprint = Blueprint('git', __name__,
                              url_prefix="/git")
api = Api(git_blueprint)

# Update Server API
class UpdateServer(Resource):
    def post(self):
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)
        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)
        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)
        if not request.is_json:
            abort(abort_code)
        if 'User-Agent' not in request.headers:
            abort(abort_code)
        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)

        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not git_util.is_valid_signature(x_hub_signature, request.data, current_app.config['GITHUB_WEBHOOK_SECRET']):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/main':
            return json.dumps({'msg': 'Not main; ignoring'})

        repo = git.Repo('')
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')
        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)

        # try:
        #     repo = git.Repo('')
        #     origin = repo.remotes.origin
        #     origin.pull()
        #     return "Success", 200
        # except Exception as e:
        #     return "Error: " + str(e), 400

# Define UpdateServer
api.add_resource(UpdateServer, '/update_server')


