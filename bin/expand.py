#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import cd, expand

def main():
	strip_atlines = False
	strip_comments = False
	prefix = None
	i = 1
	while i < len(sys.argv):
		arg = sys.argv[i]
		i += 1
		if arg == '--help':
			print('usage: expand.py [<options>] <filename> [...]')
			print('  -a        strip metadata')
			print('  +a        keep metadata (default)')
			print('  -c        strip comments')
			print('  +c        keep comments (default)')
			print('  -d path   change directory before processing files')
		elif arg == '-a':
			strip_atlines = True
		elif arg == '+a':
			strip_atlines = False
		elif arg == '-c':
			strip_comments = True
		elif arg == '+c':
			strip_comments = False
		elif arg == '-d' and i < len(sys.argv):
			prefix = sys.argv[i]
			i += 1
		elif prefix is None:
			for line in expand(arg, strip_atlines, strip_comments):
				print(line)
		else:
			with cd(prefix):
				for line in expand(arg, strip_atlines, strip_comments):
					print(line)

if __name__ == '__main__':
	main()
