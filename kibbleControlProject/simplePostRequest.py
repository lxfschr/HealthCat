
import urllib, urllib2

url = 'http://localhost:8000/healthcat/validate-bowl'
values = {'bowlSerial' : 'CAT123',
          'bowlKey' : 'alphanumeric',
          'validate':'True' }


data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

print response.geturl()
print response.info()
the_page = response.read()
print the_page