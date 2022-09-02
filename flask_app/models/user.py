import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()+_-].{8,}$')


class User:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @staticmethod
    def validate_registration(form:dict) -> bool:
        is_valid = True

        if not NAME_REGEX.match(form.get('first_name')):
            flash('* First name must be at least 2 characters long.')
            is_valid = False
        if not NAME_REGEX.match(form.get('last_name')):
            flash('* Last name must be at least 2 characters long.')
            is_valid = False
        if not EMAIL_REGEX.match(form.get('email')):
            flash('* Email must be valid.')
            is_valid = False
        if not PASSWORD_REGEX.match(form.get('password')):
            flash('* Password must be at least 8 characters!')
            is_valid = False
        if form.get('confirm_password') != form.get('password'):
            flash('* Passwords do not match.')
            is_valid = False

        return is_valid

    @classmethod
    def register_user(cls, data:dict) -> str:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('private-wall').query_db(query, data)
        return result