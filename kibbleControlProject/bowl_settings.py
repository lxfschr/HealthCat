HOST= "http://localhost:8000/healthcat/"
# HOST= "http://frozen-brushlands-8463.herokuapp.com/healthcat/"
RFID_LENGTH = 6
# make a request for getting all the schedules every 15 secs
TIMEGAP=20
BOWLSERIAL='CA123T'
BOWL_KEY = 'alpha'

#pickle file names
indexToRfidFileName='itr.txt'
rfidToIndexFileName='rti.txt'
schedulesFileName='sch.txt'

lockFileName = 'rwlock.txt'