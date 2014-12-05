import controller
import webapi
import time

def init():

	#keep reading rfid
	rfidList=[]
	eatTimeStart=None
	while (True):

		rfidList = controller.readRFID()
		numOfCats = len(rfidList)

		if numOfCats == 0:
			makeStateClosed()
		else if numOfCats==1:
			# get the rfid and see if it is valid
			rfid = rfidList[0]

			t= webapi.openOrNot(rfid)
			if (t==-1):
				# case where the new rfid needs to be created
				result =newRfidDetected(rfid)
				print result + ' is the result 1 means new rfid created 0 means not'
			
			elif t==0:
				# bowl should not be opened its 0 grams or seconds
				makeStateClosed()
				eatTimeStart=None
			
			elif t>0:
				# case where the  bowl needs to be opened for so many seconds

				if not eatTimeStart:
					eatTimeStart = datetime.datetime.now()
					makeStateOpen()
				else:
					now=datetime.datetime.now()
					if now - eatTimeStart>datetime.datetime(seconds=t):
						makeStateClosed()
						eatTimeStart=None


				#open bowl

				#




		else if numOfCats>1:

			makeStateClosed()
			eatTimeStart=None
			# make a bullying call here.

		time.sleep(1)





def makeStateOpen():
	if controller.state() == 'CLOSED':
		controller.open()

def makeStateClosed():
	if controller.state() == 'OPEN':
		controller.close()
