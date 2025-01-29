#!/usr/bin/env python

try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser

try:
	from htmlentitydefs import name2codepoint
except ImportError:
	from html.entities import name2codepoint

import os
import re
import subprocess

def charset_path(*paths):
	return os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', *paths))

def cache_path(url=None):
	path = charset_path('.charset-cache')
	if not os.path.exists(path):
		os.mkdir(path)
	if url is not None:
		url = re.sub('[ !\"\'+,/:;\\^`|~]', '-', url)
		url = re.sub('[^A-Za-z0-9_.-]', '$', url)
		path = os.path.join(path, url)
	return path

def acquire(url, version='auto', ua='Mozilla/5.0', compressed=False):
	path = cache_path(url)
	path_exists = os.path.exists(path)
	if version == 'local' and path_exists:
		return path
	else:
		args = ['curl', '-L', '-s', url, '-o', path]
		if version != 'remote' and path_exists:
			args.append('-z')
			args.append(path)
		if ua:
			args.append('-A')
			args.append(ua)
		if compressed:
			args.append('--compressed')
		subprocess.check_call(args)
		return path

class simple_html_parser(HTMLParser):
	def simple_init(self, *args, **kwargs):
		pass

	def simple_starttag(self, tag, attrs):
		pass

	def simple_data(self, data):
		pass

	def simple_endtag(self, tag):
		pass

	def simple_close(self):
		pass

	def __init__(self, *args, **kwargs):
		HTMLParser.__init__(self)
		self.simple_init(*args, **kwargs)

	def feed(self, s):
		s = re.sub(u'\u2022', u'\u2022bull;', s)
		s = re.sub(u'&(#?[A-Za-z0-9_:.-]+);', u'\u2022\\1;', s)
		s = re.sub(u'&', u'\u2022amp;', s)
		s = re.sub(u'\u2022', u'&', s)
		HTMLParser.feed(self, s)

	def handle_starttag(self, tag, attrs):
		tag = tag.lower()
		attrs = dict((k.lower(), v) for k, v in attrs)
		self.simple_starttag(tag, attrs)

	def handle_data(self, data):
		self.simple_data(data)

	def handle_entityref(self, name):
		try:
			data = unichr(name2codepoint[name])
		except:
			data = '&%s;' % name
		self.simple_data(data)

	def handle_charref(self, name):
		try:
			if name.startswith('x'):
				data = unichr(int(name[1:], 16))
			else:
				data = unichr(int(name))
		except:
			data = '&%s;' % name
		self.simple_data(data)

	def handle_endtag(self, tag):
		tag = tag.lower()
		self.simple_endtag(tag)

	def close(self):
		HTMLParser.close(self)
		self.simple_close()

class html_table_parser(simple_html_parser):
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

class html_link_collector(simple_html_parser):
	def simple_init(self, *args, **kwargs):
		self.links = []

	def simple_starttag(self, tag, attrs):
		if tag == 'a' and 'href' in attrs:
			self.links.append(attrs['href'])
