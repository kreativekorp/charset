#!/usr/bin/env python3

import os
import re
import subprocess
import sys

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

def acquire(url, version='auto', ua='Mozilla/5.0', compressed=False):
	path = cache_path(url)
	path_exists = os.path.exists(path)
	if version == 'local' and path_exists:
		return path
	else:
		args = ['curl', '-L', '-s', url, '-o', path]
		if version != 'remote' and path_exists:
			args.append('-z')
			args.append(path)
		if ua:
			args.append('-A')
			args.append(ua)
		if compressed:
			args.append('--compressed')
		subprocess.check_call(args)
		return path

def add_syspath(*paths):
	sys.path.append(charset_path(*paths))
