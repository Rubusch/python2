#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

arr = [ 'a', 'b', 'c' ]
print arr

out = '.'.join(arr)
print out

print 'having int'
arr = [ 1, 2, 3 ]
print arr

out = '.'.join(["%s" % el for el in arr])
print out

print "READY.\n"
