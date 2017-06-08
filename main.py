from boto3 import resource
from flask import json, request
from flask import Flask
from decimal import Decimal
application = Flask(__name__)

JSONEncoder_olddefault = json.JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, Decimal):
        return float(o)
    return JSONEncoder_olddefault(self, o)
json.JSONEncoder.default = JSONEncoder_newdefault


@application.route('/users', methods=['GET', 'POST', ' PUT', 'DELETE'])
def all_user_data():
    dynamodb = resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('User')
    if request.method == 'GET':
        response = table.scan()
        item = response['Items']
        return json.jsonify(item)
    elif request.method == 'POST':
        table.put_item(
            Item={
                'Username': request.form['Username'],
                'email': request.form['email']
            })

        response = table.scan()
        item = response['Items']
        return json.jsonify(item)




@application.route('/users/<string:Username>', methods=['GET', 'POST', ' PUT', 'DELETE'])
def single_user_data(Username):
    if request.method == 'GET':
        dynamodb = resource('dynamodb')
        table = dynamodb.Table('User')
        response = table.get_item(
            Key={
                'Username': Username
            }
        )
        item = response['Item']

        return json.jsonify(item)






if __name__ == "__main__":
    application.run('0.0.0.0')

