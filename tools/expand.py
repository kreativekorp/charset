#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

def expand(path, strip_atlines, strip_comments):
	with open(path, 'r') as f:
		for line in f:
			line = line.rstrip()
			if re.match('^\\s*@import\\s+', line):
				path = re.sub('^\\s*@import\\s+|\\s*#.*$', '', line)
				for line in expand(path, strip_atlines, strip_comments):
					yield line
			elif strip_atlines and re.match('^\\s*@', line):
				pass
			elif strip_comments and re.match('^\\s*#', line):
				pass
			else:
				if strip_comments:
					line = re.sub('\\s*#.*$', '', line)
				yield line

def main():
	strip_atlines = False
	strip_comments = False
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
			os.chdir(sys.argv[i])
			i += 1
		else:
			for line in expand(arg, strip_atlines, strip_comments):
				print(line)

if __name__ == '__main__':
	main()
