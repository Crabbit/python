#!/usr/bin/python

list = [ '1111', '2222', '3333', '4444', '5555' ]

count = 1
for value in list:
	print "Item %d is %s" % (count, value)
	count = count + 1

print 'Item 1 to 3 is    :', list[1:3]
print 'Item 2 to end is  :', list[2:]
print 'Item 1 to -1 is   :', list[1:-1]
print 'Item start to end is :', list[:]
print 'Iterm start to -1 is:', list[:-1]

name = 'abcdefg'
print 'Item 1 to 3 is    :', name[1:3]
print 'Item 2 to end is  :', name[2:]
print 'Item 1 to -1 is   :', name[1:-1]
print 'Item start to end is :', name[:]

