#!/usr/bin/python

name = 'lili'
real_number = 621

inputname = str(raw_input('Enter you name '))

if inputname == name:
    print '______Welcome Admin.______'
    print '______~~~~~~~~~~~~~~______'
else:
    print "Welcome",inputname

while 1:
	guess_number = int( raw_input( 'Enter you guess number:' ) )
	if guess_number == real_number:
		print "Congratulations,you guessed it."
		break
	else:
		if guess_number < real_number:
			print "Sorry, it's too low"
		else:
			print "Sorry, it's too high"
