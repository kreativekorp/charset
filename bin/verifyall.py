#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from acquisitionlib import acquire
from parselib import atline_matcher, cd, charset_path, expand, ls, split_mapline

__verify_matcher = atline_matcher('verify-against')
def verify(path):
	url = None
	map = {}
	for line in expand(path):
		u = __verify_matcher.match(line)
		if u is not None:
			url = u
		else:
			b, c = split_mapline(line)
			if b is not None and c is not None:
				map[tuple(b)] = tuple(c)
	if url is None:
		return None
	else:
		expmap = {}
		with open(acquire(url), 'r') as f:
			for line in f:
				b, c = split_mapline(line)
				if b is not None and c is not None:
					expmap[tuple(b)] = tuple(c)
		return map == expmap

def main():
	with cd(charset_path('mappings')):
		for path in ls('.'):
			result = verify(path)
			if result is not None:
				print('mappings/%s: %s' % (path[2:], 'PASSED' if result else 'FAILED'))
	with cd(charset_path('puadata')):
		for path in ls('.'):
			result = verify(path)
			if result is not None:
				print('puadata/%s: %s' % (path[2:], 'PASSED' if result else 'FAILED'))

if __name__ == '__main__':
	main()
