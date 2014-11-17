import urllib,urllib2,httplib,json
import time
import random
import pickle,json

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

updateSchedules()

	This function shall be called when a manual request for 
	update in schedules needs to be made. (We can have a button
	on the bowl, which when pressed, shall call this function.
	Advantages : bowl can work at lower frequency of update 
	schedule requests like say one request per hour)


petJustAte(index,amount)
	
	This function shall be called when a pet moves away from the
	bowl.

	REQUIRES: index to be integer.
			  index must be an integer allocated

	ENSURES:  An entry shall be added to the log.


"""


HOST= "http://localhost:8000/"
# HOST= "http://frozen-brushlands-8463.herokuapp.com/"
RFID_LENGTH = 6
# make a request for getting all the schedules every 1 hour.
TIMEGAP=3600 


#pickle file names
indexToRfidFileName='itr'
rfidToIndexFileName='rti'
schedulesFileName='sch'

#global data Variables
indexToRfid=dict()
rfidToIndex=dict()
schedules = dict()



def generateRandomID():
	power=RFID_LENGTH-1
	return random.randint(10**power,10**(power+1)-1)


def connectRFID(index):

	if index in indexToRfid:
		return 0 # an old index is not allowed

	#get a unique random ID
	a=generateRandomID()
	while(a in rfidToIndex):
		a=generateRandomID()

	# assign the unique ID to the current index and update dicts.
	indexToRfid[index]=a
	rfidToIndex[a]=index
	schedules[a]=[]

	try:
		# send a request to application on web.
		r=urllib2.urlopen(HOST+'register-rfid/'+str(a)).read()
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




def init():
	# create a new file or read from the existing pickle.
	# check for files
	getOrCreateDumps()

	# while loop
	while (True):

		updateSchedules()
		time.sleep(TIMEGAP) 



def updateSchedules():

	#make a request to get schedules for all cats in dict.
	for rfid in rfidToIndex:
		try:
			r=urllib2.urlopen(HOST+'get-feeding-intervals/'+str(rfid)).read()
			processJSONResponse(r,rfid)
		except:
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



def getOrCreateDumps():
	cwd = os.getcwd()
	indexToRfidExists= os.path.exists(os.path.join(os.getcwd(),
		indexToRfidFileName))
	rfidToIndexExists= os.path.exists(os.path.join(os.getcwd(),
		rfidToIndexFileName))
	schedulesExists= os.path.exists(os.path.join(os.getcwd(),
		schedulesFileName))

	# if paths dont exist create a file
	if not indexToRfidExists:
		f= open(indexToRfidFileName,'r+')
		json.dump(indexToRfid,f)
		f.close()

	if not rfidToIndexExists:
		f= open(rfidToIndexFileName,'r+')
		json.dump(rfidToIndex,f)
		f.close()

	if not schedulesExists:
		f= open(schedulesFileName,'r+')
		json.dumps(schedules,f)
		f.close()

	# if paths exist. load from the dumps.
	stashDumps()


def stashDumps():
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

