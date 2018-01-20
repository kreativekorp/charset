#!/usr/bin/env python

import struct

class ttf_table:
	def __init__(self, tag, checksum, offset, length):
		self.tag = tag
		self.checksum = checksum
		self.offset = offset
		self.length = length

class ttf_name:
	def __init__(self, pid, psid, lang, id, length, offset):
		self.platform_id = pid
		self.platform_specific_id = psid
		self.language_id = lang
		self.name_id = id
		self.length = length
		self.offset = offset

	def set_data(self, data):
		self.data = data
		if self.platform_id == 0:
			self.name = data.decode('utf-16be').encode('utf-8')
		elif self.platform_id == 3 and self.platform_specific_id == 1:
			self.name = data.decode('utf-16be').encode('utf-8')
		elif self.platform_id == 1 and self.platform_specific_id == 0:
			self.name = data.decode('macroman').encode('utf-8')

class ttf_file:
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.fp = open(self.path, 'rb')
		self.scaler, self.num_tables, self.search_range, self.entry_selector, self.range_shift = struct.unpack('>ihhhh', self.fp.read(12))
		self.tables = [ttf_table(*struct.unpack('>4siii', self.fp.read(16))) for i in range(0, self.num_tables)]
		return self

	def __exit__(self, etype, value, traceback):
		self.fp.close()

	def locate(self, tag):
		for table in self.tables:
			if table.tag == tag:
				self.fp.seek(table.offset)
				return table
		return None

	def names(self):
		table = self.locate('name')
		if table:
			format, num_records, string_offset = struct.unpack('>hhh', self.fp.read(6))
			names = [ttf_name(*struct.unpack('>hhhhhh', self.fp.read(12))) for i in range(0, num_records)]
			for name in names:
				self.fp.seek(table.offset + string_offset + name.offset)
				name.set_data(self.fp.read(name.length))
			return names
		return None

	def name(self, include_style=True):
		names = self.names()
		if names is None: return None
		family_names = []
		style_names = []
		for name in names:
			if (
				(name.platform_id == 0) or
				(name.platform_id == 3 and name.platform_specific_id == 1 and name.language_id == 1033) or
				(name.platform_id == 1 and name.platform_specific_id == 0 and name.language_id == 0)
			):
				if name.name_id == 1:
					if name.name not in family_names:
						family_names.append(name.name)
				elif name.name_id == 2:
					if name.name not in style_names:
						style_names.append(name.name)
		name = ', '.join(family_names)
		if include_style:
			name += ' '
			name += ', '.join(style_names)
		return name
