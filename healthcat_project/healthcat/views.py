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

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from smtplib import SMTP
from email.mime.text import MIMEText
from mimetypes import guess_type

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

# making http requests and json
import urllib2,urllib,httplib,json

import time

#debug
import random

# serializing data to send back to bowl.
from django.core import serializers



# Create your views here.
@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = {}
    context = _add_profile_context(request, context)
    return render(request, 'healthcat/profile.html', context)


def _add_profile_context(request, context):
    user = request.user
    context['user'] = user
    owner = Owner.objects.get(user=user)
    context['owner'] = owner
    bowls = Bowl.objects.filter(owner=owner)
    context['bowls'] = bowls
    feeding_intervals = FeedingInterval.objects.all()
    print "feeding intervals: "
    print feeding_intervals
    return context

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
def get_pet_photo(request, pet_id):
    pet = get_object_or_404(Pet, id = pet_id)
    if not pet.photo:
        return Http404
    content_type = guess_type(pet.photo.name)
    return HttpResponse(pet.photo, content_type=content_type)

@login_required
def statistics(request):
    context = {}
    user = request.user
    context['user'] = user
    owner = Owner.objects.get(user = user)
    context['owner'] = owner
    return render(request, 'healthcat/statistics.html', context)


@login_required
def edit_profile(request):
    return redirect('/')

@login_required
def add_feeding_interval(request):
    context={}
    context = _add_profile_context(request, context)

    if request.method=='GET':
        context['feeding_interval_form'] = FeedingIntervalForm()
        bowl_id = request.GET.get("bowl_id")
        context['bowl_id'] = bowl_id
        pet_id = request.GET.get("pet_id")
        context['pet_id'] = pet_id
        return render(request,'healthcat/feeding_interval_form.html',context)

    bowl_id = request.POST.get("bowl_id")
    bowl = get_object_or_404(Bowl, id=bowl_id)
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, id=pet_id)

    feeding_interval = FeedingInterval(pet=pet)
    feeding_interval_form = FeedingIntervalForm(request.POST, instance=feeding_interval)
    
    if not feeding_interval_form.is_valid():
        context['feeding_interval_form'] = feeding_interval_form
        context['pet_id'] = pet_id
        context['bowl_id'] = bowl_id
        return render(request, 'healthcat/profile.html', context)

    feeding_interval_form.save()

    return render(request, 'healthcat/profile.html', context)

@login_required
def edit_feeding_interval(request):
    context = {}
    context = _add_profile_context(request, context)
    
    print "in edit_feeding_interval"
    if request.method == 'GET':
        print "method == GET"
        pet_id = request.GET.get("pet_id")
        print "pet id: " + pet_id
        bowl_id = request.GET.get("bowl_id")
        print "bowl id: " + bowl_id
        feeding_interval_id = request.GET.get("feeding_interval_id")
        feeding_interval = get_object_or_404(FeedingInterval, id=feeding_interval_id)
        initial = {}
        start =  feeding_interval.start
        print start
        initial['start'] = start
        
        initial['end'] = feeding_interval.end
        initial['amount'] = feeding_interval.amount
        feeding_interval_form = FeedingIntervalForm(initial=initial)
        context['feeding_interval_form'] = feeding_interval_form
        context['pet_id'] = pet_id
        context['bowl_id'] = bowl_id
        context['feeding_interval_id'] = feeding_interval_id
        return render(request,'healthcat/edit_feeding_interval_form.html',context)

    pet_id = request.POST.get("pet_id")
    bowl_id = request.POST.get("bowl_id")
    feeding_interval_id = request.POST.get("feeding_interval_id")
    feeding_interval = get_object_or_404(FeedingInterval, id=feeding_interval_id)

    feeding_interval_form = FeedingIntervalForm(request.POST, instance=feeding_interval)

    if not feeding_interval_form.is_valid():
        context['feeding_interval_form'] = feeding_interval_form
        context['pet_id'] = pet_id
        context['bowl_id'] = bowl_id
        context['feeding_interval_id'] = feeding_interval_id
        return render(request, 'healthcat/profile.html', context)

    feeding_interval_form.save()

    return render(request, 'healthcat/profile.html', context)

@login_required
def edit_pet(request):
    context = {}
    context = _add_profile_context(request, context)

    if request.method == 'GET':
        pet_id = request.GET.get("pet_id")
        bowl_id = request.GET.get("bowl_id")
        pet = get_object_or_404(Pet, id=pet_id)
        initial = {}
        initial['name'] = pet.name
        initial['rfid'] = pet.rfid
        initial['photo'] = pet.photo
        pet_form = PetForm(initial=initial)
        context['pet_form'] = pet_form
        context['pet_id'] = pet_id
        context['bowl_id'] = bowl_id
        return render(request,'healthcat/edit_pet_form.html',context)

    pet_id = request.POST.get("pet_id")
    bowl_id = request.POST.get("bowl_id")
    pet = get_object_or_404(Pet, id=pet_id)
    
    context['pet_id'] = pet_id

    pet_form = PetForm(request.POST, request.FILES, instance=pet)

    if not pet_form.is_valid():
        context['pet_form'] = pet_form
        context['pet_id'] = pet_id
        context['bowl_id'] = bowl_id
        return render(request, 'healthcat/profile.html', context)

    pet_form.save()

    return render(request, 'healthcat/profile.html', context)

@login_required
def add_pet(request):
    context={}
    context = _add_profile_context(request, context)

    if request.method=='GET':
        context['pet_form'] = PetForm()
        bowl_id = request.GET.get("bowl_id")
        context['bowl_id'] = bowl_id
        return render(request,'healthcat/pet_form.html',context)

    bowl_id = request.POST.get("bowl_id")
    bowl = get_object_or_404(Bowl, id=bowl_id)
    owner = Owner.objects.get(user=request.user)
    new_pet = Pet(owner=owner)

    pet_form = PetForm(request.POST, request.FILES, instance=new_pet)
    
    if not pet_form.is_valid():
        print "pet form not valid"
        context['pet_form'] = pet_form
        context['bowl_id'] = bowl_id
        return render(request, 'healthcat/profile.html', context)

    pet_form.save()

    bowl.pets.add(Pet.objects.get(id=new_pet.id))

    return render(request, 'healthcat/profile.html', context)

@login_required
def add_bowl(request):
    context={}
    context = _add_profile_context(request, context)

    print 'adding a bowl'


    if request.method=='GET':
        context['add_bowl_form'] = BowlForm()
        return render(request,'healthcat/add_bowl_form.html',context)

    owner = Owner.objects.get(user=request.user)
    # new_bowl = Bowl(owner=owner, serial_number=random.random()) #todo implement serial
    new_bowl = Bowl(owner=owner) #todo implement serial

    add_bowl_form = BowlForm(request.POST, instance=new_bowl)
    
    if not add_bowl_form.is_valid():
        context['add_bowl_form'] = add_bowl_form
        return render(request, 'healthcat/profile.html', context)


    # ip_address = add_bowl_form.cleaned_data['ip_address']

    # try:
    #     r = urllib2.urlopen(ip_address+'connect').read()
    #     print r
    # except:
    #     print "Could not connect to " + ip_address

    # logic here
    bowl_serial = add_bowl_form.cleaned_data['serial_number']

    unassigned_bowl = UnAssignedBowls.objects.filter(bowl_serial=bowl_serial)
    # print unassigned_bowl

    print unassigned_bowl[0].is_valid

    if unassigned_bowl and unassigned_bowl[0].is_valid:
        print 'creating new bowl from unassigned_bowl'
        unassigned_bowl[0].is_valid=False
        add_bowl_form.save()

    return render(request, 'healthcat/profile.html', context)

    #old code below
    # exisiting_bowl = Bowl.objects.filter(ip_address=ip_address)
    # if exisiting_bowl:
    #     print "bowl model already exists"
    #     exisiting_bowl[0].owner = owner #Todo add caretaker
    # else:
    #     print "creating new bowl model"
    #     add_bowl_form.save()

    # return render(request, 'healthcat/profile.html', context)

@login_required
def edit_bowl(request):
    print "in edit bowl"
    context={}
    context = _add_profile_context(request, context)

    if request.method=='GET':
        bowl_id = request.GET.get("bowl_id")
        bowl = get_object_or_404(Bowl, id=bowl_id)
        initial = {}
        initial['ip_address'] = bowl.ip_address
        initial['name'] = bowl.name
        bowl_form = BowlForm(initial=initial)
        context['bowl_form'] = bowl_form
        context['bowl_id'] = bowl_id
        return render(request,'healthcat/edit_bowl_form.html',context)
    
    bowl_id = request.POST.get("bowl_id")
    context['bowl_id'] = bowl_id
    bowl = get_object_or_404(Bowl, id=bowl_id)
    bowl_form = BowlForm(request.POST, instance=bowl)
    
    if not bowl_form.is_valid():
        context['bowl_form'] = bowl_form
        context['bowl_form_id'] = bowl_id
        return render(request, 'healthcat/profile.html', context)

    bowl_form.save()

    return render(request, 'healthcat/profile.html', context)

# this function is called when there is a request from a bowl with new rfid.
def registerRfid(request,bowlSerial,rfid):
    responseDict= {}

    # get the user with the bowl.
    try: 
        bowl=Bowl.objects.get(serial_number=bowlSerial)
        bowl_owner_email = bowl.owner.user.username
        responseDict['result']='SUCCESS'
    except:
        print 'result is fail . '
        responseDict['result']='FAIL'
        return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

    email_body = "We have found a new RFID on bowl %s.\
     The RFID is %s"%(bowlSerial,rfid)
    send_mail(subject="New RFID Detected",
      message= email_body,
      from_email="healthcat15637@gmail.com",
      recipient_list=[bowl_owner_email])
    responseDict['result']='SUCCESS'
    return HttpResponse(json.dumps(responseDict),
        content_type="application/json")


# this function is used to retrieve cat's food schedule.
def retrieveFeedingIntervals(request,rfid):

    responseDict={}

    #get the cat exists based on the rfid.
    try:
        p=Pet.objects.get(rfid=rfid)
    except ObjectDoesNotExist:
        # responseDict["result"]="FAIL"
        return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

    #get the feeding interval based on rfid
    intervals= FeedingInterval.objects.filter(pet=p)
    jsonIntervals =serializers.serialize('json',intervals,
        fields=('start','end','amount',))
    return HttpResponse(jsonIntervals,content_type="application/json")

def addConsumptionRecord(request,rfid,amount,dateAndTime):

    #based on get request consumption record is added. 
    # needs authentication and POST ??
    #get the cat exists based on the rfid.
    responseDict={}
    try:
        p=Pet.objects.get(rfid=rfid)
    except ObjectDoesNotExist:
        responseDict["result"]="FAIL"
        return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

    #extract date and time.
    

    pass

@csrf_exempt
def validateBowl(request):
    responseDict={}

    if request.method=='POST':
        bowl_serial = request.POST.get('bowlSerial')
        bowl_key = request.POST.get('bowlKey')
        validate = request.POST.get('validate')

        try:
            unassigned_bowl = UnAssignedBowls.objects.get(bowl_serial = bowl_serial)
            print 'now '
            if not unassigned_bowl.bowl_key == bowl_key:
                raise bowlKeyMismatch
            unassigned_bowl.is_valid = validate=='True'

            responseDict['result']='PASS'
            unassigned_bowl.save()
            return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

        except :
            responseDict['result']='FAIL'
            return HttpResponse(json.dumps(responseDict),
            content_type="application/json")


    responseDict['result'] = 'NOT PASSED : GET REQUEST'
    return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

    pass
