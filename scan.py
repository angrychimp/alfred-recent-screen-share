# -*- coding: utf-8 -*-
import os
import plistlib
import alfred

_MAX_RESULTS = 20
_CACHE_EXPIRY = 24 * 60 * 60 # in seconds
_CACHE = alfred.work(True)

def combine(operator, iterable):
	return u'(%s)' % (u' %s ' % operator).join(iterable)

def results(path, query):
	match = set()
	for root, dirs, files in os.walk(path):
		for file in files:
			if file in match:
				continue
			if file.find(query) > -1:
				match.add(file)
				parts = file.split('.')
				parts.pop()
				title = '.'.join(parts)
				pl = plistlib.readPlist(root+file)
				url = pl.URL
				yield alfred.Item({u'arg': root+file}, title, url, os.getcwd()+"/icon.png")

(path, query) = alfred.args()
alfred.write(alfred.xml(results(path, query), maxresults=_MAX_RESULTS))