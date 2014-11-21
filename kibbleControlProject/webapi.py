import urllib,urllib2,httplib,json
import time
import random
import pickle,json
import os
import datetime
import re
from bowl_settings import *


"""
Documentation:

Functions available. 

newRfidDetected(index)
	
	This function shall be called whenever you detect a new RFID.
	The index number should be a new number. 
	REQUIRES: index to be integer.
			  index should not have been an integer allocated 
			  previously to a different pet.
	ENSURES:  Sends a request to server if connected to internet
			  Which then sends an email to user.
			  returns 0 if fail, including internet disConnects.
			  returns 1 if success

openOrNot(index)

	This function shall be called when a cat walks nearby/
	an old rfid is detected.

	REQUIRES: index to be integer.
			  index must be an integer allocated

	ENSURES:  returns an integer indicating amount of food to 
			  be fed.
			  0 indicates no food to be fed.



validateBowl()
	This function shall be called when a connect button is pressed on bowl

unValidateBowl()
	This function shall be called after a set time after a validateBowl() 
	is called. this unvalidates the bowl.



petJustAte(index,amount)
	
	This function shall be called when a pet moves away from the
	bowl.

	REQUIRES: index to be integer.
			  index must be an integer allocated

	ENSURES:  An entry shall be added to the log.


"""



#global data Variables
indexToRfid={}
rfidToIndex={}
schedules = {}


def generateRandomID():
	power=RFID_LENGTH-1
	return random.randint(10**power,10**(power+1)-1)


def newRfidDetected(index):

	global indexToRfid,rfidToIndex,schedules

	getOrCreateDumps()
	
	if str(index) in indexToRfid:
		print ' old index being used'
		return 0 # an old index is not allowed

	#get a unique random ID
	a=generateRandomID()

	while(a in rfidToIndex):
		a=generateRandomID()

	# assign the unique ID to the current index and update dicts.
	indexToRfid[index]=a
	rfidToIndex[a]=index
	schedules[a]=[]
	print  'ereaerea'
	try:
		# send a request to application on web.
		r=urllib2.urlopen(HOST+'new-rfid-detected/'+BOWLSERIAL+'/'+str(a)).read()
		stashDumps()
		return 1
	except:
		# rollback: delete the newly added keys to the dicts.
		indexToRfid.pop(index,None)
		rfidToIndex.pop(a,None)
		schedules.pop(a,None)
		print "No Internet Connection"
		return 0

	print "ERR10: No Case should come here"
	return 0



def openOrNot(index):

	global indexToRfid,rfidToIndex,schedules

	getOrCreateDumps()	

	if str(index) not in indexToRfid:
		return 0 # an new index is not allowed

	# get the rfid based on index
	rfid=indexToRfid[str(index)]

	# get the schedules based on rfid.
	intervals = schedules[str(rfid)]

	# for each interval check if the current time falls in it.
	timenow = datetime.datetime.now().strftime("%H:%M")
	# timenow = datetime.datetime(2009, 1, 6, 19, 8, 24, 78915).strftime("%H:%M")

	timenowRE=re.match(r'^(?P<hour>\d\d):(?P<minute>\d\d)$',timenow)
	timenowHH=timenowRE.group('hour')
	timenowMM=timenowRE.group('minute')
	timenowNum=int(timenowHH+timenowMM)

	for interval in intervals:
		print 'checking interval....', interval
		amount=interval[0]

		timeStart=interval[1]
		timeStartRE=re.match(r'^(?P<hour>\d\d):(?P<minute>\d\d):(?P<sec>\d\d)$',
			timeStart)
		timeStartHH=timeStartRE.group('hour')
		timeStartMM=timeStartRE.group('minute')
		timeStartNum=int(timeStartHH+timeStartMM)

		timeEnd=interval[2]
		timeEndRE=re.match(r'^(?P<hour>\d\d):(?P<minute>\d\d):(?P<sec>\d\d)$',
			timeEnd)
		timeEndHH=timeEndRE.group('hour')
		timeEndMM=timeEndRE.group('minute')
		timeEndNum=int(timeEndHH+timeEndMM)
		
		if timenowNum>=timeStartNum and timenowNum<=timeEndNum:
			return amount
	return 0

def petJustAte(index,amount):
	#tries to send the info right away. if the internet connection fails
	# stores in a local log file
	timenow= datetime.datetime.now().strftime("%Y%m%d%H%M")

	

def validateBowl():
	validation_helper('True')

def unValidateBowl():
	validation_helper('False')


def validation_helper(arg):
	url = HOST+'validate-bowl'
	values = {'bowlSerial' : BOWLSERIAL,
	          'bowlKey' : BOWL_KEY,
	          'validate':arg }


	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	return 1













####################################################################
# functions to open and close data files
####################################################################

def getOrCreateDumps():
	print 'reading dumps...'
	cwd = os.getcwd()
	indexToRfidExists= os.path.exists(os.path.join(os.getcwd(),
		indexToRfidFileName))
	rfidToIndexExists= os.path.exists(os.path.join(os.getcwd(),
		rfidToIndexFileName))
	schedulesExists= os.path.exists(os.path.join(os.getcwd(),
		schedulesFileName))

	# if paths dont exist create a file
	if not indexToRfidExists:
		f1= open(indexToRfidFileName,'w+')
		json.dump(indexToRfid,f1)
		f1.close()

	if not rfidToIndexExists:
		f2= open(rfidToIndexFileName,'w+')
		json.dump(rfidToIndex,f2)
		f2.close()

	if not schedulesExists:
		f3= open(schedulesFileName,'w+')
		json.dump(schedules,f3)
		f3.close()

	# if paths exist. load from the dumps.
	loadDumps()


def loadDumps():

	print 'loading files....'
	global indexToRfid,rfidToIndex,schedules

	# open the files and dump
	f1= open(indexToRfidFileName,'r+')
	indexToRfid=json.load(f1)
	f1.close()

	f2= open(rfidToIndexFileName,'r+')
	rfidToIndex=json.load(f2)
	f2.close()

	f3= open(schedulesFileName,'r+')
	schedules=json.load(f3)
	f3.close()

	# return [indexToRfid,rfidToIndex,schedules]




def stashDumps():

	print 'saving files....'
	global indexToRfid,rfidToIndex,schedules

	# open the files and dump
	f1= open(indexToRfidFileName,'w+')
	json.dump(indexToRfid,f1)
	f1.close()

	f2= open(rfidToIndexFileName,'w+')
	json.dump(rfidToIndex,f2)
	f2.close()

	f3= open(schedulesFileName,'w+')
	json.dump(schedules,f3)
	f3.close()


#############################################
# decpricated Documentation
############################################
"""
updateSchedules()

This function shall be called when a manual request for 
update in schedules needs to be made. (We can have a button
on the bowl, which when pressed, shall call this function.
Advantages : bowl can work at lower frequency of update 
schedule requests like say one request per hour)
"""