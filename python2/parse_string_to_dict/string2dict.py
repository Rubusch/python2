#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

## parses strings, separated by '=' and ';' (or ',') into dicts

import urlparse
urlparse.parse_qs("Name1=Value1;Name2=Value2;Name3=Value3")

## {'Name2': ['Value2'], 'Name3': ['Value3'], 'Name1': ['Value1']}
print "READY.\n"