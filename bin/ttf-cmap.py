#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttf_file

def main():
	include_style = True
	for arg in sys.argv[1:]:
		print(arg)
		with ttf_file(arg) as ttf:
			for cmap in ttf.cmaps():
				print('\t%s\t%s\t%s\t%s' % (cmap.platform_id, cmap.platform_specific_id, cmap.language, cmap.format))
				for cp, glyph in cmap.glyphs():
					print('\t\t%s -> %s' % (cp, glyph))

if __name__ == '__main__':
	main()
