#!/usr/bin/python
# filename: function.py

def sayHello( name = 'lili',times = 2,):
#Doc strings
	'''Study the function.'''
	global date
	print 'Hello python.'
	print 'times = ',times
	print 'Hello',name * times
	print 'Hello',date
	print '-------------'

def max(x = 0, y = 0):
	'''Print the lager number.'''
	if x > y:
		return x
	else:
		return y

date = 621
sayHello( 'lili' )
sayHello( 'lili' , 5)
sayHello( times = 5, name = 'lili' )

print 'The max number is ',max(y = 5, x = 10)
print sayHello.__doc__
print max.__doc__
