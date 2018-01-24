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

class __ttf_base:
	def locate(self, tag):
		for table in self.tables:
			if table.tag == tag:
				self.fp.seek(table.offset)
				return table
		return None

	def names(self):
		table = self.locate('name')
		if table is not None:
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

class ttf_file(__ttf_base):
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.fp = open(self.path, 'rb')
		self.scaler, self.num_tables, self.search_range, self.entry_selector, self.range_shift = struct.unpack('>ihhhh', self.fp.read(12))
		self.tables = [ttf_table(*struct.unpack('>4siii', self.fp.read(16))) for i in range(0, self.num_tables)]
		return self

	def __exit__(self, etype, value, traceback):
		self.fp.close()

class ttc_font(__ttf_base):
	def __init__(self, path, fp, offset):
		fp.seek(offset)
		self.path, self.fp, self.offset = path, fp, offset
		self.scaler, self.num_tables, self.search_range, self.entry_selector, self.range_shift = struct.unpack('>ihhhh', self.fp.read(12))
		self.tables = [ttf_table(*struct.unpack('>4siii', self.fp.read(16))) for i in range(0, self.num_tables)]

class ttc_file:
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.fp = open(self.path, 'rb')
		self.magic, self.version, self.num_fonts = struct.unpack('>iii', self.fp.read(12))
		self.offsets = [struct.unpack('>i', self.fp.read(4))[0] for i in range(0, self.num_fonts)]
		self.fonts = [ttc_font(self.path, self.fp, offset) for offset in self.offsets]
		return self

	def __exit__(self, etype, value, traceback):
		self.fp.close()

class dfont_resource_type:
	def __init__(self, type, count, offset):
		self.type = type
		self.count = (count + 1) & 0xFFFF
		self.offset = offset

class dfont_resource:
	def __init__(self, id, name_offset, data_offset, ptr):
		self.id = id
		self.attributes = (data_offset >> 24)
		self.name_offset = name_offset
		self.data_offset = (data_offset & 0xFFFFFF)

class dfont_file:
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.fp = open(self.path, 'rb')
		self.data_offset, self.map_offset, self.data_length, self.map_length = struct.unpack('>iiii', self.fp.read(16))
		self.fp.seek(self.map_offset)
		self.data_offset_2, self.map_offset_2, self.data_length_2, self.map_length_2 = struct.unpack('>iiii', self.fp.read(16))
		self.next_resource_map, self.file_ref, self.attributes, self.typelist_offset, self.namelist_offset = struct.unpack('>ihhhh', self.fp.read(12))
		self.fp.seek(self.map_offset + self.typelist_offset)
		self.type_count = (struct.unpack('>h', self.fp.read(2))[0] + 1) & 0xFFFF
		self.types = [dfont_resource_type(*struct.unpack('>4shh', self.fp.read(8))) for i in range(0, self.type_count)]
		for type in self.types:
			self.fp.seek(self.map_offset + self.typelist_offset + type.offset)
			type.resources = [dfont_resource(*struct.unpack('>hhii', self.fp.read(12))) for i in range(0, type.count)]
			for resource in type.resources:
				if resource.name_offset < 0:
					resource.name = None
				else:
					self.fp.seek(self.map_offset + self.namelist_offset + resource.name_offset)
					name_length = struct.unpack('>B', self.fp.read(1))[0]
					resource.name = self.fp.read(name_length).decode('macroman').encode('utf-8')
				self.fp.seek(self.data_offset + resource.data_offset)
				resource.length = struct.unpack('>i', self.fp.read(4))[0]
				resource.offset = self.data_offset + resource.data_offset + 4
		return self

	def __exit__(self, etype, value, traceback):
		self.fp.close()
