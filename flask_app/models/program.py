# import the function that will return an instance of a connection
import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
# model the class after the program table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'fitness_coach'


class Program:
    def __init__(self, data) -> None:
        self.id = data['id']
        if 'first_name' in data:
            self.first_name = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']