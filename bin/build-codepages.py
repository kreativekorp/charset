#!/usr/bin/env python

from __future__ import print_function

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from acquisitionlib import acquire, charset_path, html_table_parser

def main():
	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/cs/cs_gcsgid.html'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()
	with io.open(charset_path('identifiers', 'ibm-gcsgid.txt'), mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if row[0] != 'GCSGID':
				id = int(row[0])
				name = row[1]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/cp/cp_cpgid.html'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()
	with io.open(charset_path('identifiers', 'ibm-cpgid.txt'), mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if row[0] != 'CPGID':
				id = int(row[0])
				name = row[1]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/ccsid/ccsid_registered.html'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()
	with io.open(charset_path('identifiers', 'ibm-ccsid.txt'), mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if not row[0].startswith('CCSID'):
				id = int(row[0])
				name = row[2]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	with io.open(charset_path('identifiers', 'codepages-ibm.txt'), mode='w', encoding='utf-8') as f:
		print(u'@codepage', file=f)
		for row in parser.rows:
			if not row[0].startswith('CCSID'):
				id = int(row[0])
				name = row[2]
				if (id < 100):
					print(u'%03d\t# %s' % (id, name), file=f)
				else:
					print(u'%d\t# %s' % (id, name), file=f)
	parser = html_table_parser()
	with io.open(acquire('https://msdn.microsoft.com/en-us/library/windows/desktop/dd317756.aspx'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()
	with io.open(charset_path('identifiers', 'codepages-microsoft.txt'), mode='w', encoding='utf-8') as f:
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

if __name__ == '__main__':
	main()
