# Get relevant GitHub repositories from GitHub
from logging import error
from sre_constants import SUCCESS
from peewee import *
from playhouse.shortcuts import model_to_dict
import requests
import sys
from db import *
import math

def GetReposFromGitHub(username,userId):
    # api url to grab public user data
    user_info_api_url = f"https://api.github.com/users/{username}"

    try:
        # Get total number of repos for pagination
        user_info_request = requests.get(user_info_api_url)
        user_info = user_info_request.json()
        user_public_repos = user_info["public_repos"]
        num_pages = math.ceil(user_public_repos/30)

        status = user_info_request.status_code

        if(status == '404'):
            return 'Error:User not found'

        data = []
        for i in range(1,num_pages+1):
            api_url = f"https://api.github.com/users/{username}/repos?pages={i}"
            response = requests.get(api_url)
            #get the data in json or equivalent dict format
            data += response.json()

        # Create records in repository table
        for repo in data:
            print(repo['name'])
            Repository.create(userId = userId,name = repo['name'])
        return SUCCESS
    except:
        return "Something went wrong"

# Create user if not exists and adds the repositories to the Repositories table
def createUser(inputUser):
    try:
        user = User.select().where(User.username == inputUser).get()
    # if not user
    except:
        # add to database
        user = User.create(username = inputUser)
    finally:
        res = GetReposFromGitHub(inputUser,user.id)
        # Call service to get repositories
        if(res == SUCCESS):
            print("The user",inputUser,"was successfully added")
            return model_to_dict(user)
        else:
            return res

if __name__ == "__main__":
    create_tables()
    users = sys.argv[1].split(',')
    for user in users:
        createUser(user)