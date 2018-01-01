#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import atline_matcher, cd, charset_path, expand, is_atline, ls

__generate_matcher = atline_matcher('generate-txt')
def generate(inpath, outpath):
	txt = None
	lines = []
	for line in expand(inpath):
		t = __generate_matcher.match(line)
		if t is not None:
			txt = t
		elif not is_atline(line):
			lines.append(line)
	if txt is None:
		return None
	else:
		path = os.path.join(outpath, txt)
		parent = os.path.dirname(path)
		if not os.path.exists(parent):
			os.makedirs(parent)
		with open(path, 'w') as f:
			for line in lines:
				print(line, file=f)
		return path

__index_name = 'index.php'
__index_content = """<?php
require_once (stripslashes($_SERVER['DOCUMENT_ROOT']) . '/static/dirlister.php');
site_generate_index();"""

def create_index(path):
	path = os.path.join(path, __index_name)
	if not os.path.exists(path):
		with open(path, 'w') as f:
			f.write(__index_content)

def create_indices(path):
	create_index(path)
	for f in os.listdir(path):
		if f[0] != '.':
			f = os.path.join(path, f)
			if os.path.isdir(f):
				create_indices(f)

def main():
	mappings = charset_path('out', 'MAPPINGS')
	with cd(charset_path('mappings')):
		for path in ls('.'):
			out = generate(path, mappings)
			if out is not None:
				print('mappings/%s -> %s' % (path[2:], out))
	create_indices(mappings)
	puadata = charset_path('out', 'PUADATA')
	with cd(charset_path('puadata')):
		for path in ls('.'):
			out = generate(path, puadata)
			if out is not None:
				print('puadata/%s -> %s' % (path[2:], out))
	create_indices(puadata)

if __name__ == '__main__':
	main()
