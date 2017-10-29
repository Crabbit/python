#!/usr/bin/python

# new_list just point orign_list
orign_list = ['1111','2222','3333','4444','5555']
new_list = orign_list

del orign_list[0]

print "Orign list is ", orign_list
print "new list is ", new_list
print " ".join(orign_list)

# use this operation,copy it, not point it
new_list = orign_list[:]
del new_list[0]

print "Orign list is ", orign_list
print "new list is ", new_list
