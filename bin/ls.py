#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import charset_path, ls

def main():
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg[0] == '@':
				for f in ls(charset_path(arg[1:])):
					print(f)
			else:
				for f in ls(arg):
					print(f)
	else:
		for f in ls('.'):
			print(f)

if __name__ == '__main__':
	main()
