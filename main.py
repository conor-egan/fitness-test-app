from boto3 import resource
from flask import json, request, abort
from flask import Flask
from decimal import Decimal
from user_helper import SignUpCredential, LoginCredential, User
from flask_restplus import Api, Resource, fields

application = Flask(__name__)
api = Api(application)

JSONEncoder_olddefault = json.JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, Decimal):
        return float(o)
    return JSONEncoder_olddefault(self, o)


json.JSONEncoder.default = JSONEncoder_newdefault

dynamodb = resource('dynamodb', region_name='eu-west-1')
user_table = dynamodb.Table('User')
program_table = dynamodb.Table('Programs')


resource_fields = api.model('login_credential', {
    'username': fields.String,
    'password': fields.String
})



@api.route('/users', methods=['GET', 'POST'])
class Users(Resource):
    def get(self):
        resp = users_get()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    @api.expect(resource_fields)
    def post(self):
        return user_login()


@api.route('/users/<string:Username>', methods=['GET', 'PUT', 'DELETE'])
class User(Resource):
    def get(self, Username):
        return user_get(Username)

    def put(self, Username):
        return create_user(Username)

    def delete(self, Username):
        return delete_user(Username)


@api.route('/users/<string:Username>/programs', methods=['GET'])
class UserPrograms(Resource):
    # This would probably query a separate table to the User table and
    # return more detailed results
    def get(self, Username):
        return json.jsonify(get_user_programs(Username))


@api.route('/users/<string:Username>/programs/<string:program_name>', methods=['GET'])
class UserProgramDetails(Resource):
    # This would probably query a separate table to the User table and
    # return more detailed results
    def get(self, Username, program_name):
        return get_user_program(Username, program_name)

# below are the helper methods


def users_get():
    response = user_table.scan()
    item = response['Items']
    users = list()
    for user in item:
        user_obj = {'Username': user['Username'], 'fullname': user['fullname'],
                    'email': user['email'], 'liftmaxes': user['liftmaxes'], 'programs': user['programs']}
        users.append(user_obj)

    return json.jsonify(users)


def user_login():
    credential = LoginCredential(request.form['Username'], request.form['password'])
    user = user_table.get_item(
        Key={
            'Username': credential.username
        }
    )
    item = user['Item']

    if item['password'] == credential.password:
        return json.jsonify({"success": True})
    else:
        return json.jsonify({"success": False})


def user_get(Username):
    response = get_user_response(Username)
    if 'Item' not in response.keys():
        return abort(404)
    else:
        item = response['Item']
        user_obj = User(item['Username'], item['fullname'], item['email'], item['liftmaxes'], item['programs'])
        return json.jsonify(user_obj.to_dict())


def create_user(Username):
    cred = SignUpCredential(Username, request.form['email'], request.form['fullname'], request.form['password'])
    user_table.put_item(
        Item={
            'Username': cred.username,
            'email': cred.email,
            'fullname': cred.fullname,
            'password': cred.password,
            'liftmaxes': {},
            'programs': [],
            'prefferedunit': 'lbs'
        })

    response = get_user_response(Username)
    item = response['Item']
    return json.jsonify(item)


def delete_user(Username):
    user_table.delete_item(Key={
        'Username': Username
    })
    return json.jsonify({"deleted": True})


def get_user_programs(Username):
    response = get_user_response(Username)
    item = response['Item']
    return item['programs']


def get_user_program(Username, program_name):
    return "implementation goes here"


def get_user_response(Username):
    response = user_table.get_item(
        Key={
            'Username': Username
        }
    )
    return response

if __name__ == "__main__":
    application.run('0.0.0.0')
