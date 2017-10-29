#!/usr/bin/python
#
# Creat Time :Mon 11 Nov 2013 04:40:41 AM GMT
# Author     : lili

class For_sum:
	sum = 0

	def __init__( self, name ):
		'''Initializes the name.'''
		self.name = name
		print '(Initializing %s)' % self.name

		For_sum.sum += 1
	
	def __del__(self):
		'''I'm dying.'''
		print '%s says bye.' % self.name

		For_sum.sum -+ 1

		if For_sum.sum == 0:
			print 'I\'m the last one.'
		else:
			print "There are still %d perple left." % For_sum.sum
	def sayHi(self):
		'''Greeting by person.'''
		print 'Hi, my name is %s.' % self.name
	def howMany(self):
		'''Prints the current population.'''
		if For_sum.sum == 1:
			print 'I\'m the only person here.'
		else:
			print 'We have %d persons here.' % For_sum.sum

lili = For_sum( 'lili' )
lili.sayHi()
lili.howMany()

cici = For_sum( 'cici' )
cici.sayHi()
cici.howMany()

lili.sayHi()
lili.howMany()

