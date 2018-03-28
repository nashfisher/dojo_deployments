# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages
from django.contrib.messages import error
import bcrypt



def index(request):
    
    return render(request, 'login_reg_app/index.html')

def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        user =  Users.objects.create(
            name = request.POST['name'],
            username = request.POST['username'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
            date_hired = request.POST['date_hired'],
        )
        # request.session['logged_user'] = request.POST['first_name']
    context = {
        
    }
    return redirect('/')

def login(request):
    errors = Users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        request.session['logged_user'] = request.POST['username_login']
        return redirect('/exam_app')
        
# def success(request):
#     context = {
#         'logged_in' : request.session['logged_user']
#     }
#     return render(request, 'login_reg_app/success.html', context)

# Create your views here.
