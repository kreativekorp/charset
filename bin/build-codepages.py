#!/usr/bin/env python

from __future__ import print_function

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from acquisitionlib import acquire, simple_html_parser
from parselib import charset_path

class __datatable_parser(simple_html_parser):
	def simple_init(self, *args, **kwargs):
		self.rows = []
		self.in_table = False
		self.in_column = -1
		self.row = []

	def simple_starttag(self, tag, attrs):
		if tag == 'table':
			self.in_table = True
			self.in_column = -1
			self.row = []
		elif self.in_table:
			if tag == 'tr':
				self.in_column = -1
				self.row = []
			elif tag == 'th' or tag == 'td':
				self.in_column += 1

	def simple_data(self, data):
		if self.in_table and self.in_column >= 0:
			while self.in_column >= len(self.row):
				self.row.append('')
			self.row[self.in_column] += data

	def simple_endtag(self, tag):
		if tag == 'table':
			self.in_table = False
			self.in_column = -1
			self.row = []
		elif self.in_table:
			if tag == 'tr':
				for i in range(0, len(self.row)):
					self.row[i] = self.row[i].strip()
				self.rows.append(self.row)
				self.in_column = -1
				self.row = []

def main():
	parser = __datatable_parser()
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
	parser = __datatable_parser()
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
	parser = __datatable_parser()
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
	parser = __datatable_parser()
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
