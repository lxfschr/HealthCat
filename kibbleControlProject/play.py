import sets
import copy

a=  [[]]*5
a[3]=[10,2,3]
a[1]=[2,3]
# print a

def f1(num):
	def f2(lis):
		if num in lis:
			return True
		return False
	return f2

# print f1(10)([1,2])
# print map(f1(2),a)

a= sets.Set()
a.add(1)
a.add(1)

a.add('helllo')
a.add('helllo')
a.add('helllasdfo')

print list(a)

