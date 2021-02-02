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
		elif self.platform_id == 3 and self.platform_specific_id == 10:
			self.name = data.decode('utf-16be').encode('utf-8')
		elif self.platform_id == 3 and self.platform_specific_id == 1:
			self.name = data.decode('utf-16be').encode('utf-8')
		elif self.platform_id == 1 and self.platform_specific_id == 0:
			self.name = data.decode('macroman').encode('utf-8')

class ttf_cmap:
	def __init__(self, pid, psid, offset):
		self.platform_id = pid
		self.platform_specific_id = psid
		self.offset = offset

	def set_data(self, format, length, language, data):
		self.format = format
		self.length = length
		self.language = language
		self.data = data
		if format == 0:
			self.entries = {}
			for i in range(0, len(data)):
				cp = ord(chr(i).decode('macroman'))
				self.entries[cp] = ord(data[i])
		elif format == 4:
			self.entries = []
			countX2 = struct.unpack('>H', data[0:2])[0]
			for i in range(0, countX2, 2):
				dp = i + 8
				stop = struct.unpack('>H', data[dp:dp+2])[0]
				dp += countX2 + 2
				start = struct.unpack('>H', data[dp:dp+2])[0]
				dp += countX2
				delta = struct.unpack('>H', data[dp:dp+2])[0]
				dp += countX2
				offset = struct.unpack('>H', data[dp:dp+2])[0]
				self.entries.append((start, stop, delta, offset, dp))
			self.min = min(e[0] for e in self.entries)
			self.max = max(e[1] for e in self.entries)
		elif format == 6:
			self.first, self.count = struct.unpack('>HH', data[0:4])
		elif format == 10:
			self.first, self.count = struct.unpack('>II', data[0:8])
		elif format == 12:
			self.entries = []
			count = struct.unpack('>I', data[0:4])[0]
			for i in range(0, count):
				dp = i * 12 + 4
				start, stop, glyph = struct.unpack('>III', data[dp:dp+12])
				self.entries.append((start, stop, glyph))
			self.min = min(e[0] for e in self.entries)
			self.max = max(e[1] for e in self.entries)

	def glyph(self, cp):
		if self.format == 0:
			if cp in self.entries:
				return self.entries[cp]
		elif self.format == 4:
			if cp >= self.min and cp <= self.max:
				for start, stop, delta, offset, dp in self.entries:
					if cp >= start and cp <= stop:
						if offset == 0:
							return (cp + delta) & 0xFFFF
						else:
							ip = dp + offset + ((cp - start) << 1)
							if ip < len(self.data):
								glyph = struct.unpack('>H', self.data[ip:ip+2])[0]
								if glyph > 0:
									return (glyph + delta) & 0xFFFF
		elif self.format == 6:
			i = cp - self.first
			if i >= 0 and i < self.count:
				dp = (i << 1) + 4
				return struct.unpack('>H', self.data[dp:dp+2])[0]
		elif self.format == 10:
			i = cp - self.first
			if i >= 0 and i < self.count:
				dp = (i << 1) + 8
				return struct.unpack('>H', self.data[dp:dp+2])[0]
		elif self.format == 12:
			if cp >= self.min and cp <= self.max:
				for start, stop, glyph in self.entries:
					if cp >= start and cp <= stop:
						return (glyph + (cp - start)) & 0xFFFF
		return 0

	def glyphs(self):
		if self.format == 0:
			for cp in self.entries:
				glyph = self.entries[cp]
				if glyph > 0:
					yield cp, glyph
		elif self.format == 4:
			for start, stop, delta, offset, dp in self.entries:
				for cp in range(start, stop + 1):
					if offset == 0:
						glyph = (cp + delta) & 0xFFFF
						if glyph > 0:
							yield cp, glyph
					else:
						ip = dp + offset + ((cp - start) << 1)
						if ip < len(self.data):
							glyph = struct.unpack('>H', self.data[ip:ip+2])[0]
							if glyph > 0:
								glyph = (glyph + delta) & 0xFFFF
								if glyph > 0:
									yield cp, glyph
		elif self.format == 6:
			for i in range(0, self.count):
				dp = (i << 1) + 4
				glyph = struct.unpack('>H', self.data[dp:dp+2])[0]
				if glyph > 0:
					yield self.first + i, glyph
		elif self.format == 10:
			for i in range(0, self.count):
				dp = (i << 1) + 8
				glyph = struct.unpack('>H', self.data[dp:dp+2])[0]
				if glyph > 0:
					yield self.first + i, glyph
		elif self.format == 12:
			for start, stop, glyph in self.entries:
				for cp in range(start, stop + 1):
					gid = (glyph + (cp - start)) & 0xFFFF
					if gid > 0:
						yield cp, gid

def _puaa_read_string(fp, to, ed):
	if ed > 0:
		fp.seek(to + ed)
		length = struct.unpack('>B', fp.read(1))[0]
		return fp.read(length).decode('utf-8').encode('utf-8')
	if ed < 0:
		chars = [((ed >> x) & 0x7F) for x in [24, 16, 8, 0]]
		return ''.join(chr(x) for x in chars if x)
	return None

def _puaa_read_int_array(fp, to, ed):
	if ed > 0:
		fp.seek(to + ed)
		count = struct.unpack('>H', fp.read(2))[0]
		return [struct.unpack('>i', fp.read(4))[0] for i in range(0, count)]
	return None

class ttf_puaa:
	def __init__(self, et, plane, fcp, lcp, ed):
		self.entry_type = et
		self.first_code_point = (plane << 16) | fcp
		self.last_code_point = (plane << 16) | lcp
		self.entry_data = ed

	def set_data(self, fp, to):
		if self.entry_type == 0:
			self.value = None
		elif self.entry_type == 1:
			self.value = _puaa_read_string(fp, to, self.entry_data)
		elif self.entry_type == 2:
			ints = _puaa_read_int_array(fp, to, self.entry_data)
			self.value = [_puaa_read_string(fp, to, x) for x in ints]
		elif self.entry_type == 3:
			self.value = (self.entry_data != 0)
		elif self.entry_type == 4 or self.entry_type == 5:
			self.value = self.entry_data
		elif self.entry_type == 6 or self.entry_type == 7:
			self.value = _puaa_read_int_array(fp, to, self.entry_data)
		elif self.entry_type == 8:
			ints = _puaa_read_int_array(fp, to, self.entry_data)
			cond = _puaa_read_string(fp, to, ints[-1])
			self.value = (ints[:-1], cond)
		elif self.entry_type == 9:
			ints = _puaa_read_int_array(fp, to, self.entry_data)
			str0 = _puaa_read_string(fp, to, ints[0])
			str1 = _puaa_read_string(fp, to, ints[1])
			self.value = (str0, str1)
		else:
			self.value = None

	def contains(self, cp):
		return self.first_code_point <= cp <= self.last_code_point

	def get_property_value(self, cp):
		if self.value is None:
			return None
		elif self.entry_type == 2 or self.entry_type == 6:
			return self.value[cp - self.first_code_point]
		else:
			return self.value

	def get_property_string(self, cp):
		value = self.get_property_value(cp)
		if value is None:
			return None
		elif self.entry_type == 1 or self.entry_type == 2:
			return value
		elif self.entry_type == 3:
			return 'Y' if value else 'N'
		elif self.entry_type == 5 or self.entry_type == 6:
			return '%04X' % value
		elif self.entry_type == 7:
			return ' '.join('%04X' % x for x in value)
		elif self.entry_type == 8:
			seqs = ' '.join('%04X' % x for x in value[0])
			return '; '.join(seqs, value[1]) if value[1] else seqs
		elif self.entry_type == 9:
			return ';'.join(value)
		else:
			return str(value)

def _puaa_read_entries(fp, to, sho):
	if sho > 0:
		fp.seek(to + sho)
		count = struct.unpack('>H', fp.read(2))[0]
		entries = [ttf_puaa(*struct.unpack('>BBHHi', fp.read(10))) for i in range(0, count)]
		for entry in entries:
			entry.set_data(fp, to)
		return entries
	return None

class _ttf_base:
	def locate(self, tag):
		for table in self.tables:
			if table.tag == tag:
				self.fp.seek(table.offset)
				return table
		return None

	def names(self):
		table = self.locate('name')
		if table is not None:
			format, num_records, string_offset = struct.unpack('>HHH', self.fp.read(6))
			names = [ttf_name(*struct.unpack('>HHHHHH', self.fp.read(12))) for i in range(0, num_records)]
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
				(name.platform_id == 3 and name.platform_specific_id == 10 and name.language_id == 1033) or
				(name.platform_id == 3 and name.platform_specific_id == 1 and name.language_id == 1033) or
				(name.platform_id == 1 and name.platform_specific_id == 0 and name.language_id == 0)
			):
				if name.name_id == 1:
					if name.name not in family_names:
						family_names.append(name.name)
				elif name.name_id == 2:
					if name.name not in style_names:
						style_names.append(name.name)
		name = min(family_names, key=len)
		if include_style:
			name += ' ' + min(style_names, key=len)
		return name

	def cmaps(self):
		table = self.locate('cmap')
		if table is not None:
			format, num_records = struct.unpack('>HH', self.fp.read(4))
			cmaps = [ttf_cmap(*struct.unpack('>HHI', self.fp.read(8))) for i in range(0, num_records)]
			for cmap in cmaps:
				self.fp.seek(table.offset + cmap.offset)
				format, length = struct.unpack('>HH', self.fp.read(4))
				if format < 8:
					language = struct.unpack('>H', self.fp.read(2))[0]
					data = self.fp.read(length - 6)
				else:
					length, language = struct.unpack('>II', self.fp.read(8))
					data = self.fp.read(length - 12)
				cmap.set_data(format, length, language, data)
			return cmaps
		return None

	def vendorid(self):
		table = self.locate('OS/2')
		if table is not None:
			self.fp.read(0x3A)
			return self.fp.read(4).decode('us-ascii')
		return None

	def puaas(self):
		table = self.locate('PUAA')
		if table is not None:
			version, num_props = struct.unpack('>HH', self.fp.read(4))
			props = [struct.unpack('>ii', self.fp.read(8)) for i in range(0, num_props)]
			prop_dict = {}
			for pno, sho in props:
				prop_name = _puaa_read_string(self.fp, table.offset, pno)
				entries = _puaa_read_entries(self.fp, table.offset, sho)
				prop_dict[prop_name] = entries
			return prop_dict
		return None

	def puaa(self, prop):
		table = self.locate('PUAA')
		if table is not None:
			version, num_props = struct.unpack('>HH', self.fp.read(4))
			props = [struct.unpack('>ii', self.fp.read(8)) for i in range(0, num_props)]
			for pno, sho in props:
				prop_name = _puaa_read_string(self.fp, table.offset, pno)
				if prop_name == prop:
					return _puaa_read_entries(self.fp, table.offset, sho)
		return None

class ttf_file(_ttf_base):
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.fp = open(self.path, 'rb')
		self.scaler, self.num_tables, self.search_range, self.entry_selector, self.range_shift = struct.unpack('>ihhhh', self.fp.read(12))
		self.tables = [ttf_table(*struct.unpack('>4siii', self.fp.read(16))) for i in range(0, self.num_tables)]
		return self

	def __exit__(self, etype, value, traceback):
		self.fp.close()

class ttc_font(_ttf_base):
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
