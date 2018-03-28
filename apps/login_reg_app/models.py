# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
import datetime
import bcrypt

class RegManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name value cannot be less than 3 characters."
        # if len(postData['last_name']) < 2:
        #     errors['last_name'] = "Last name value cannot be less than 2 characters."
        if len(postData['username']) < 3:
            errors['username'] = 'Username cannot be less than 3 characters.'
        # try:
        #     validate_email(postData['email'])
        # except ValidationError:
        #     errors['email'] = 'Invalid email'
        # else:
        #     if Users.objects.filter(email = postData['email']):
        #         errors['email'] = "Email already in use."
        if postData['password'] != postData['password_confirm']:
            errors['password'] = 'Passwords do not match'
        if len(postData['password']) < 8:
            errors['password'] = 'Passwords must be at contain at least 8 characters.'
        if not postData['date_hired']:
            errors['date'] = 'Date hired cannot be empty'
        if postData['date_hired']:
            dt = datetime.datetime.now()
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            if datetime.datetime.strptime(postData['date_hired'], '%Y-%m-%d') > dt:
                errors['valid_date'] = 'Start date must be prior to current date.'
                print datetime.datetime.now()
                print datetime.datetime.strptime(postData['date_hired'], '%Y-%m-%d')

        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['username_login']) < 1:
            errors['username_empty'] = 'Username input cannot be blank'
            return errors
        if len(Users.objects.filter(username = postData['username_login'])) < 1:
            errors['unexisting_user'] = 'User does not exist'
            return errors
        User_id = Users.objects.get(username = postData['username_login'])
        if postData['username_login'] == User_id.username:      
            user_check = Users.objects.get(username = postData['username_login'])
            if bcrypt.checkpw(postData['password_login'].encode(), user_check.password.encode()):
                return errors
            else:
                errors['login'] = 'Invalid password'
                return errors
        else:
            errors['login_username'] = 'Username does not match any existing users.'
            return errors

class Users(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    date_hired = models.DateField()

    objects = RegManager()
# Create your models here.
