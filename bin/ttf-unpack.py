#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttf_file

def unpack_ttf(ttfpath):
	with ttf_file(ttfpath) as ttf:
		for table in ttf.tables:
			name = re.sub('[^A-Za-z0-9]', '_', table.tag)
			with open('%s.%s.bin' % (ttfpath, name), 'wb') as tf:
				ttf.fp.seek(table.offset)
				tf.write(ttf.fp.read(table.length))

def main():
	for arg in sys.argv[1:]:
		unpack_ttf(arg)
		print(arg)

if __name__ == '__main__':
	main()
