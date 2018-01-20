#!/usr/bin/env python

import io
import os
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
		if tag == 'table' and 'id' in attrs and attrs['id'] == 'VendorList':
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
				self.vendor['detail_url'] = 'https://www.microsoft.com' + attrs['href']

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
				for k, v in self.vendor.items():
					self.vendor[k] = v.strip()
				self.vendors.append(self.vendor)
				self.in_column = 0
				self.vendor = {}

class __vendor_id_detail_parser(simple_html_parser):
	def simple_init(self, *args, **kwargs):
		self.vendor = kwargs['vendor']
		self.in_section = None
		self.in_para = 0
		self.in_link = False

	def simple_starttag(self, tag, attrs):
		if tag == 'span' and 'id' in attrs and attrs['id'] == 'VendorName':
			self.in_section = 'name'
			self.in_para = 0
			self.in_link = False
		elif tag == 'div' and 'id' in attrs and attrs['id'] == 'Detail':
			self.in_section = 'detail'
			self.in_para = 0
			self.in_link = False
		elif self.in_section is not None:
			if tag == 'p':
				self.in_para += 1
			elif tag == 'a' and 'href' in attrs:
				self.in_link = True
				self.vendor['url'] = attrs['href']

	def simple_data(self, data):
		if self.in_section == 'name':
			if 'detail_name' in self.vendor:
				self.vendor['detail_name'] += data
			else:
				self.vendor['detail_name'] = data
		elif self.in_section == 'detail':
			if self.in_para == 1:
				if not self.in_link:
					if 'contact_info' in self.vendor:
						self.vendor['contact_info'] += data
					else:
						self.vendor['contact_info'] = data
			elif self.in_para == 2:
				if 'description' in self.vendor:
					self.vendor['description'] += data
				else:
					self.vendor['description'] = data

	def simple_endtag(self, tag):
		if tag == 'span' or tag == 'div':
			self.in_section = None
			self.in_para = 0
			self.in_link = False
		elif tag == 'a':
			self.in_link = False

	def simple_close(self):
		for k, v in self.vendor.items():
			self.vendor[k] = v.strip()

def list_vendors():
	vip = __vendor_id_index_parser()
	with io.open(acquire('https://www.microsoft.com/typography/links/vendorlist.aspx', 'local'), mode='r', encoding='iso8859-1') as f:
		for line in f:
			vip.feed(line)
	vip.close()
	for vendor in vip.vendors:
		if 'detail_url' in vendor:
			vdp = __vendor_id_detail_parser(vendor=vendor)
			with io.open(acquire(vendor['detail_url'], 'local'), mode='r', encoding='iso8859-1') as f:
				for line in f:
					vdp.feed(line)
			vdp.close()
			yield vdp.vendor
		else:
			yield vendor
