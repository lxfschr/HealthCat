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

	try:
		# send a request to application on web.
		r=urllib2.urlopen(HOST+'register-rfid/'+str(a)).read()
		return 1
	except:
		# rollback: delete the newly added keys to the dicts.
		indexToRfid.pop(index,None)
		rfidToIndex.pop(a,None)
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

		#make a request to get schedules.
		r=urllib2.urlopen(HOST+'get-/'+str(rfid)).read()
		




		# make a request for getting all the schedules every 1 hour.
		time.sleep(3600)



def updateSchedules():
	pass

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
		json.dumps(indexToRfid,f)

	if not rfidToIndexExists:
		f= open(rfidToIndexFileName,'r+')
		json.dumps(rfidToIndex,f)

	if not schedulesExists:
		f= open(schedulesFileName,'r+')
		json.dumps(schedules,f)


	# if paths exist. load from the dumps.
	f1= open(indexToRfidFileName,'r+')
	indexToRfid=json.load(f1)

	f2= open(rfidToIndexFileName,'r+')
	rfidToIndex=json.load(f2)

	f3= open(schedulesFileName,'r+')
	schedules=json.load(f3)


