import serial
import time
import datetime
import webapi
import bowl
import controlFunctions as cf
import RPi.GPIO as GPIO
import sets

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

RFID_CHK_FREQ = 1000 #millisec
NUM_SNAPSHOTS = 5


def init():
    dTime = datetime.timedelta(milliseconds=RFID_CHK_FREQ)
    prevTime = datetime.datetime.now()

    snapshotList=[[]]*NUM_SNAPSHOTS

    while True:
        if(GPIO.input(23)):
            webapi.validateBowl()
        
        nowTime = datetime.datetime.now()
        if nowTime - prevTime > dTime:
            prevTime = nowTime

            #get rfid snapshot
            snapshot = cf.readRFID()

            #enque and deque
            snapshotList.append(snapshot)
            snapshotList.pop(0)

            if shouldBowlClose(snapshotList) :
                cf.close()
            else:
                cf.open()


def shouldBowlClose(snapshotList):

    #get all cats from the list
    catsList = getCatsFromSnapShotList(snapshotList)
    if len(catsList)==0:
        return False
    elif len(catsList)>1:
        webapi.bullyNotify(catsList)
        return False
    elif len(catsList)==1:
        #at this moment not evven considering time intervals
        t = webapi.openOrNot(catsList[0])
        if t==-1:
            webapi.newRfidDetected(catsList[0])
            return False
        return t==0



def getCatsFromSnapShotList(snapshotList):
    s= sets.Set()
    for snapshot in snapshotList:
        for cat in snapshot:
            s.add(cat)
    return list(s)

def testGetCatsFromSnapShotList():
    print getCatsFromSnapShotList([[0]])


def getRfidsNearby():

    listoflists=[]

    #use five iterations 150ms apart
    for i in range(5):
        listoflists.append(cf.readRFID())


init()
