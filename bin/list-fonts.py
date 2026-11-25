#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import charset_path, load_plugin, ls

def main():
	fonts = []
	path = charset_path('acquisition', 'fonts')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for name, path, url in mod.list_fonts():
				print('%s (%s) -> %s' % (name, url, path))
				fonts.append(path)
	with open(charset_path('.charset-cache', 'fonts.lst'), 'w') as f:
		f.write('\n'.join(fonts))

if __name__ == '__main__':
	main()
