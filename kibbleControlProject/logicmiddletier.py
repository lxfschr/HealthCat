import controller
import controlFunctions
import webapi
import time

def init():

	#keep reading rfid
	rfidList=[]
	eatTimeStart=None
	eatWeightStart=None

	while (True):

		rfidList = controlFunctions.readRFID()
		numOfCats = len(rfidList)

		if numOfCats==prevNumCats:
			numOfCatsNotChanged +=1

		else:
			numOfCatsNotChanged +=1
			prevNumCats = numOfCats

		if numOfCatsNotChanged>5 and numOfCats == 0:
			makeStateClosed()

		elif  numOfCatsNotChanged> 5 and numOfCats==1:

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
				eatWeightStart=None
			
			elif t>0:
				# case where the  bowl needs to be opened for so many seconds

				if not eatTimeStart:
					eatTimeStart = datetime.datetime.now()
					eatWeightStart = controller.getWeight()
					makeStateOpen()

				else:
					now=datetime.datetime.now()
					weightNow = controller.getWeight()

					if now - eatTimeStart > datetime.datetime(seconds=t)
						and weightNow - eatWeightStart > 10:

						makeStateClosed()
						eatTimeStart=None
						#make logging call here

		else if numOfCatsNotChanged>5 and numOfCats>1:

			makeStateClosed()
			eatTimeStart=None
			eatWeightStart = None
			# make a bullying call here.

		time.sleep(1)

def makeStateOpen():
	if not controlFunctions.isOpen():
		controlFunctions.open()

def makeStateClosed():
	if controlFunctions.isOpen():
		controlFunctions.close()

def refillBowl():

	makeStateClosed()
	controlFunctions.refill()