#!/usr/bin/env python

from __future__ import print_function

import sys

def write_meta(bdfpath, metapath):
	in_bitmap = False
	with open(bdfpath, 'r') as bdf:
		with open(metapath, 'w') as meta:
			for line in bdf:
				if line.strip() == 'BITMAP':
					in_bitmap = True
				if line.strip() == 'ENDCHAR':
					in_bitmap = False
				if not in_bitmap:
					meta.write(line)

def main():
	for arg in sys.argv[1:]:
		write_meta(arg, arg + 'meta')
		print('%s -> %s' % (arg, arg + 'meta'))

if __name__ == '__main__':
	main()
