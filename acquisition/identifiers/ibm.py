#!/usr/bin/env python

from __future__ import print_function

import io
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, charset_path, html_table_parser

def list_files():
	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/cs/cs_gcsgid.html', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()

	path = charset_path('identifiers', 'ibm-gcsgid.txt')
	with io.open(path, mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if row[0] != 'GCSGID':
				id = int(row[0])
				name = row[1]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	yield ('ibm-gcsgid.txt', path)

	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/cp/cp_cpgid.html', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()

	path = charset_path('identifiers', 'ibm-cpgid.txt')
	with io.open(path, mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if row[0] != 'CPGID':
				id = int(row[0])
				name = row[1]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	yield ('ibm-cpgid.txt', path)

	parser = html_table_parser()
	with io.open(acquire('https://www-01.ibm.com/software/globalization/ccsid/ccsid_registered.html', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			parser.feed(line)
	parser.close()

	path = charset_path('identifiers', 'ibm-ccsid.txt')
	with io.open(path, mode='w', encoding='utf-8') as f:
		for row in parser.rows:
			if not row[0].startswith('CCSID'):
				id = int(row[0])
				name = row[2]
				print(u'%05d\t%04X\t%s' % (id, id, name), file=f)
	yield ('ibm-ccsid.txt', path)

	path = charset_path('identifiers', 'codepages-ibm.txt')
	with io.open(path, mode='w', encoding='utf-8') as f:
		print(u'@codepage', file=f)
		for row in parser.rows:
			if not row[0].startswith('CCSID'):
				id = int(row[0])
				name = row[2]
				if (id < 100):
					print(u'%03d\t# %s' % (id, name), file=f)
				else:
					print(u'%d\t# %s' % (id, name), file=f)
	yield ('codepages-ibm.txt', path)
