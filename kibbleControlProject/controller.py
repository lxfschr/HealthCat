import serial
import time
import webapi
import bowl
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
    if(GPIO.input(23)):
    	print 'button pressed'
        webapi.validateBowl()

