#!/usr/bin/env python

from __future__ import print_function

import os
import struct
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttf_file

def write_meta(ttfpath, metapath):
	with ttf_file(ttfpath) as ttf:
		tables = [t for t in ttf.tables if t.tag in ['head', 'hhea', 'name', 'cmap', 'OS/2']]
		new_offset = 12 + 16 * len(tables)
		for table in tables:
			table.new_offset = new_offset
			new_offset += table.length + 3
			new_offset &= ~3
		with open(metapath, 'wb') as meta:
			meta.write(struct.pack('>ihhhh', 0x778E7A00, len(tables), 0, 0, 0))
			for table in tables:
				meta.write(struct.pack('>4siii', table.tag, 0, table.new_offset, table.length))
			for table in tables:
				ttf.fp.seek(table.offset)
				data = ttf.fp.read(table.length)
				meta.write(data)
				padding = table.length & 3
				if padding:
					for i in range(padding, 4):
						meta.write('\0')

def main():
	for arg in sys.argv[1:]:
		write_meta(arg, arg + 'meta')
		print('%s -> %s' % (arg, arg + 'meta'))

if __name__ == '__main__':
	main()
