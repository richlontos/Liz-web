# import the function that will return an instance of a connection
import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint
import re
from flask_app.models.program import Program
# model the class after the user table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'fitness_coach'


class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.programs = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        # query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return User(result[0])
        else:
            return False


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user




    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", 'first_name')
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", 'last_name')
        if user['confirm-password'] != user['password']:
            is_valid = False
            flash("passwords must match")
        if len(user['password']) < 8:
            is_valid = False
            flash('password must be at least 8 characters')
        if not EMAIL_REGEX.match(user['email']): 
            is_valid = False
            flash("Invalid email address!")
        return is_valid


    @classmethod
    def get_one_with_programs(cls, data):
        query = "SELECT * FROM users LEFT JOIN programs ON users.id = programs.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = User(results[0])

        for result in results:
            temp_program = {
                "id": result['id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "user_id": result['user_id'],

                # "age": result['age'],
                "created_at": result['programs.created_at'],
                "updated_at": result['programs.updated_at']
            }
            user.programs.append(Program(temp_program))

        return user

    
