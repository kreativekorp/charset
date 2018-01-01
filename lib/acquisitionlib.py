#!/usr/bin/env python

import os
import re
import subprocess

from parselib import charset_path

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
