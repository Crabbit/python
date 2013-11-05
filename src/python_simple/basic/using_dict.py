#!/usr/bin/python

info = {	'lili'	:	'A linuxer.',
		'cici'	:	'A comicer',
		'Rela'	:	'lover',
		'Time'	:	'Two years',
	}

print "Editor is %s" % info['lili']

#Add a new key-value
info['local'] = "Xi'an -- Nanchang" 

del info['Time']

print "\nThere are %d contacts in the information." % len(info)

for value1, value2 in info.items():
	print 'Contact %s -- %s.' %(value1,value2)

if 'local' in info:
	print "Value1 is %s" % info['local']
