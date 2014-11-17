import urllib,urllib2,httplib,json
import time
import random
import pickle,json
import os

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


petJustAte(index,amount)
	
	This function shall be called when a pet moves away from the
	bowl.

	REQUIRES: index to be integer.
			  index must be an integer allocated

	ENSURES:  An entry shall be added to the log.


"""


HOST= "http://localhost:8000/healthcat/"
# HOST= "http://frozen-brushlands-8463.herokuapp.com/healthcat/"
RFID_LENGTH = 6
# make a request for getting all the schedules every 3 secs
TIMEGAP=3
BOWLSERIAL='CAT123'

#pickle file names
indexToRfidFileName='itr.txt'
rfidToIndexFileName='rti.txt'
schedulesFileName='sch.txt'

#global data Variables
indexToRfid={}
rfidToIndex={}
schedules = {}


def init():
	# create a new file or read from the existing pickle.
	# check for files
	getOrCreateDumps()

	# while loop
	while (True):
		updateSchedules()
		stashDumps()
		time.sleep(TIMEGAP)




def updateSchedules():

	print 'making a request..'

	#make a request to get schedules for all cats in dict.

	for rfid in rfidToIndex:
		try:
			r=urllib2.urlopen(HOST+'get-feeding-intervals/'+str(rfid)).read()
			processJSONResponse(r,rfid)
			print 'request made'
		except:
			print 'request failed'
			continue

def processJSONResponse(response,rfid):
	inputDict=json.loads(response)
	newIntervalList=[]
	for entry in inputDict:
		#see the fields of the JSON object
		fieldsDict= entry.get('fields',None)
		if fieldsDict==None	:
			print "No fields in 'fields' ...."
			continue
		try:

			amount= fieldsDict['amount']
			timeStart= fieldsDict['start']
			timeEnd= fieldsDict['end']
		except:
			print 'problem in JSON. check dict.'
			continue

		interval= [amount,timeStart,timeEnd]
		newIntervalList.append(interval)

	#replace the existing list for the pet.
	schedules[rfid]=newIntervalList















####################################################################
# functions to open and close data files
####################################################################

def getOrCreateDumps():
	# print 'reading dumps...'
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

	# print 'loading files....'
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

	# print 'saving files....'
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

init()