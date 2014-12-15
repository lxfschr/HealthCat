from django.shortcuts import render, redirect, get_object_or_404, render_to_response
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

import time,datetime
from django.utils import timezone

#debug
import random

# serializing data to send back to bowl.
from django.core import serializers

#time out
TIMEOUT = 120 #seconds

# Create your views here.
@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = {}
    context = _add_profile_context(request, context)
    w = PetForm()
    print "media: ", w.media
    return render(request, 'healthcat/profile.html', context)

@login_required
def failed_to_connect(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = {}
    context = _add_profile_context(request, context)
    context['modal'] = "healthcat/failed_to_connect.html"
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
@transaction.commit_on_success
def notifications(request):
    date = request.GET.get("date")
    print date
    context = {}
    context = _add_profile_context(request, context)

    owner = Owner.objects.get(user = request.user)
    bowls = Bowl.objects.filter(owner = owner)

    notifications = []

    if date is not None:
        notifications = ConsumptionRecord.objects.all().filter(bowl__in=bowls).filter(date__gt=date).order_by('-date')
        consumption_records = ConsumptionRecord.objects.all().filter(bowl__in=bowls).filter(date__gt=date).order_by('-date')
        bullying_records = BullyingRecord.objects.all().filter(bowl__in=bowls).filter(date__gt=date).order_by('-date')
        new_rfid_records = NewRFIDRecord.objects.all().filter(bowl__in=bowls).filter(date__gt=date).order_by('-date')
        refilled_bowl_records = RefilledBowlRecord.objects.all().filter(bowl__in=bowls).filter(date__gt=date).order_by('-date')

        latest = list(consumption_records) + list(bullying_records) + list(new_rfid_records) + list(refilled_bowl_records)
        notifications = sorted(latest, key=lambda x: x.date, reverse=True)
    else:
        notifications = ConsumptionRecord.objects.all().filter(bowl__in=bowls).order_by('-date')
        consumption_records = ConsumptionRecord.objects.all().filter(bowl__in=bowls).order_by('-date')
        bullying_records = BullyingRecord.objects.all().filter(bowl__in=bowls).order_by('-date')
        new_rfid_records = NewRFIDRecord.objects.all().filter(bowl__in=bowls).order_by('-date')
        refilled_bowl_records = RefilledBowlRecord.objects.all().filter(bowl__in=bowls).order_by('-date')

        latest = list(consumption_records) + list(bullying_records) + list(new_rfid_records) + list(refilled_bowl_records)
        notifications = sorted(latest, key=lambda x: x.date, reverse=True)

    context['notifications'] = notifications
    owner.num_notifications = 0;
    owner.save()
    if date is not None:
        return render(request, 'healthcat/notifications_list.html', context)
    else:
        return render(request, 'healthcat/notifications.html', context)    

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
def delete_feeding_interval(request):
    context = {}
    context = _add_profile_context(request, context)
    response = {}
    feeding_interval_id = request.POST.get("feeding_interval_id")
    # Deletes the item if present in the todo-list database.
    try:
        item_to_delete = FeedingInterval.objects.get(id=feeding_interval_id)
        item_to_delete.delete()
    except ObjectDoesNotExist:
        pass

    response['result']='SUCCESS'
    return HttpResponse(json.dumps(response),
        content_type="application/json")

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
        initial['color'] = pet.color
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

    _determine_next_color(Owner.objects.filter(user=request.user))

    return render(request, 'healthcat/profile.html', context)

def _determine_next_color(owner):
    hex_colors = [pet.encode("utf8") for pet in Pet.objects.filter(owner=owner).values_list('color', flat=True)]
    colors = []
    for hex_color in hex_colors:
        colors.append(hex_color.translate(None, '#').upper())
    print "colors: ", colors 
    from django.conf import settings
    print "settings.COLORS: ", settings.COLORS
    for color in settings.COLORS:
        if color not in colors:
            settings.NEXT_COLOR = color
            print "settings.NEXT_COLOR: ", settings.NEXT_COLOR
            break

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

    _determine_next_color(owner)

    bowl.pets.add(Pet.objects.get(id=new_pet.id))

    return render(request, 'healthcat/profile.html', context)

@login_required
def add_bowl(request):
    context={}
    context = _add_profile_context(request, context)

    if request.method=='GET':
        context['add_bowl_form'] = BowlForm()
        return render(request,'healthcat/add_bowl_form.html',context)

    owner = Owner.objects.get(user=request.user)
    new_bowl = Bowl(owner=owner) #todo implement serial

    add_bowl_form = BowlForm(request.POST, instance=new_bowl)
    
    if not add_bowl_form.is_valid():
        context['add_bowl_form'] = add_bowl_form
        return render(request, 'healthcat/profile.html', context)

    # logic here
    bowl_serial = add_bowl_form.cleaned_data['serial_number']
    bowl_name = add_bowl_form.cleaned_data['name']
    
    unassigned_bowl = UnAssignedBowls.objects.get( bowl_serial=bowl_serial )
    
    #get the current datetime
    cDateTime = datetime.datetime.now()

    # update / create a connection pending bowl.
    try:
        cpBowl=ConnectionPendingBowls.objects.get(uaBowl=unassigned_bowl)
        cpBowl.initTime = cDateTime
        cpBowl.name=bowl_name
        cpBowl.save()

    except:
        newcpBowl = ConnectionPendingBowls(uaBowl=unassigned_bowl,
         owner=owner,initTime=cDateTime, name=bowl_name)
        newcpBowl.save()

    context['modal'] = "healthcat/press_button_modal.html"
    context['serial_number'] = bowl_serial

    return render(request, 'healthcat/profile.html', context)



@login_required
def edit_bowl(request):
    print "in edit bowl"
    context={}
    context = _add_profile_context(request, context)

    if request.method=='GET':
        bowl_id = request.GET.get("bowl_id")
        bowl = get_object_or_404(Bowl, id=bowl_id)
        initial = {}
        initial['name'] = bowl.name
        bowl_form = EditBowlForm(initial=initial)
        context['bowl_form'] = bowl_form
        context['bowl_id'] = bowl_id
        return render(request,'healthcat/edit_bowl_form.html',context)
    
    bowl_id = request.POST.get("bowl_id")
    context['bowl_id'] = bowl_id
    bowl = get_object_or_404(Bowl, id=bowl_id)
    bowl_form = EditBowlForm(request.POST, instance=bowl)
    
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
    # send_mail(subject="New RFID Detected",
    #   message= email_body,
    #   from_email="healthcat15637@gmail.com",
    #   recipient_list=[bowl_owner_email])
    print email_body
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
        print 'validating bowl  : '+ bowl_serial

        try:
            unassigned_bowl = UnAssignedBowls.objects.get(bowl_serial = bowl_serial)

            print 'unassigned_bowl found'

            if not unassigned_bowl.bowl_key == bowl_key:
                print 'bowlKey Mismatch'
                raise Exception('bowlKeyMismatch')

            cpBowl = ConnectionPendingBowls.objects.get(uaBowl=unassigned_bowl)


            print 'connection pending bowl found'


            # check for time out. 
            timenow = timezone.now()
            cpBowlTime = cpBowl.initTime
            dTime=datetime.timedelta(seconds=TIMEOUT)

            if timenow - cpBowlTime >dTime:
                print 'timeout'
                raise Exception('bowlValidationTimeOut')


            #create a connected bowl.
            newBowl = Bowl(name=cpBowl.name,owner=cpBowl.owner,
                serial_number=bowl_serial)
            newBowl.save()

            cpBowl.delete()

            responseDict['result']='PASS'
 
            return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

        except Exception, e:
            print e

            responseDict['result']='FAIL'
            return HttpResponse(json.dumps(responseDict),
            content_type="application/json")


    responseDict['result'] = 'NOT PASSED : GET REQUEST'
    return HttpResponse(json.dumps(responseDict),
            content_type="application/json")

    pass

def isBowlConnected(request):
    serial_number = request.GET.get("serial_number")
    print "serial_number: " + serial_number
    responseDict={}

    try:

        b = Bowl.objects.get(serial_number=serial_number)
        responseDict['result'] = 'SUCCESS'

        print 'returning success'

        return HttpResponse(json.dumps(responseDict),
            content_type="application/json")    
    except Exception, e:

        print 'returning fail exception :', e
        responseDict['result'] = 'FAIL'
        return HttpResponse(json.dumps(responseDict),
            content_type="application/json")


def add_bully(request):

    if request.method=='POST':
        bowl_serial = request.POST.get('bowlSerial')
        bowl_key = request.POST.get('bowlKey')
        validate = request.POST.get('validate')

        try :
            pass
        except:
            pass
    responseDict['result'] = 'NOT IMPLEMENTED'
    return HttpResponse(json.dumps(responseDict),
        content_type="application/json")

def _mass_addition(list):
    sum = 0
    for item in list:
        sum += item
    return sum

@login_required
def total_consumption(request):
    owner = Owner.objects.filter(user=request.user)
    pets = Pet.objects.filter(owner=owner)
    colors = [pet.encode("utf8") for pet in pets.values_list('color', flat=True)]
    amounts = []
    for pet in pets:
        amounts.append(_mass_addition(ConsumptionRecord.objects.filter(pet=pet).values_list("amount", flat=True)))
    xdata = pets.values_list("name", flat=True)
    ydata = amounts
    extra_serie = {"tooltip": {"y_start": "", "y_end": " grams"}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {'color': colors}
        }
    }
    return render_to_response('healthcat/piechart.html', data)

def _dates_inbetween(start, end):
    r = (end-start).days
    return [start+datetime.timedelta(days=i) for i in range(1,r)]

from itertools import tee, islice, chain, izip

def _previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)

@login_required
def consumption_over_time(request):
    owner = get_object_or_404(Owner, user=request.user)
    pets = Pet.objects.filter(owner=owner)
    colors = [pet.encode("utf8") for pet in pets.values_list('color', flat=True)]

    # Add tooltip to chartdata
    tooltip_date = "%d %b %Y"
    extra_serie = {"tooltip": {"y_start": "consumed ", "y_end": " grams"},
                   "date_format": tooltip_date}
    chartdata = {
        'x': [],
        'y1': [],
        'extra1': extra_serie,
        'extra2': extra_serie,
        'extra3': extra_serie
    }
    from django.conf import settings
    charttype = "lineWithFocusChart"
    chartcontainer = 'linewithfocuschart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': settings.DATE_FORMAT,
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {'color': colors}
        }
    }

    # find earliest date
    start_date = None
    try:
        start_date = ConsumptionRecord.objects.filter(pet__owner=owner).order_by('date')[:1].get().date.date()
        end_date = ConsumptionRecord.objects.filter(pet__owner=owner).latest('date').date.date()
        print "start_date", start_date
        print "end_date", end_date
    except ObjectDoesNotExist:
        return render_to_response('healthcat/line_graph_with_focus.html', data)

    # create dictionary of dates and amounts
    from collections import OrderedDict
    for i, pet in enumerate(pets):
        index = i+1
        date_dict = OrderedDict()
        print "pet: ", pet.name
        records = ConsumptionRecord.objects.filter(pet=pet).order_by('date')
        print "records: ", records
        last_record = None
        for prev, record, next in _previous_and_next(records):
            # if the date already exisits, add the amount to the value
            if date_dict.has_key(record.date.date()):
                prev_value = date_dict[record.date.date()]
                date_dict[record.date.date()] = prev_value + record.amount
            # Otherwise, add all the dates inbetween the previous and current date
            else:
                if prev is None:
                    print "prev: ", prev
                    inbetween_dates = _dates_inbetween(start_date-datetime.timedelta(days=1), record.date.date())
                else:
                    inbetween_dates = _dates_inbetween(prev.date.date(), record.date.date())
                print "inbetween_dates: ", inbetween_dates
                inbetween_dates_dict = OrderedDict.fromkeys(inbetween_dates, 0)
                print "inbetween_dates_dict: ", inbetween_dates_dict
                date_dict.update(inbetween_dates_dict)
                date_dict[record.date.date()] = record.amount
            last_record = record
        print "date_dict", date_dict

        # Add trailing dates
        if last_record is None:
            trailing_dates = _dates_inbetween(start_date-datetime.timedelta(days=1), end_date+datetime.timedelta(days=1))
        else:
            trailing_dates = _dates_inbetween(record.date.date(), end_date+datetime.timedelta(days=1))
        trailing_dates_dict = OrderedDict.fromkeys(trailing_dates, 0)
        date_dict.update(trailing_dates_dict)

        y = "y%s" % index
        chartdata[y] = map(lambda amount: int(amount), date_dict.values())

        name = "name%s" % index
        chartdata[name] = pet.name

    chartdata['x'] = map(lambda date: int(time.mktime(date.timetuple()) * 1000), date_dict.keys())
    data['chartdata'] = chartdata

    print "chartdata", chartdata
    
    return render_to_response('healthcat/line_graph_with_focus.html', data)

@login_required
def total_bullying_instances(request):
    owner = Owner.objects.filter(user=request.user)
    pets = Pet.objects.filter(owner=owner)
    colors = [pet.encode("utf8") for pet in pets.values_list('color', flat=True)]

    amounts = []
    for pet in pets:
        amounts.append(BullyingRecord.objects.filter(bully=pet).count())
    xdata = pets.values_list("name", flat=True)
    ydata = amounts

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {
        'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
    }
    charttype = "discreteBarChart"
    chartcontainer = 'discretebarchart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {'color': colors}
        }
    }
    return render_to_response('healthcat/bar_chart.html', data)

@login_required
def total_bullied_instances(request):
    owner = Owner.objects.filter(user=request.user)
    pets = Pet.objects.filter(owner=owner)
    colors = [pet.encode("utf8") for pet in pets.values_list('color', flat=True)]

    amounts = []
    for pet in pets:
        amounts.append(BullyingRecord.objects.filter(pet=pet).count())
    xdata = pets.values_list("name", flat=True)
    ydata = amounts

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {
        'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
    }
    charttype = "discreteBarChart"
    chartcontainer = 'discretebarchart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {'color': colors}
        }
    }
    return render_to_response('healthcat/bar_chart.html', data)
