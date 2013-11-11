#!/usr/bin/python
 #
 # Creat Time :Tue 05 Nov 2013 06:10:28 AM GMT
 # Autoor     : lili

class My_first_method:
 __'''init__ method can initialization'''
	def __init__(self, name1, name2):
		self.name1 = name1
		self.name2 = name2
	def say(self):
		print '%s love %s.' % (self.name1, self.name2)

p = My_first_method('lili', 'cici')
p.say()
