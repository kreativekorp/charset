#!/usr/bin/env python

from __future__ import print_function

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, charset_path, html_table_parser

def list_files():
	parser = html_table_parser()
	with io.open(acquire('https://msdn.microsoft.com/en-us/library/windows/desktop/dd317756.aspx', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()

	path = charset_path('identifiers', 'codepages-microsoft.txt')
	with io.open(path, mode='w', encoding='utf-8') as f:
		print(u'@codepage\t@charset', file=f)
		for row in parser.rows:
			if re.match('[0-9]+', row[0]):
				id = int(row[0])
				cs = row[1] if row[1] else '--'
				name = row[2]
				if (id < 100):
					print(u'%03d\t%s\t# %s' % (id, cs, name), file=f)
				else:
					print(u'%d\t%s\t# %s' % (id, cs, name), file=f)
	yield ('codepages-microsoft.txt', path)
