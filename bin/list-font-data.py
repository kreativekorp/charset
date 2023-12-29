#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from datalib import get_font_data

def main():
	for name, chars, vendorid, puadata, url in get_font_data():
		print('%s\t%s\t%s\t%s\t%s' % (name, vendorid, chars.popcount(), puadata is not None, url))

if __name__ == '__main__':
	main()
