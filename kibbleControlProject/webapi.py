import urllib,urllib2,httplib,json

def connectRFID(rfid):
	r=urllib2.urlopen('http://localhost/register-rfid/'+str(rfid)).read()
	print r
	return