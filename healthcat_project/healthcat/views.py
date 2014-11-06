from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction

#Import classes
from healthcat.models import *
from forms import *

from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from smtplib import SMTP
from email.mime.text import MIMEText
from mimetypes import guess_type

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

import json


# Create your views here.
@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = {}
    user = request.user
    context['user'] = user
    owner = Owner.objects.get(user = user)
    context['owner'] = owner
    return render(request, 'healthcat/profile.html', context)

def register(request):
    context = {}
    errors = []
    
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'healthcat/register.html', context)

    form = RegistrationForm(request.POST, request.FILES)
    
    context['form'] = form
    
    if not form.is_valid():
        return render (request,'healthcat/register.html',context)

    new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'], 
                                        first_name = form.cleaned_data['first_name'],
                                        last_name = form.cleaned_data['last_name'],
                                        email=form.cleaned_data['username'])

    new_user.save()
    
    user_owner = Owner(user = new_user, zip_code = form.cleaned_data['zip_code'], photo=form.cleaned_data['photo'])

    user_owner.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to HealthCat. Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm_registration', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="ajfische@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['username']
    return render(request, 'healthcat/confirm_registration.html', context)

def reset_password(request):
    context = {}
    
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ResetPasswordForm()
        return render(request, 'healthcat/reset_password.html', context)

    form = ResetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render (request,'healthcat/reset_password.html', context)

    email = form.cleaned_data['email']
    user = User.objects.get(username=email)
    user.set_password("1234")
    user.save()
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(user)

    email_body = """
Your new password is: 1234
Please log in with this new password and change your password.
"""

    send_mail(subject="Password Reset",
              message= email_body,
              from_email="ajfische@andrew.cmu.edu",
              recipient_list=[user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'healthcat/sent_password.html', context)

def change_password(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ChangePasswordForm()
        return render(request, 'healthcat/change_password.html', context)

    form = ChangePasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render (request,'healthcat/change_password.html', context)

    user = request.user

    user.set_password(form.cleaned_data['password1'])
    user.save()

    return render(request, 'healthcat/login', context)

@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'healthcat/confirmed_registration.html', {})

@transaction.commit_on_success
def confirm_password_reset(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'healthcat/confirmed_password_reset.html', {})

@login_required
def get_owner_photo(request, user_id):
    user = get_object_or_404(User, id = user_id)
    owner = get_object_or_404(Owner, user=user)
    if not owner.photo:
        return Http404
    content_type = guess_type(owner.photo.name)
    return HttpResponse(owner.photo, content_type=content_type)

@login_required
def statistics(request):
    return redirect('/')


@login_required
def edit_profile(request):
    return redirect('/')