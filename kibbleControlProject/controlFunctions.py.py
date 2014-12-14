import serial
import time
import webapi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


tagReturnLen = 44

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
RFID=serial.Serial('/dev/ttyACM0', 4800, xonxoff=True)
start_time=time.time()



time.sleep(1)
RFID.open()
time.sleep(1)
print "port OPEN"


def getWeight():
    RFID.write('w')
    weight=0
    while RFID.inWaiting():
        weight = RFID.readline()
    return weight

def close():
    RFID.write('c')

def refill():
    RFID.write('f')

def open():
    RFID.write('o')

def isOpen():
    RFID.write('s')
    while RFID.inWaiting():
        state = RFID.readline()
    return state

def readRFID():

    RFID.write('r')
    lineRead = ''
    while RFID.inWaiting():
        try :
            lineRead += RFID.readline()
        except Exception,e :
            print 'Input error'
            continue

    tagsFound = len(lineRead)/tagReturnLen
    tagList=[]

    for i in xrange(tagsFound):
        print i
        tagList.append(lineRead[20+(tagReturnLen*i):tagReturnLen+(tagReturnLen*i)])

    return tagList