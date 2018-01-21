#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import dfont_file

def unpack_dfont(dfontpath):
	with dfont_file(dfontpath) as dfont:
		for type in dfont.types:
			if type.type == 'sfnt':
				for i in range(0, type.count):
					res = type.resources[i]
					with open('%s.%d.ttf' % (dfontpath, i), 'wb') as ttf:
						dfont.fp.seek(res.offset)
						data = dfont.fp.read(res.length)
						ttf.write(data)

def main():
	for arg in sys.argv[1:]:
		unpack_dfont(arg)
		print(arg)

if __name__ == '__main__':
	main()
