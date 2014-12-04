import datetime
import time

d = datetime.datetime.now()
time.sleep(2)
d2 = datetime.datetime.now()

p=datetime.timedelta(seconds=1)

print d2-d<p
