import serial
import time
import datetime
import webapi
import RPi.GPIO as GPIO
import sets
GPIO.setmode(GPIO.BCM)

button = 18
red1 = 23
green1 = 24
blue1 = 25

GPIO.setup(red1, GPIO.OUT) #setup all the pins  
GPIO.setup(green1, GPIO.OUT)  
GPIO.setup(blue1, GPIO.OUT)  

red2 = 27
green2 = 17
blue2 = 22

GPIO.setup(red2, GPIO.OUT) #setup all the pins  
GPIO.setup(green2, GPIO.OUT)  
GPIO.setup(blue2, GPIO.OUT)  

Freq = 100 #Hz 

#setup all the colours  
RED1 = GPIO.PWM(red1, Freq) #Pin, frequency  
RED1.start(0) #Initial duty cycle of 0, so off  
GREEN1 = GPIO.PWM(green1, Freq)    
GREEN1.start(0)   
BLUE1 = GPIO.PWM(blue1, Freq)  
BLUE1.start(0)  

#setup all the colours  
RED2 = GPIO.PWM(red2, Freq) #Pin, frequency  
RED2.start(0) #Initial duty cycle of 0, so off  
GREEN2 = GPIO.PWM(green2, Freq)    
GREEN2.start(0)   
BLUE2 = GPIO.PWM(blue2, Freq)  
BLUE2.start(0)  


GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


def colour1(R, G, B):  
  #colour brightness range is 0-100  
  RED1.ChangeDutyCycle(R)  
  GREEN1.ChangeDutyCycle(G)  
  BLUE1.ChangeDutyCycle(B) 

def colour2(R, G, B):
  #colour brightness range is 0-100  
  RED2.ChangeDutyCycle(R)  
  GREEN2.ChangeDutyCycle(G)  
  BLUE2.ChangeDutyCycle(B) 

RFID_CHK_FREQ = 1000 #millisec
NUM_SNAPSHOTS = 50


colour1(100,0,0)

def init(rocky, patra, validated):
    dTime = datetime.timedelta(milliseconds=RFID_CHK_FREQ)
    prevTime = datetime.datetime.now()
    checked = False
    changeLight = 0
    time.sleep(1)
    while True:
        if (validated and checked==False): colour1(0,0,100)
        if (validated): checked = True
        if(GPIO.input(button)):
            validated = True

        nowTime = datetime.datetime.now()
        if nowTime - prevTime > dTime:
            prevTime = nowTime
            if (rocky and patra):
                if(changeLight==0): colour2(60,20,0)
                else: colour2(40,60,5)
                changeLight = (changeLight+1)%2
                # print "both"
                print changeLight
            elif (rocky): 
                colour2(60,20,0)
                # print "roc"
            elif (patra): 
                colour2(40,60,5)
                # print "pat"
            else: 
                colour2(0,0,0)
                # print "none"





