import datetime
import time
Dreaded=Exception('boo')

try:
	raise Dreaded
	b = 1/0


except Exception,e:
	print e
	print 'hello'
