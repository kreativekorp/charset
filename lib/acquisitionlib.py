#!/usr/bin/env python

import os
import re
import subprocess

def charset_path(*paths):
	return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', *paths))

def cache_path(url=None):
	path = charset_path('.charset-cache')
	if not os.path.exists(path):
		os.mkdir(path)
	if url is not None:
		url = re.sub('[ !\"\'+,/:;\\^`|~]', '-', url)
		url = re.sub('[^A-Za-z0-9_.-]', '$', url)
		path = os.path.join(path, url)
	return path

def acquire(url):
	path = cache_path(url)
	args = ['curl', '-s', url, '-o', path]
	if os.path.exists(path):
		args.append('-z')
		args.append(path)
	subprocess.check_call(args)
	return path
