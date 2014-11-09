from django.shortcuts import render,redirect,get_object_or_404
from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist

#decorator to use built-in auth system
from django.contrib.auth.decorators import login_required

#more auth for loggin in manually
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

from bowlApp.models import *
# from bowlApp.forms import *

from django.db import transaction# Create your views here.

from itertools import chain

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.core.mail import send_mail
from django.core import serializers

from django.contrib.auth.tokens import default_token_generator


# to make http requests. 
import urllib2,urllib,httplib,json

#time related library
import time, datetime

###########################################################################

BOWLID = ABC12

def openornot(request,rfid,timenow,YYYYMMDD):

	responseDict= {}

	if openornotLogic(rfid,int(timenow),YYYYMMDD):
		responseDict['result'] = 'true'

		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')
	else:
		responseDict['result'] = 'false'

		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')		


# this holds the logic
# it should return true if the bowl can open else not.
def openornotLogic(rfid,timenow,YYYYMMDD):

	# having a simple logic now. 
	# if its day time open else close for any cat.
	return timenow >800 and timenow< 2200

# making logs of when the cat ate.
def catJustAte(request, amount,timeStart,timeEnd,YYYYMMDD):

	urltopost="http://healthcat.herokuapp.com/record"
	data= urllib2.urlencode({'amount':amount, 'tStart':timeStart, 
							'tEnd':timeEnd, 'YYYYMMDD':YYYYMMDD})
	conn= httplib.HTTPConnection(urltopost)
	headers = {"content_type": "application/x-www-form-urlencoded",
				"Accept":"text/plain"}

	conn.request('POST','/record',data,headers)
	response= conn.getresponse()
	pass


def createPet(request,rfid):

	#validation for rfid

	#new pet creation
	newPet=Pet(rfid=rfid)
	newPet.save()
	responseDict={}
	responseDict['result']='Success'
	responseDict['petID'] = newPet.id

	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')	

def createSchedule(request,nameOfSch):

	newFoodSch= FoodSchedule()
	newFoodSch.name=nameOfSch
	newFoodSch.save()

	#respond with schID
	responseDict={}
	responseDict['result'] = 'success'
	responseDict['schID'] = newFoodSch.id

	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')	

def updateScheduleAdd(request,schID,timein,timeout,amount):
	# validating the timein timeout and amount .

	# convert time in to timestamp
	timein,timeout=int(timein),int(timeout)
	dtTimeIn = datetime.time(timein/100,timein%100)
	dtTimeOut = datetime.time(timeout/100,timeout%100)

	# make a new schedule and add it to a pet.
	responseDict={}
	try:
		fs = FoodSchedule.objects.get(id=schID)
	except:
		responseDict['result'] = 'Fail'
		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')


	newTimeAmountWindow= TimeAmountWindow(timeOpen=dtTimeIn,
			timeClose=dtTimeOut,amount=amount,relatedSchedule=fs)
	newTimeAmountWindow.save()
	responseDict['result'] = 'success'
	responseDict['tawID'] = newTimeAmountWindow.id

	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')


def updateScheduleRemove(request,tawID):
	# validating the timein timeout and amount .

	# make a new schedule and add it to a pet.
	responseDict={}
	try:
		fs = TimeAmountWindow.objects.get(id=schID)
	except:
		responseDict['result'] = 'Fail'
		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')


	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')

def assignPetASchedule(request,rfid,schID):

	responseDict={}
	try:
		fs = FoodSchedule.objects.get(id=schID)
		p = Pet.objects.get(rfid=rfid)
	except:
		responseDict['result'] = 'Fail'
		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')
	p.foodSchedule_set(fs)
	responseDict['result'] = 'Success'
	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')


def connect(request):
	
	responseDict={}
	responseDict['result'] = 'Success'
	responseDict['bowlID'] = BOWLID

	return HttpResponse(json.dumps(responseDict),
		content_type='application/json')

# this function is called upon a connection of new rfid at the bowl.
# it should send a request to webserver saying this rfid is detected at bowl.
def registerRFID(request,rfid):
	print ' In request making'

	r= urllib2.urlopen("http://frozen-brushlands-8463.herokuapp.com/new-rfid-detected/"+BOWLID+"/"+rfid)
	response = r.read()
	pass

