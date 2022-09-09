from collections import UserList
from crypt import methods
from dataclasses import dataclass
from distutils.log import error
from enum import unique
from os import abort
from pyexpat import model
from sre_constants import FAILURE, SUCCESS
from tokenize import String
from flask import Flask
from peewee import *
from playhouse.shortcuts import model_to_dict
import json
import requests
from flask_cors import CORS
from db import *
from script import *

# pagination, array

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

@app.route('/api/user/<name>', methods = ['GET'])
def getUserRepos(name):
    print("User repos asked for:",name)
    # try fetching user from user table
    try:
        user = User.select().where(User.username == name).get()
        print("return from select",user)
    # if not exists create user
    except:
        user = createUser(name)
        print("return from create user",user)
    finally:
        repos = list(Repository.select().where(Repository.userId == user.id).dicts())
        return repos

# Get users
@app.route('/api/users', methods = ['GET'])
def getUsers():
    users = list(User.select().dicts())
    return users

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '8080')