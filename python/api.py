#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
import scrypt

app = Flask(__name__)
api = Api(app)

# DO NOT USE IN PRODUCTION
from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
# DO NOT USE IN PRODUCTION

SECRET = "N\x8a!Mj#JHjrIW)eBmJ"

ROBOTS = {
    'robot1': {'name': 'R2-D2'},
    'robot2': {'name': 'Wall-E'},
    'robot3': {'name': 'Chappy'},
}

def hash_password(password):
    return scrypt.hash(password, SECRET)

USERS = {
    'stan' : hash_password('robotz')
}

def check_auth():
    auth = request.authorization
    if auth and auth.username in USERS and \
       hash_password(auth.password) == USERS[auth.username]:
        return (True, None)
    else:
        r = Response('Could not verify your access level for that URL.\n'
                     'You have to login with proper credentials', 401,
                     {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return (False, r)

def abort_if_robot_doesnt_exist(robot_id):
    if robot_id not in ROBOTS:
        abort(404, message="Robot {} doesn't exist".format(robot_id))

parser = reqparse.RequestParser()
parser.add_argument('name')


# Robot
# shows a single robot item and lets you delete a robot item
class Robot(Resource):
    def get(self, robot_id):
        abort_if_robot_doesnt_exist(robot_id)
        return ROBOTS[robot_id]

    def delete(self, robot_id):
        auth, r = check_auth()
        if not auth:
            return r
        abort_if_robot_doesnt_exist(robot_id)
        del ROBOTS[robot_id]
        return '', 204

    def put(self, robot_id):
        auth, r = check_auth()
        if not auth:
            return r
        args = parser.parse_args()
        name = {'name': args['name']}
        ROBOTS[robot_id] = name
        return name, 201


# RobotList
# shows a list of all robots, and lets you POST to add new names
class RobotList(Resource):
    def get(self):
        return ROBOTS

    def post(self):
        auth, r = check_auth()
        if not auth:
            return r
        args = parser.parse_args()
        robot_id = int(max(ROBOTS.keys()).lstrip('robot')) + 1
        robot_id = 'robot%i' % robot_id
        ROBOTS[robot_id] = {'name': args['name']}
        return ROBOTS[robot_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(RobotList, '/robots')
api.add_resource(Robot, '/robots/<robot_id>')


if __name__ == '__main__':
    app.run(debug=True)