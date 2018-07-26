#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, simple_html_parser

class __vendor_id_index_parser(simple_html_parser):
	def simple_init(self, *args, **kwargs):
		self.vendors = []
		self.in_table = False
		self.in_column = 0
		self.vendor = {}

	def simple_starttag(self, tag, attrs):
		if tag == 'table':
			self.in_table = True
			self.in_column = 0
			self.vendor = {}
		elif self.in_table:
			if tag == 'tr':
				self.in_column = 0
				self.vendor = {}
			elif tag == 'td':
				self.in_column += 1
			elif tag == 'a' and 'href' in attrs:
				self.vendor['url'] = attrs['href']

	def simple_data(self, data):
		if self.in_table:
			if self.in_column == 1:
				if 'id' in self.vendor:
					self.vendor['id'] += data
				else:
					self.vendor['id'] = data
			elif self.in_column == 2:
				if 'name' in self.vendor:
					self.vendor['name'] += data
				else:
					self.vendor['name'] = data

	def simple_endtag(self, tag):
		if tag == 'table':
			self.in_table = False
			self.in_column = 0
			self.vendor = {}
		elif self.in_table:
			if tag == 'tr':
				exists = False
				for k, v in self.vendor.items():
					self.vendor[k] = re.sub('\\s+', ' ', v.strip())
					exists = True
				if exists:
					self.vendors.append(self.vendor)
				self.in_column = 0
				self.vendor = {}

def list_vendors():
	vip = __vendor_id_index_parser()
	with io.open(acquire('https://docs.microsoft.com/en-us/typography/vendors/', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			vip.feed(line)
	vip.close()
	for vendor in vip.vendors:
		yield vendor
