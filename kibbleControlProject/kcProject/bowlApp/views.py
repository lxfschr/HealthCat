from django.shortcuts import render,redirect,get_object_or_404
from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist

#decorator to use built-in auth system
from django.contrib.auth.decorators import login_required

#more auth for loggin in manually
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

from grumblr.models import *
from grumblr.forms import *

from django.db import transaction# Create your views here.

from itertools import chain

from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.core.mail import send_mail
from django.core import serializers

from django.contrib.auth.tokens import default_token_generator


# to make http requests. 
import urllib2,urllib,httplib

###########################################################################


def openornot(rfidID,timenow,YYYYMMDD):

	responseDict= {}

	if openornotLogic(catID,timenow,YYYYMMDD):
		responseDict['result'] = 'true'

		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')
	else:
		responseDict['result'] = 'false'

		return HttpResponse(json.dumps(responseDict),
			content_type='application/json')		


# this holds the logic
def openornotLogic(catID,timenow,YYYYMMDD):
	# having a simple logic now. 
	# if its day time open else close for any cat. 
	return timenow >800 and timenow< 2200


# making logs of when the cat ate.
def catJustAte(amount,timeStart,timeEnd,YYYYMMDD):
	urltopost="http://healthcat.herokuapp.com/record"
	data= urllib2.urlencode({'amount':amount, 'tStart':timeStart, 
							'tEnd':timeEnd, 'YYYYMMDD':YYYYMMDD})
	headers = {"content_type": "application/x-www-form-urlencoded",
				"Accept":"text/plain"}

	h.request('POST', urltopost ,data,headers)


	pass





