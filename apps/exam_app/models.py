# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_reg_app.models import Users
import datetime
import math

class ItemsManager(models.Manager):
    def item_manager(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = 'Name cannot be empty.'
        if len(postData['name']) < 4:
            errors['name2'] = 'Name must be longer than 3 characters.'
        
        return errors

class Items(models.Model):
    name = models.CharField(max_length = 250)
    creator = models.CharField(max_length = 250)
    created_at = models.DateTimeField(auto_now_add = True)
    
    other_triptakers = models.ManyToManyField(Users, related_name='joined_trips')

    objects = ItemsManager()
# Create your models here.
