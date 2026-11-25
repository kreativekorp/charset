#!/usr/bin/env python3

import re
import sys
import thisrepo

BASE_URL = 'http://www.unicode.org/Public/UNIDATA/'

def list_files():
	files = []
	link_re = re.compile('<a href="([^"]+[.][Tt][Xx][Tt])">\\1</a>')
	with open(thisrepo.acquire(BASE_URL, 'local'), 'r') as f:
		for line in f:
			m = link_re.search(line)
			if m:
				files.append(m.group(1))
	return files

def read_file(file):
	with open(thisrepo.acquire(BASE_URL + file, 'local'), 'r') as f:
		return [line.rstrip('\r\n') for line in f]

class UnicodeCharacterDatabase:
	def __init__(self):
		self.character_properties = {}
		self.range_properties = {}

	def get(self, property, code_point):
		if property in self.character_properties:
			if code_point in self.character_properties[property]:
				return self.character_properties[property][code_point]
		if property in self.range_properties:
			for code_point_range in self.range_properties[property]:
				if code_point_range[0] <= code_point <= code_point_range[1]:
					value = self.range_properties[property][code_point_range]
					return value % code_point if isinstance(value, str) else value
		return None

	def set_character_property(self, property, code_point, value):
		if property not in self.character_properties:
			self.character_properties[property] = {}
		self.character_properties[property][code_point] = value

	def set_range_property(self, property, first_code_point, last_code_point, value):
		if property not in self.range_properties:
			self.range_properties[property] = {}
		self.range_properties[property][(first_code_point, last_code_point)] = value

	def read_blocks(self):
		if 'Block' not in self.range_properties:
			block_re = re.compile('([0-9A-Fa-f]+)[.][.]([0-9A-Fa-f]+);\\s+(.+)')
			for line in read_file('Blocks.txt'):
				m = block_re.search(line.partition('#')[0].strip())
				if m:
					fcp = int(m.group(1), 16)
					lcp = int(m.group(2), 16)
					self.set_range_property('Block', fcp, lcp, m.group(3))

	def read_unicodedata(self):
		if 'Name' not in self.character_properties:
			range_memo = {}
			range_re = re.compile('<(.+), (First|Last)>')
			for line in read_file('UnicodeData.txt'):
				data = line.split(';')
				if len(data) >= 15:
					code_point = int(data[0], 16)
					m = range_re.search(data[1])
					if m:
						range_key = m.group(1)
						if range_key in range_memo:
							fcp = min(code_point, range_memo[range_key])
							lcp = max(code_point, range_memo[range_key])
							self.set_range_property('Name', fcp, lcp, (
								'CJK UNIFIED IDEOGRAPH-%04X' if range_key.startswith('CJK Ideograph') else
								'HANGUL SYLLABLE-%04X' if range_key.startswith('Hangul Syllable') else
								'HIGH SURROGATE-%04X' if range_key.endswith('High Surrogate') else
								'LOW SURROGATE-%04X' if range_key.endswith('Low Surrogate') else
								'PRIVATE USE-%04X' if range_key.endswith('Private Use') else
								'TANGUT IDEOGRAPH-%04X' if range_key.startswith('Tangut Ideograph') else
								'JURCHEN CHARACTER-%04X' if range_key.startswith('Jurchen Character') else
								'SEAL CHARACTER-%04X' if range_key.startswith('Seal Character') else
								(range_key.upper() + '-%04X')
							))
							self.set_range_property('General_Category', fcp, lcp, data[2])
							self.set_range_property('Canonical_Combining_Class', fcp, lcp, int(data[3]))
							self.set_range_property('Bidi_Class', fcp, lcp, data[4])
							self.set_range_property('Decomposition_Type', fcp, lcp, data[5].partition(' ')[0] if data[5] else None)
							self.set_range_property('Decomposition_Mapping', fcp, lcp, data[5].partition(' ')[2] if data[5] else None)
							self.set_range_property('Numeric_Type', fcp, lcp, 'Decimal' if data[6] else 'Digit' if data[7] else 'Numeric' if data[8] else None)
							self.set_range_property('Numeric_Value', fcp, lcp, data[6] if data[6] else data[7] if data[7] else data[8] if data[8] else None)
							self.set_range_property('Bidi_Mirrored', fcp, lcp, data[9] == 'Y')
							self.set_range_property('Unicode_1_Name', fcp, lcp, data[10] if data[10] else None)
							self.set_range_property('ISO_Comment', fcp, lcp, data[11] if data[11] else None)
							self.set_range_property('Simple_Uppercase_Mapping', fcp, lcp, data[12] if data[12] else None)
							self.set_range_property('Simple_Lowercase_Mapping', fcp, lcp, data[13] if data[13] else None)
							self.set_range_property('Simple_Titlecase_Mapping', fcp, lcp, data[14] if data[14] else None)
						else:
							range_memo[range_key] = code_point
					else:
						self.set_character_property('Name', code_point, data[1])
						self.set_character_property('General_Category', code_point, data[2])
						self.set_character_property('Canonical_Combining_Class', code_point, int(data[3]))
						self.set_character_property('Bidi_Class', code_point, data[4])
						self.set_character_property('Decomposition_Type', code_point, data[5].partition(' ')[0] if data[5] else None)
						self.set_character_property('Decomposition_Mapping', code_point, data[5].partition(' ')[2] if data[5] else None)
						self.set_character_property('Numeric_Type', code_point, 'Decimal' if data[6] else 'Digit' if data[7] else 'Numeric' if data[8] else None)
						self.set_character_property('Numeric_Value', code_point, data[6] if data[6] else data[7] if data[7] else data[8] if data[8] else None)
						self.set_character_property('Bidi_Mirrored', code_point, data[9] == 'Y')
						self.set_character_property('Unicode_1_Name', code_point, data[10] if data[10] else None)
						self.set_character_property('ISO_Comment', code_point, data[11] if data[11] else None)
						self.set_character_property('Simple_Uppercase_Mapping', code_point, data[12] if data[12] else None)
						self.set_character_property('Simple_Lowercase_Mapping', code_point, data[13] if data[13] else None)
						self.set_character_property('Simple_Titlecase_Mapping', code_point, data[14] if data[14] else None)

	def read_property(self, property):
		if property == 'Block':
			self.read_blocks()
		if property in [
			'Name', 'General_Category', 'Canonical_Combining_Class',
			'Bidi_Class', 'Decomposition_Type', 'Decomposition_Mapping',
			'Numeric_Type', 'Numeric_Value', 'Bidi_Mirrored',
			'Unicode_1_Name', 'ISO_Comment', 'Simple_Uppercase_Mapping',
			'Simple_Lowercase_Mapping', 'Simple_Titlecase_Mapping'
		]:
			self.read_unicodedata()

def main():
	ucd = UnicodeCharacterDatabase()
	args = sys.argv[1:]
	if args:
		for arg in args:
			if arg.endswith('.txt'):
				for line in read_file(arg):
					print(line)
			else:
				ucd.read_property(arg)
				if arg in ucd.character_properties:
					for cp in sorted(ucd.character_properties[arg]):
						if ucd.character_properties[arg][cp] is not None:
							print('%04X; %s' % (cp, ucd.character_properties[arg][cp]))
				if arg in ucd.range_properties:
					for fcp, lcp in sorted(ucd.range_properties[arg]):
						if ucd.range_properties[arg][(fcp, lcp)] is not None:
							print('%04X..%04X; %s' % (fcp, lcp, ucd.range_properties[arg][(fcp, lcp)]))
	else:
		for line in list_files():
			print(line)

if __name__ == '__main__':
	main()
