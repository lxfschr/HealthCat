import urllib,urllib2,httplib,json
import time
import random
import pickle,json
import os
from bowl_settings import *

"""
Documentation:

Functions available. 

init()
    This function shall be called to start the interval
    pooling program.


"""


#global data Variables
indexToRfid={}
rfidToIndex={}
schedules = {}


def init():
    # create a new file or read from the existing pickle.
    # check for files

    # while loop
    while (True):

        acquireLock()
        getOrCreateDumps()#loads files from the data.

        updateSchedules()# makes a request to webapp and loads


        stashDumps()# saves files back to data
        releaseLock()


        time.sleep(TIMEGAP) # waits.


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
        if fieldsDict==None :
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
        json.dump({},f1)
        f1.close()

    if not rfidToIndexExists:
        f2= open(rfidToIndexFileName,'w+')
        json.dump({},f2)
        f2.close()

    if not schedulesExists:
        f3= open(schedulesFileName,'w+')
        json.dump({},f3)
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




def acquireLock():
    # set the lock file to 1

    print 'acquiring lock....',
    lockExists= os.path.exists(os.path.join(os.getcwd(),
        lockFileName))
    if not lockExists:
        print 'lock doesnt exist .. creating one..'
        f3= open(lockFileName,'w+')
        # lockdict={}
        # lockdict['lock']='UNLOCKED'
        # json.dump({},f3)
        f3.write('UNLOCKED')
        f3.close()


    fLock= open(lockFileName,'r')

    s=fLock.read()

    while(s == 'LOCKED'):
        fLock.close()
        time.sleep(1)
        fLock= open(lockFileName,'r')
        s=fLock.read()
        print 'trying to acquire lock'

    fLock.close()

    fLock =open(lockFileName,'w+')
    fLock.write('LOCKED')
    fLock.close()
    print 'lock acquired'



def releaseLock():
    # set the lock to 0
    print 'releasing lock...',

    fLock= open(lockFileName,'w+')
    fLock.write('UNLOCKED')
    fLock.close()

    print 'lockReleased'
init
()