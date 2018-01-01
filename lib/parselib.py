#!/usr/bin/env python

import os
import re

def charset_path(*paths):
	return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', *paths))

class cd:
	def __init__(self, path):
		self.newPath = path

	def __enter__(self):
		self.oldPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.oldPath)

def ls(path):
	for f in os.listdir(path):
		if f[0] != '.':
			f = os.path.join(path, f)
			if os.path.isfile(f):
				yield f
			if os.path.isdir(f):
				for f in ls(f):
					yield f

class atline_matcher:
	def __init__(self, keyword):
		self.m = re.compile('^\\s*@%s\\s+' % re.escape(keyword), re.IGNORECASE)
		self.s = re.compile('^\\s*@%s\\s+|\\s*#.*$' % re.escape(keyword), re.IGNORECASE)

	def match(self, line):
		if self.m.match(line):
			return self.s.sub('', line)
		else:
			return None

__is_atline = re.compile('^\\s*@')
def is_atline(line):
	return __is_atline.match(line) is not None

__is_comment = re.compile('^\\s*#')
def is_comment(line):
	return __is_comment.match(line) is not None

__strip_comment = re.compile('\\s*#.*$')
def strip_comment(line):
	return __strip_comment.sub('', line)

__import_matcher = atline_matcher('import')
def expand(path, strip_atlines=False, strip_comments=False):
	with open(path, 'r') as f:
		for line in f:
			line = line.rstrip()
			path = __import_matcher.match(line)
			if path is not None:
				for line in expand(path, strip_atlines, strip_comments):
					yield line
			elif strip_atlines and is_atline(line):
				pass
			elif not strip_comments:
				yield line
			elif not is_comment(line):
				yield strip_comment(line)

__mapline_matcher = re.compile('^\\s*([0][Xx][0-9A-Fa-f]+)\\s+([0][Xx][0-9A-Fa-f]+([+][0][Xx][0-9A-Fa-f]+)*)')
def split_mapline(line):
	m = __mapline_matcher.match(line)
	if m is None: return (None, None)
	bytes = [int(m.group(1)[i:i+2], 16) for i in range(2, len(m.group(1)), 2)]
	chars = [int(cp[2:], 16) for cp in m.group(2).split('+')]
	return (bytes, chars)
