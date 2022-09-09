from peewee import *
from playhouse.shortcuts import model_to_dict

DATABASE = 'GitHubUserRepos.db'

database = SqliteDatabase(DATABASE)

# Base Pewee model for database
class Base(Model):
    class Meta:
        database = database

# User Model class
class User(Base):
    username = CharField(unique = True)

# Repository class
class Repository(Base):
    userId = ForeignKeyField(User)
    name = CharField()

# Utility function to create tables
def create_tables():
    with database:
        database.create_tables([User, Repository])