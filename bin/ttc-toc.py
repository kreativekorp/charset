#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttc_file

def main():
	for arg in sys.argv[1:]:
		with ttc_file(arg) as ttc:
			for i in range(0, ttc.num_fonts):
				print('Font #%d' % i)
				print('\tTable\tOffset\tLength')
				for table in ttc.fonts[i].tables:
					print('\t%s\t%d\t%d' % (table.tag, table.offset, table.length))

if __name__ == '__main__':
	main()
