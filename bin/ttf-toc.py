#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttf_file

def main():
	for arg in sys.argv[1:]:
		with ttf_file(arg) as ttf:
			print('Table\tOffset\tLength')
			for table in ttf.tables:
				print('%s\t%d\t%d' % (table.tag, table.offset, table.length))

if __name__ == '__main__':
	main()
