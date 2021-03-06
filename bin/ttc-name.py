#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttc_file

def main():
	include_style = True
	for arg in sys.argv[1:]:
		if arg == '-s':
			include_style = False
		elif arg == '+s':
			include_style = True
		else:
			with ttc_file(arg) as ttc:
				for font in ttc.fonts:
					print(font.name(include_style))

if __name__ == '__main__':
	main()
