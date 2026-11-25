#!/usr/bin/env python3

import bitset
import io
import os
import re
import struct
import sys

def unquote(s):
	if len(s) >= 2:
		if s[0] == '"' and s[-1] == '"':
			return s[1:-1]
		if s[0] == "'" and s[-1] == "'":
			return s[1:-1]
	return s

class FontBase:
	def __init__(self):
		self.name = None
		self.chars = bitset.BitSet()
		self.vendorid = None
		self.puadata = None

class BdfFile(FontBase):
	def __init__(self, file):
		FontBase.__init__(self)
		with open(file, 'r', encoding='iso-8859-1') as f:
			for line in f:
				if line[:12] == 'FAMILY_NAME ':
					self.name = unquote(line[12:].strip())
				if line[:11] == 'OS2_VENDOR ':
					self.vendorid = unquote(line[11:].strip())
				if line[:9] == 'ENCODING ':
					try:
						self.chars.set(int(line[9:].strip()))
					except ValueError:
						pass

class TtfTable:
	def __init__(self, tag, checksum, offset, length):
		self.tag = tag
		self.checksum = checksum
		self.offset = offset
		self.length = length

	def set_data(self, data):
		self.data = data

class TtfName:
	def __init__(self, pid, psid, lang, id, length, offset):
		self.platform_id = pid
		self.platform_specific_id = psid
		self.language_id = lang
		self.name_id = id
		self.length = length
		self.offset = offset
		if pid == 0 or pid == 2 or pid == 10:
			self.encoding = 'utf-16be'
			self.is_english = True
		elif pid == 3 and (psid == 1 or psid == 10):
			self.encoding = 'utf-16be'
			self.is_english = (lang == 1033)
		elif pid == 1 and psid == 0:
			self.encoding = 'macroman'
			self.is_english = (lang == 0)
		else:
			self.encoding = None
			self.is_english = False

	def set_data(self, data):
		self.data = data
		self.name = None
		if self.encoding is not None:
			try:
				self.name = data.decode(self.encoding)
			except UnicodeDecodeError:
				pass

class TtfCmap:
	def __init__(self, pid, psid, offset):
		self.platform_id = pid
		self.platform_specific_id = psid
		self.offset = offset
		if pid == 0 or pid == 2 or pid == 10:
			self.is_mac_roman = False
			self.is_unicode = True
		elif pid == 3 and (psid == 1 or psid == 10):
			self.is_mac_roman = False
			self.is_unicode = True
		elif pid == 1 and psid == 0:
			self.is_mac_roman = True
			self.is_unicode = False
		else:
			self.is_mac_roman = False
			self.is_unicode = False

	def set_data(self, format, length, language, data):
		self.format = format
		self.length = length
		self.language = language
		self.data = data
		if format == 0:
			self.entries = {}
			for i in range(0, len(data)):
				cp = ord(bytes([i]).decode('macroman'))
				self.entries[cp] = data[i] & 0xFF
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
		elif format == 12 or format == 13:
			self.entries = []
			for i in range(struct.unpack('>I', data[0:4])[0]):
				dp = i * 12 + 4
				self.entries.append(struct.unpack('>III', data[dp:dp+12]))
			self.min = min(e[0] for e in self.entries)
			self.max = max(e[1] for e in self.entries)

	def glyph(self, cp):
		if self.format == 0:
			if cp in self.entries:
				return self.entries[cp]
		elif self.format == 4:
			if self.min <= cp <= self.max:
				for start, stop, delta, offset, dp in self.entries:
					if start <= cp <= stop:
						if offset == 0:
							return (cp + delta) & 0xFFFF
						ip = dp + offset + ((cp - start) << 1)
						if ip < len(self.data):
							glyph = struct.unpack('>H', self.data[ip:ip+2])[0]
							if glyph > 0:
								return (glyph + delta) & 0xFFFF
		elif self.format == 6:
			i = cp - self.first
			if 0 <= i < self.count:
				dp = (i << 1) + 4
				return struct.unpack('>H', self.data[dp:dp+2])[0]
		elif self.format == 10:
			i = cp - self.first
			if 0 <= i < self.count:
				dp = (i << 1) + 8
				return struct.unpack('>H', self.data[dp:dp+2])[0]
		elif self.format == 12:
			if self.min <= cp <= self.max:
				for start, stop, glyph in self.entries:
					if start <= cp <= stop:
						return (glyph + (cp - start)) & 0xFFFF
		elif self.format == 13:
			if self.min <= cp <= self.max:
				for start, stop, glyph in self.entries:
					if start <= cp <= stop:
						return glyph
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
								yield cp, glyph
		elif self.format == 6:
			for i in range(self.count):
				dp = (i << 1) + 4
				glyph = struct.unpack('>H', self.data[dp:dp+2])[0]
				if glyph > 0:
					yield self.first + i, glyph
		elif self.format == 10:
			for i in range(self.count):
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
		elif self.format == 13:
			for start, stop, glyph in self.entries:
				for cp in range(start, stop + 1):
					if glyph > 0:
						yield cp, glyph

# TODO PUAA table

class TtfBase(FontBase):
	def __init__(self, fp, header_offset, table_offset):
		FontBase.__init__(self)
		fp.seek(header_offset)
		self.scaler, self.num_tables, self.search_range, self.entry_selector, self.range_shift = struct.unpack('>ihhhh', fp.read(12))
		self.tables = [TtfTable(*struct.unpack('>4siii', fp.read(16))) for i in range(self.num_tables)]
		for table in self.tables:
			fp.seek(table_offset + table.offset)
			table.set_data(fp.read(table.length))
		self.name = self.get_name(1)
		self.chars = self.get_chars()
		self.vendorid = self.get_vendorid()
		# TODO puadata

	def get_table(self, tag):
		for table in self.tables:
			if table.tag == tag:
				return table
		return None

	def list_names(self):
		table = self.get_table(b'name')
		if table is not None:
			with io.BytesIO(table.data) as fp:
				format, num_records, string_offset = struct.unpack('>HHH', fp.read(6))
				names = [TtfName(*struct.unpack('>HHHHHH', fp.read(12))) for i in range(num_records)]
				for name in names:
					fp.seek(string_offset + name.offset)
					name.set_data(fp.read(name.length))
				return names
		return None

	def get_name(self, name_id):
		names = self.list_names()
		if names is not None:
			for name in names:
				if name.name_id == name_id:
					if name.is_english:
						return name.name
		return None

	def list_cmaps(self):
		table = self.get_table(b'cmap')
		if table is not None:
			with io.BytesIO(table.data) as fp:
				format, num_records = struct.unpack('>HH', fp.read(4))
				cmaps = [TtfCmap(*struct.unpack('>HHI', fp.read(8))) for i in range(num_records)]
				for cmap in cmaps:
					fp.seek(cmap.offset)
					format = struct.unpack('>H', fp.read(2))[0]
					if format < 8:
						length, language = struct.unpack('>HH', fp.read(4))
						cmap.set_data(format, length, language, fp.read(length - 6))
					elif format < 14:
						reserved, length, language = struct.unpack('>HII', fp.read(10))
						cmap.set_data(format, length, language, fp.read(length - 12))
					elif format == 14:
						length = struct.unpack('>I', fp.read(4))[0]
						cmap.set_data(format, length, 0, fp.read(length - 6))
					else:
						cmap.set_data(format, 0, 0, None)
				return cmaps
		return None

	def get_chars(self):
		chars = bitset.BitSet()
		cmaps = self.list_cmaps()
		if cmaps is not None:
			for cmap in cmaps:
				if cmap.is_mac_roman or cmap.is_unicode:
					for cp, glyph in cmap.glyphs():
						chars.set(cp)
		return chars

	def get_vendorid(self):
		table = self.get_table(b'OS/2')
		if table is not None:
			return table.data[0x3A:0x3E].decode('us-ascii')
		return None

class TtfFile(TtfBase):
	def __init__(self, file):
		with open(file, 'rb') as fp:
			TtfBase.__init__(self, fp, 0, 0)

class TtcFont(TtfBase):
	def __init__(self, fp, offset):
		TtfBase.__init__(self, fp, offset, 0)

class TtcFile:
	def __init__(self, file):
		with open(file, 'rb') as fp:
			self.magic, self.version, self.num_fonts = struct.unpack('>iii', fp.read(12))
			self.offsets = [struct.unpack('>i', fp.read(4))[0] for i in range(self.num_fonts)]
			self.fonts = [TtcFont(fp, offset) for offset in self.offsets]

class DfontFont(TtfBase):
	def __init__(self, data):
		with io.BytesIO(data) as fp:
			TtfBase.__init__(self, fp, 0, 0)

class DfontResource:
	def __init__(self, id, name_offset, data_offset, ptr):
		self.id = id
		self.name_offset = name_offset
		self.attributes = (data_offset >> 24) & 0xFF
		self.data_offset = data_offset & 0xFFFFFF

class DfontResourceType:
	def __init__(self, type, count, offset):
		self.type = type
		self.count = (count + 1) & 0xFFFF
		self.offset = offset

class DfontFile:
	def __init__(self, file):
		with open(file, 'rb') as fp:
			self.data_offset, self.map_offset, self.data_length, self.map_length = struct.unpack('>iiii', fp.read(16))
			fp.seek(self.map_offset)
			self.data_offset_2, self.map_offset_2, self.data_length_2, self.map_length_2 = struct.unpack('>iiii', fp.read(16))
			self.next_resource_map, self.file_ref, self.attributes, self.typelist_offset, self.namelist_offset = struct.unpack('>ihhhh', fp.read(12))
			fp.seek(self.map_offset + self.typelist_offset)
			self.type_count = (struct.unpack('>h', fp.read(2))[0] + 1) & 0xFFFF
			self.types = [DfontResourceType(*struct.unpack('>4shh', fp.read(8))) for i in range(self.type_count)]
			for type in self.types:
				fp.seek(self.map_offset + self.typelist_offset + type.offset)
				type.resources = [DfontResource(*struct.unpack('>hhii', fp.read(12))) for i in range(type.count)]
				for resource in type.resources:
					if resource.name_offset < 0:
						resource.name = None
					else:
						fp.seek(self.map_offset + self.namelist_offset + resource.name_offset)
						resource.name_length = fp.read(1)[0] & 0xFF
						resource.name = fp.read(resource.name_length).decode('macroman')
					fp.seek(self.data_offset + resource.data_offset)
					resource.data_length = struct.unpack('>i', fp.read(4))[0]
					resource.data = fp.read(resource.data_length)

	def fonts(self):
		for type in self.types:
			if type.type == b'sfnt':
				for resource in type.resources:
					yield DfontFont(resource.data)

def load(file, verbosity=0, ignore_errors=False, ignore_unknown=False):
	if verbosity > 0:
		print(file)
	if os.path.isdir(file):
		for child in os.listdir(file):
			if child.startswith('.') or child.endswith('\r'):
				continue
			for font in load(os.path.join(file, child), verbosity, ignore_errors, True):
				yield font
	else:
		ext = os.path.splitext(file)[1].lower()
		if ext == '.lst':
			lines = []
			try:
				with open(file, 'r') as f:
					lines = [line.rstrip('\r\n') for line in f]
			except Exception as e:
				if ignore_errors and verbosity >= 0:
					print('Error: %s: %s' % (e, file))
				if not ignore_errors:
					raise e
			for line in lines:
				if line:
					for font in load(line, verbosity, ignore_errors, False):
						yield font
		elif ext == '.bdf' or ext == '.bdfmeta':
			try:
				yield BdfFile(file)
			except Exception as e:
				if ignore_errors and verbosity >= 0:
					print('Error: %s: %s' % (e, file))
				if not ignore_errors:
					raise e
		elif ext == '.ttf' or ext == '.ttfmeta' or ext == '.otf' or ext == '.otfmeta':
			try:
				yield TtfFile(file)
			except Exception as e:
				if ignore_errors and verbosity >= 0:
					print('Error: %s: %s' % (e, file))
				if not ignore_errors:
					raise e
		elif ext == '.ttc' or ext == '.ttcmeta':
			try:
				for font in TtcFile(file).fonts:
					yield font
			except Exception as e:
				if ignore_errors and verbosity >= 0:
					print('Error: %s: %s' % (e, file))
				if not ignore_errors:
					raise e
		elif ext == '.dfont' or ext == '.dfontmeta':
			try:
				for font in DfontFile(file).fonts():
					yield font
			except Exception as e:
				if ignore_errors and verbosity >= 0:
					print('Error: %s: %s' % (e, file))
				if not ignore_errors:
					raise e
		elif not ignore_unknown:
			if ignore_errors and verbosity >= 0:
				print('Error: unknown format: %s' % file)
			if not ignore_errors:
				raise ValueError('unknown format')

def ignore_font(font):
	if not font.name:
		return True
	if font.name.startswith('.'):
		return True
	if re.match('^[.]?Last[ ]?Resort$', font.name):
		return True
	if re.match('^YOz[A-Z][A-Za-z0-9]+$', font.name):
		return True
	words = font.name.split(' ')
	if words[0] == 'Noto' and words[-1] in [
		'Bk', 'Black', 'Blk', 'Bold', 'Cn', 'Cond', 'Condensed', 'DemiLight',
		'ExBd', 'ExCd', 'ExLt', 'ExtBd', 'ExtCond', 'ExtLight', 'ExtLt',
		'ExtraBold', 'ExtraCond', 'ExtraCondensed', 'ExtraLight', 'Italic',
		'Light', 'Lt', 'Md', 'Med', 'Medium', 'SemBd', 'SemCond',
		'Semi', 'SemiBold', 'SemiCond', 'SemiCondensed', 'Semibold',
		'SmBd', 'SmCd', 'SmCn', 'Th', 'Thin', 'XBd', 'XCn', 'XLt'
	]:
		return True
	return False

def main():
	parse_opts = True
	verbosity = 0
	ignore_errors = False
	ignore_unknown = False
	ignore_ignored = False
	args = sys.argv[1:]
	for arg in args:
		if parse_opts and arg.startswith('-'):
			if arg == '--':
				parse_opts = False
			elif arg == '-q':
				verbosity = -1
			elif arg == '-v':
				verbosity = 1
			elif arg == '-f':
				ignore_errors = True
			elif arg == '-s':
				ignore_unknown = True
			elif arg == '-i':
				ignore_ignored = True
			else:
				print('Error: Unknown option: %s' % arg)
		else:
			for font in load(arg, verbosity, ignore_errors, ignore_unknown):
				if ignore_ignored and ignore_font(font):
					if verbosity >= 0:
						print('Skipped: %s' % font.name)
					continue
				print('%s\t%d\t%s' % (font.name, font.chars.popcount(), font.vendorid))

if __name__ == '__main__':
	main()
