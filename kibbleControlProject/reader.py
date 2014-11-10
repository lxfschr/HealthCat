import serial
import time
import webapi

STATUS_OK = "01"
RFID = serial.Serial('/dev/ttyAMA0', 9600, timeout=2, writeTimeout=2)


time.sleep(1)
RFID.open()
print "port OPEN. Writing Power Antenna"
RFID.write('\x18\x03\xFF')

while RFID.isOpen():


    # print "Turn on Antenna..."
    # RFID.write('\x18\x03\x00')
    # try:
    #     while RFID.inWaiting() > 0:
    #         fromReader = RFID.read(RFID.inWaiting())
    #         print "fromReader HEX: ", fromReader.encode('hex')
    # except Exception, e:
    #     print "[Errno 5] Input/output error", e
    #     continue
    input = raw_input(">> ")

    if input == 'e':
        print "Turn off Antenna..."
        try:
            RFID.write('\x18\x03\x00')
        except Exception, e:
            print "could not write", e
        print "exit..."
        RFID.close()
        exit()
    elif input == 'a':
        print "Turn on Antenna..."
        try:
            RFID.write('\x18\x03\xFF')
        except Exception, e:
            print "could not send"
        fromReader = ''
        try:
            fromReader = RFID.read(100)
            print "fromReader HEX: ", fromReader.encode('hex')
        except Exception, e:
            print "[Errno 5] Input/output error", e
            continue
    elif input == 'o':
        print "Turn off Antenna..."
        try:
            RFID.write('\x18\x03\x00')
        except Exception, e:
            print "could not send"
        fromReader = ''
        try:
            fromReader += RFID.read(100)  
            if fromReader != '':
                print "fromReader HEX: ", fromReader.encode('hex')
        except Exception, e:
            print "[Errno 5] Input/output error", e
            continue
    elif input == 's':
        print "Scan..."
        try:
            RFID.write('\x43\x04\x01\xCD')
        except Exception, e:
            print "[Errno 5] Input/output error", e
            continue
        fromReader = ''
        try:
            fromReader += RFID.read(100)  
            if fromReader != '':
                print "fromReader HEX: ", fromReader.encode('hex')
                rfid_int = int(fromReader.encode('hex'), 16)
                print "fromReader INT: ", rfid_int
                webapi.connectRFID(rfid_int)
        except Exception, e:
            print "[Errno 5] Input/output error", e
            continue