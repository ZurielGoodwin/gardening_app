from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import garden
bcrypt = Bcrypt(app)



class User:
    db= 'garden'
    def __init__ (self, data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
        self.garden = []



    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append (cls(row))
        return users


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])


    @staticmethod
    def validate_register(user):
        is_valid=True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            is_valid = False
            flash("That email is already in our database")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid email characters")
        if len(user['first_name']) < 2:
            is_valid = False
            flash('At least 2 characters are required for the first name')
        if len(user['last_name']) < 2:
            is_valid = False
            flash('At least 2 characters are required for the last name')
        if len(user['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters long')
        if user['password'] != user['confirm']:
            is_valid = False
            flash('Passwords do not match')
        return is_valid
