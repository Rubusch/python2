#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

x = int(raw_input("enter an integer: "))
if x < 0:
    x = 0
    print 'negative changed to zero'
elif x == 0:
    print 'zero'
elif x == 1:
    print 'single'
else:
    print 'value is: ', x

print "READY.\n"