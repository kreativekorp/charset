#!/usr/bin/env python

from __future__ import print_function

import os
import struct
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttc_file

def unpack_ttc(ttcpath):
	with ttc_file(ttcpath) as ttc:
		for i in range(0, ttc.num_fonts):
			font = ttc.fonts[i]
			new_offset = 12 + 16 * len(font.tables)
			for table in font.tables:
				table.new_offset = new_offset
				new_offset += table.length + 3
				new_offset &= ~3
			with open('%s.%d.ttf' % (ttcpath, i), 'wb') as ttf:
				ttf.write(struct.pack('>ihhhh', font.scaler, font.num_tables, font.search_range, font.entry_selector, font.range_shift))
				for table in font.tables:
					ttf.write(struct.pack('>4siii', table.tag, table.checksum, table.new_offset, table.length))
				for table in font.tables:
					ttc.fp.seek(table.offset)
					data = ttc.fp.read(table.length)
					ttf.write(data)
					padding = table.length & 3
					if padding:
						for x in range(padding, 4):
							ttf.write('\0')

def main():
	for arg in sys.argv[1:]:
		unpack_ttc(arg)
		print(arg)

if __name__ == '__main__':
	main()
