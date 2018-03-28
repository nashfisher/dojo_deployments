# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from ..login_reg_app.models import Users
from .models import Items
from django.contrib import messages
from django.contrib.messages import error

def index(request):
    
    context = {
        "Items" : Items.objects.all(),
        'My_Items' : Items.objects.filter(creator = request.session['logged_user']) | Items.objects.filter(other_triptakers=Users.objects.get(username=request.session["logged_user"])),
        'logged_user' : request.session['logged_user'],
    }
    return render(request,'exam_app/index.html', context)

def new(request):

    return render(request, 'exam_app/new.html')

def create(request):
    print 'made it to create'

    errors = Items.objects.item_manager(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect ('/exam_app/new')
    else:
        item = Items.objects.create(
            name = request.POST['name'],
            creator = request.session['logged_user'],
        )
        
    return redirect('/exam_app/')

def show(request, id):
    print 'made it to show'
    trip_show = Items.objects.get(id = id)
    triptakers = Items.objects.all()
    context = {
        'item' : trip_show,
        'triptakers' : triptakers,
        'logged_user' : request.session['logged_user'],
    }
    return render(request, 'exam_app/item_page.html', context)

def join(request, id):
    print 'made it to join'
    current_user = Users.objects.get(username = request.session['logged_user'])
    trip_to_join = Items.objects.get(id=id)
    if trip_to_join.creator == request.session['logged_user']:
        return redirect('/exam_app')
    else:
        trip_to_join.other_triptakers.add(current_user)
        trip_to_join.save()
    
    return redirect('/exam_app')

def remove(request, id):
    print 'made it to remove'
    current_user = Users.objects.get(username = request.session['logged_user'])
    trip_to_join = Items.objects.get(id=id)
    trip_to_join.other_triptakers.remove(current_user)
    trip_to_join.save()
    
    return redirect('/exam_app')

def destroy(request, id):
    print 'made it to destroy'
    print request.session['logged_user']
    print id

    target_item = Items.objects.get(id = id)

    if target_item.creator == request.session['logged_user']:
        target_item.delete()
    else:
        print 'wrong user'
    return redirect('/exam_app')

def logout(request):
    request.session.clear()

    return redirect('/')
# Create your views here.
