# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json

import flask
from flask import request, Response

#from boto import dynamodb2
#from boto.dynamodb2.table import Table
#from boto.dynamodb2.items import Item
#from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from boto import sns

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from functools import wraps


# Default config vals
THEME = 'default' if os.environ.get('THEME') is None else os.environ.get('THEME')
FLASK_DEBUG = 'false' if os.environ.get('FLASK_DEBUG') is None else os.environ.get('FLASK_DEBUG')
AWS_REGION = 'us-east-1' if os.environ.get('AWS_REGION') is None else os.environ.get('AWS_REGION')
#STARTUP_SIGNUP_TABLE = '' if os.environ.get('STARTUP_SIGNUP_TABLE') is None else os.environ.get('STARTUP_SIGNUP_TABLE')
STARTUP_SIGNUP_RDBMS = '' if os.environ.get('STARTUP_SIGNUP_RDBMS') is None else os.environ.get('STARTUP_SIGNUP_RDBMS')
NEW_SIGNUP_TOPIC = '' if os.environ.get('NEW_SIGNUP_TOPIC') is None else os.environ.get('NEW_SIGNUP_TOPIC')

# Create the Flask app
application = flask.Flask(__name__)

# Load config values specified above
application.config.from_object(__name__)

# Only enable Flask debugging if an env var is set to true
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

# Connect to MySQL DB
application.config['MYSQL_DATABASE_USER'] = 'dbuser'
application.config['MYSQL_DATABASE_PASSWORD'] = 'dbpassword'
application.config['MYSQL_DATABASE_DB'] = 'userdb'
application.config['MYSQL_DATABASE_HOST'] = application.config['STARTUP_SIGNUP_RDBMS']
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + application.config['MYSQL_DATABASE_USER'] + ':' + application.config['MYSQL_DATABASE_PASSWORD'] + '@' + application.config['MYSQL_DATABASE_HOST'] + '/' + application.config['MYSQL_DATABASE_DB']

db = SQLAlchemy(application)

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    theme = db.Column(db.String(30))
    previewAccess = db.Column(db.String(10))
    age = db.Column(db.Integer)

# Connect to DynamoDB and get ref to Table
#ddb_conn = dynamodb2.connect_to_region(application.config['AWS_REGION'])
#ddb_table = Table(table_name=application.config['STARTUP_SIGNUP_TABLE'],connection=ddb_conn)

# Connect to SNS
sns_conn = sns.connect_to_region(application.config['AWS_REGION'])


@application.route('/')
def welcome():
    theme = application.config['THEME']
    return flask.render_template('index.html', theme=theme, flask_debug=application.debug)


@application.route('/signup', methods=['POST'])
def signup():
    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    exists = User.query.filter_by(email=signup_data["email"]).first()
    if exists is None:
        store_in_rdbms(signup_data)
#       store_in_dynamo(signup_data)
        publish_to_sns(signup_data)
    else:
        return Response("", status=409, mimetype='application/json')

    return Response(json.dumps(signup_data), status=201, mimetype='application/json')
      

def store_in_rdbms(signup_data):
   db.session.add(User(**signup_data))
   db.session.commit()

#def store_in_dynamo(signup_data):
#    signup_item = Item(ddb_table, data=signup_data)
#    signup_item.save()


def publish_to_sns(signup_data):
    try:
        sns_conn.publish(application.config['NEW_SIGNUP_TOPIC'], json.dumps(signup_data), "New signup: %s" % signup_data['email'])
    except Exception as ex:
        sys.stderr.write("Error publishing subscription message to SNS: %s" % ex.message)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@application.route('/users')
@requires_auth
def show_users():
    entries = User.query.all()
    theme = application.config['THEME']
    return flask.render_template('users.html', theme=theme, title='A New Startup - Registered Users', entries=entries)


@application.errorhandler(404)
def not_found_error(error):
    print u'{ "Page Not Found": "%s" }' % error
    theme = application.config['THEME']
    return flask.render_template('404.html', theme=theme, title='404 File Not Found'), 404

@application.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    print u'{ "Reason": "%s" }' % error
    theme = application.config['THEME']
    return flask.render_template('500.html', theme=theme, title='Unexpected Error Occured'), 500



if __name__ == '__main__':
    application.run(host='0.0.0.0')
