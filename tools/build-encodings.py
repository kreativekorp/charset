#!/usr/bin/env python3

import os
import re
import sys
import unicodedata

import bitset
import controlchars
import fontloader
import htmlgen
import thisrepo
import unicodedotorg

thisrepo.add_syspath('charsets', 'tools')
import tablint

class CharsetInfo:
	def __init__(self, bytes_to_chars, chars_to_bytes, name, aliases, ucd=None, font_chars=None):
		self.is_EBCDIC = controlchars.is_EBCDIC(bytes_to_chars, chars_to_bytes)
		self.is_FIELDATA = controlchars.is_FIELDATA(bytes_to_chars, chars_to_bytes)
		self.is_teletext = name.startswith('x-ets-300-706') or name.startswith('x-acorn-mode7')
		self.canon_sequences = {}
		self.alt_sequences = {}
		self.subtables = {}
		self.chars = bitset.BitSet()
		for bs in bytes_to_chars:
			cs = bytes_to_chars[bs]
			if bs not in self.canon_sequences:
				self.canon_sequences[bs] = {}
			if bs not in self.alt_sequences:
				self.alt_sequences[bs] = {}
			if cs in chars_to_bytes and chars_to_bytes[cs] == bs:
				self.canon_sequences[bs][cs] = cs
			else:
				self.alt_sequences[bs][cs] = cs
			for i in range(len(bs)):
				self.subtables[bs[0:i]] = bs[0:i]
			for c in cs:
				if 0x20 <= c < 0x7F or c >= 0xA0:
					self.chars.set(c)
		for cs in chars_to_bytes:
			bs = chars_to_bytes[cs]
			if bs not in self.canon_sequences:
				self.canon_sequences[bs] = {}
			if bs not in self.alt_sequences:
				self.alt_sequences[bs] = {}
			if bs in bytes_to_chars and bytes_to_chars[bs] == cs:
				self.canon_sequences[bs][cs] = cs
			else:
				self.alt_sequences[bs][cs] = cs
			for i in range(len(bs)):
				self.subtables[bs[0:i]] = bs[0:i]
			for c in cs:
				if 0x20 <= c < 0x7F or c >= 0xA0:
					self.chars.set(c)
		self.ucd = ucd
		self.font_chars = (
			None if font_chars is None else
			{k: bitset.intersect(self.chars, font_chars[k]) for k in font_chars}
		)
		self.name = name
		self.aliases = []
		for alias in aliases:
			self.add_name(alias)

	def add_name(self, name):
		if name != self.name and name not in self.aliases:
			self.aliases.append(name)

	def control_acronym(self, cp):
		if self.is_EBCDIC and cp in controlchars.EBCDIC_CONTROL_NAMES:
			return controlchars.EBCDIC_CONTROL_NAMES[cp][0]
		if self.is_FIELDATA and cp in controlchars.FIELDATA_CONTROL_NAMES:
			return controlchars.FIELDATA_CONTROL_NAMES[cp][0]
		if self.is_teletext and cp in controlchars.TELETEXT_CONTROL_NAMES:
			return controlchars.TELETEXT_CONTROL_NAMES[cp][0]
		if cp in controlchars.ASCII_CONTROL_NAMES:
			return controlchars.ASCII_CONTROL_NAMES[cp][0]
		return None

	def character_name(self, cp):
		if self.is_EBCDIC and cp in controlchars.EBCDIC_CONTROL_NAMES:
			return controlchars.EBCDIC_CONTROL_NAMES[cp][1]
		if self.is_FIELDATA and cp in controlchars.FIELDATA_CONTROL_NAMES:
			return controlchars.FIELDATA_CONTROL_NAMES[cp][1]
		if self.is_teletext and cp in controlchars.TELETEXT_CONTROL_NAMES:
			return controlchars.TELETEXT_CONTROL_NAMES[cp][1]
		if cp in controlchars.ASCII_CONTROL_NAMES:
			return controlchars.ASCII_CONTROL_NAMES[cp][1]
		if self.ucd is not None:
			name = self.ucd.get('Name', cp)
			if name is not None:
				return name
		return unicodedata.name(chr(cp), None)

	def char_cell(self, bs):
		boxes = []
		if bs in self.canon_sequences:
			for cs in sorted(self.canon_sequences[bs]):
				boxes.append(htmlgen.char_box(
					cs, canon=True,
					name_fn=lambda cp: self.character_name(cp),
					acro_fn=lambda cp: self.control_acronym(cp)
				))
		if bs in self.alt_sequences:
			for cs in sorted(self.alt_sequences[bs]):
				boxes.append(htmlgen.char_box(
					cs, canon=False,
					name_fn=lambda cp: self.character_name(cp),
					acro_fn=lambda cp: self.control_acronym(cp)
				))
		if bs in self.subtables:
			boxes.append(htmlgen.subtable_box(bs))
		return htmlgen.char_cell(boxes)

	def char_table(self, prefix):
		return htmlgen.char_table([self.char_cell(prefix + (i,)) for i in range(256)])

	def char_rows(self, bs):
		rows = []
		if bs in self.canon_sequences:
			for cs in sorted(self.canon_sequences[bs]):
				rows.append(htmlgen.char_row(
					cs, bs, canon=True,
					name_fn=lambda cp: self.character_name(cp),
					acro_fn=lambda cp: self.control_acronym(cp)
				))
		if bs in self.alt_sequences:
			for cs in sorted(self.alt_sequences[bs]):
				rows.append(htmlgen.char_row(
					cs, bs, canon=False,
					name_fn=lambda cp: self.character_name(cp),
					acro_fn=lambda cp: self.control_acronym(cp)
				))
		if bs in self.subtables:
			rows.append(htmlgen.subtable_row(bs))
		return rows

	def char_list(self, prefix):
		rows = []
		for i in range(256):
			rows.extend(self.char_rows(prefix + (i,)))
		return htmlgen.char_list(rows)

	def has_alternates(self):
		for bs in set(list(self.canon_sequences) + list(self.alt_sequences) + list(self.subtables)):
			n1 = len(self.canon_sequences[bs]) if bs in self.canon_sequences else 0
			n2 = len(self.alt_sequences[bs]) if bs in self.alt_sequences else 0
			n3 = 1 if bs in self.subtables else 0
			if n1 + n2 + n3 > 1:
				return True
		return False

	def write_index(self, out_file):
		print('Writing %s...' % out_file)
		lines = []
		lines.append(htmlgen.page_head(
			'Character Encodings - Legacy Encodings - %s - %s' % self.display_name,
			['unicopy', 'charlist2']
		))
		for prefix in sorted(self.subtables):
			if prefix:
				lines.append('<hr id="%s">' % ''.join('%02X' % b for b in prefix))
				lines.append(htmlgen.breadcrumb(
					None,
					('/charset/', 'Character Encodings'),
					('/charset/encoding/', 'Legacy Encodings'),
					('/charset/encoding/#%s' % self.display_name[0], self.display_name[0]),
					('#top', self.display_name[1])
				))
				lines.append('<h2>Starting with <code>%s</code></h2>' % ' '.join('%02X' % b for b in prefix))
			else:
				lines.append(htmlgen.breadcrumb(
					None,
					('/charset/', 'Character Encodings'),
					('/charset/encoding/', 'Legacy Encodings'),
					('/charset/encoding/#%s' % self.display_name[0], self.display_name[0])
				))
				lines.append('<h1>%s</h1>' % htmlgen.html_encode(self.display_name[1]))
				lines.append('<table>')
				if self.display_aliases:
					aka = htmlgen.html_encode(', '.join(sorted(a for c, a in self.display_aliases)))
					lines.append('<tr><th>Also Known As:</th><td>%s</td></tr>' % aka)
				if self.iana_names:
					iana_names = htmlgen.html_encode(', '.join(sorted(self.iana_names)))
					lines.append('<tr><th>IANA Charset:</th><td>%s</td></tr>' % iana_names)
				if self.iana_mibenum:
					iana_mibenum = htmlgen.html_encode(', '.join(str(i) for i in sorted(self.iana_mibenum)))
					lines.append('<tr><th>IANA MIBenum:</th><td>%s</td></tr>' % iana_mibenum)
				if self.ms_codepage:
					codepage = htmlgen.html_encode(', '.join(str(i) for i in sorted(self.ms_codepage)))
					lines.append('<tr><th>Windows Code Page:</th><td>%s</td></tr>' % codepage)
				if self.ms_dotnet_name:
					dotnet_name = htmlgen.html_encode(', '.join(sorted(self.ms_dotnet_name)))
					lines.append('<tr><th>.NET Name:</th><td>%s</td></tr>' % dotnet_name)
				if self.cf_string_encoding:
					cfse = ['<code>%s</code> (%d) [<code>0x%X</code>]' % (htmlgen.html_encode(k), v, v) for k, v in sorted(self.cf_string_encoding)]
					lines.append('<tr><th>CFStringEncoding:</th><td>%s</td></tr>' % ', '.join(cfse))
				if self.ns_string_encoding:
					nsse = ['<code>%s</code> (%d) [<code>0x%X</code>]' % (htmlgen.html_encode(k), v, v) for k, v in sorted(self.ns_string_encoding)]
					lines.append('<tr><th>NSStringEncoding:</th><td>%s</td></tr>' % ', '.join(nsse))
				name = htmlgen.html_encode(self.name)
				lines.append('<tr><th>Mapping File:</th><td>%s</td></tr>' % ' '.join([
					'<a href="https://github.com/kreativekorp/charsets/blob/main/tables/%s.txt" target="_blank">%s.txt</a>' % (name, name),
					'<a href="https://raw.githubusercontent.com/kreativekorp/charsets/refs/heads/main/tables/%s.txt" target="_blank">(Raw)</a>' % name,
					'<i>(Spot an error? <a href="https://github.com/kreativekorp/charsets/issues" target="_blank">Create an issue</a> or <a href="https://github.com/kreativekorp/charsets/pulls" target="_blank">open a pull request</a>.)</i>'
				]))
				if self.font_chars:
					lines.append('<tr><th>Font:</th><td>%s</td></tr>' % htmlgen.font_selector(self.chars, self.font_chars))
				if self.has_alternates():
					lines.append('<tr><th>Alternate Codes:</th><td><button class="show-alt-codes">Show</button> <button class="hide-alt-codes">Hide</button></td></tr>')
				lines.append('</table>')
			lines.append(self.char_table(prefix))
			lines.append(self.char_list(prefix))
		lines.append(htmlgen.page_tail(
			['jquery', 'ucd', 'pua', 'entitydb', 'psnamedb', 'unicopy', 'charlist2']
		))
		with open(out_file, 'w') as f:
			f.write('\n'.join(lines))

	def write_dir(self, out_dir):
		os.makedirs(out_dir, exist_ok=True)
		self.write_index(os.path.join(out_dir, 'index.shtml'))

class CharsetInfoCollection:
	def __init__(self, ucd=None, font_chars=None):
		self.ucd = ucd
		self.font_chars = font_chars
		self.charsets = {}
		self.add_charset_fn = lambda n, cn, b2c, c2b: self.add_charset(n, cn, b2c, c2b)

	def add_charset(self, name, canonical_name, bytes_to_chars, chars_to_bytes):
		if canonical_name in self.charsets:
			self.charsets[canonical_name].add_name(name)
		else:
			cs = CharsetInfo(bytes_to_chars, chars_to_bytes, canonical_name, [name], self.ucd, self.font_chars)
			self.charsets[canonical_name] = cs

	def read_tocs(self, toc_dir):
		self.charset_index = {}
		for cs in self.charsets:
			cs = self.charsets[cs]
			self.charset_index[cs.name] = cs.name
			for alias in cs.aliases:
				self.charset_index[alias] = cs.name
		# DisplayNames.txt
		self.display_name_index = {} # {category: {display_name: name}}
		self.display_name_map = {} # {name: (category, display_name)}
		with open(os.path.join(toc_dir, 'DisplayNames.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line, maxsplit=1)
				if len(fields) == 2 and fields[0] in self.charset_index:
					subfields = fields[1].split('|', maxsplit=1)
					category = 'Uncategorized' if len(subfields) < 2 else subfields[0]
					if category not in self.display_name_index:
						self.display_name_index[category] = {}
					self.display_name_index[category][subfields[-1]] = fields[0]
					self.display_name_map[fields[0]] = (category, subfields[-1])
		# IANA.txt
		self.iana_name_index = {} # {iana_name: repo_name}
		self.iana_name_map = {} # {repo_name: [iana_name]}
		self.iana_mibenum_index = {} # {mibenum: repo_name}
		self.iana_mibenum_map = {} # {repo_name: mibenum}
		with open(os.path.join(toc_dir, 'IANA.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) >= 2 and fields[-1] in self.charset_index:
					for name in fields[0:-2]:
						self.iana_name_index[name] = fields[-1]
					self.iana_name_map[fields[-1]] = fields[0:-2]
					self.iana_mibenum_index[int(fields[-2])] = fields[-1]
					self.iana_mibenum_map[fields[-1]] = int(fields[-2])
		# Microsoft.txt
		self.ms_codepage_index = {} # {(codepage, dotnet_name): repo_name}
		self.ms_codepage_map = {} # {repo_name: (codepage, dotnet_name)}
		with open(os.path.join(toc_dir, 'Microsoft.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) == 3 and fields[2] in self.charset_index:
					self.ms_codepage_index[(int(fields[0]), fields[1])] = fields[2]
					self.ms_codepage_map[fields[2]] = (int(fields[0]), fields[1])
		# CFStringEncoding.txt
		self.cf_string_encoding_index = {} # {(value, key): name}
		self.cf_string_encoding_map = {} # {name: (key, value)}
		with open(os.path.join(toc_dir, 'CFStringEncoding.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) == 3 and fields[2] in self.charset_index:
					self.cf_string_encoding_index[(int(fields[1]), fields[0])] = fields[2]
					self.cf_string_encoding_map[fields[2]] = (fields[0], int(fields[1]))
		# NSStringEncoding.txt
		self.ns_string_encoding_index = {} # {(value, key): name}
		self.ns_string_encoding_map = {} # {name: (key, value)}
		with open(os.path.join(toc_dir, 'NSStringEncoding.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) == 3 and fields[2] in self.charset_index:
					self.ns_string_encoding_index[(int(fields[1]), fields[0])] = fields[2]
					self.ns_string_encoding_map[fields[2]] = (fields[0], int(fields[1]))
		# KTEFiles.txt
		self.kte_id_index = {}
		self.kte_filename_index = {}
		with open(os.path.join(toc_dir, 'KTEFiles.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) == 3 and fields[2] in self.charset_index:
					self.kte_id_index[int(fields[1])] = fields[2]
					self.kte_filename_index[fields[0]] = fields[2]
		# OldNames.txt
		self.old_name_index = {}
		with open(os.path.join(toc_dir, 'OldNames.txt'), 'r') as f:
			for line in f:
				line = line.partition('#')[0].strip()
				fields = re.split(r'\s+', line)
				if len(fields) == 2 and fields[1] in self.charset_index:
					self.old_name_index[fields[0]] = fields[1]
		# Propagate to CharsetInfo
		for cs in self.charsets:
			cs = self.charsets[cs]
			if cs.name not in self.display_name_map:
				category = 'Uncategorized'
				if category not in self.display_name_index:
					self.display_name_index[category] = {}
				self.display_name_index[category][cs.name] = cs.name
				self.display_name_map[cs.name] = (category, cs.name)
			cs.display_name = self.display_name_map[cs.name]
			cs.display_aliases = [self.display_name_map[a] for a in cs.aliases if a in self.display_name_map]
			cs.iana_names = {}
			cs.iana_mibenum = {}
			cs.ms_codepage = {}
			cs.ms_dotnet_name = {}
			cs.cf_string_encoding = {}
			cs.ns_string_encoding = {}
			for name in [cs.name] + cs.aliases:
				if name in self.iana_name_map:
					for iana_name in self.iana_name_map[name]:
						cs.iana_names[iana_name] = iana_name
				if name in self.iana_mibenum_map:
					iana_mibenum = self.iana_mibenum_map[name]
					cs.iana_mibenum[iana_mibenum] = iana_mibenum
				if name in self.ms_codepage_map:
					codepage, dotnet_name = self.ms_codepage_map[name]
					cs.ms_codepage[codepage] = codepage
					if dotnet_name != '?':
						cs.ms_dotnet_name[dotnet_name] = dotnet_name
				if name in self.cf_string_encoding_map:
					cfse = self.cf_string_encoding_map[name]
					cs.cf_string_encoding[cfse] = cfse
				if name in self.ns_string_encoding_map:
					nsse = self.ns_string_encoding_map[name]
					cs.ns_string_encoding[nsse] = nsse

	def write_index(self, out_file):
		print('Writing %s...' % out_file)
		lines = []
		# Page Head
		lines.append(htmlgen.page_head('Character Encodings - Legacy Encodings', ['enclist']))
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings')))
		lines.append('<h1>Legacy Encodings</h1>')
		# Table of Contents
		lines.append('<p><b>Jump to Category:</b></p>')
		lines.append('<p>%s</p>' % ' &#183; '.join('<a href="#%s">%s</a>' % (s, s) for s in [
			htmlgen.html_encode(category) for category in sorted(self.display_name_index)
		]))
		lines.append('<p><b>Jump to Index:</b></p>')
		lines.append('<p>%s</p>' % ' &#183; '.join('<a href="#%s">%s</a>' % (a, b) for a, b in [
			('IANA', 'By IANA Charset'), ('MIBenum', 'By IANA MIBenum'),
			('Windows', 'By Windows Code Page'), ('dotNET', 'By .NET Name'),
			('CFStringEncoding', 'By CFStringEncoding'), ('NSStringEncoding', 'By NSStringEncoding')
		]))
		# By Category
		for category in sorted(self.display_name_index):
			lines.append('<hr id="%s">' % htmlgen.html_encode(category))
			lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
			lines.append('<h2>%s</h2>' % htmlgen.html_encode(category))
			lines.append('<div class="enclist-wrapper"><table class="enclist">')
			for display_name in sorted(self.display_name_index[category], key=htmlgen.natural_sort_key):
				html_name = htmlgen.html_encode(display_name)
				name = htmlgen.html_encode(self.display_name_index[category][display_name])
				lines.append('<tr><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (name, html_name))
			lines.append('</table></div>')
		# By IANA Charset
		lines.append('<hr id="IANA">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By IANA Charset</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>Name</th><th>MIBenum</th><th>Encoding</th></tr>')
		for iana_name in sorted(self.iana_name_index, key=htmlgen.natural_sort_key):
			lines.append('<tr><td>%s</td><td>%d</td><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (
				htmlgen.html_encode(iana_name),
				self.iana_mibenum_map[self.iana_name_index[iana_name]],
				htmlgen.html_encode(self.iana_name_index[iana_name]),
				htmlgen.html_encode(self.display_name_map[self.iana_name_index[iana_name]][1])
			))
		lines.append('</table></div>')
		# By IANA MIBenum
		lines.append('<hr id="MIBenum">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By IANA MIBenum</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>MIBenum</th><th>Encoding</th><th>Names</th></tr>')
		for mibenum in sorted(self.iana_mibenum_index):
			lines.append('<tr><td>%d</td><td><a href="/charset/encoding/%s/">%s</a></td><td>%s</td></tr>' % (
				mibenum,
				htmlgen.html_encode(self.iana_mibenum_index[mibenum]),
				htmlgen.html_encode(self.display_name_map[self.iana_mibenum_index[mibenum]][1]),
				htmlgen.html_encode(', '.join(self.iana_name_map[self.iana_mibenum_index[mibenum]]))
			))
		lines.append('</table></div>')
		# By Windows Code Page
		lines.append('<hr id="Windows">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By Windows Code Page</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>Code Page</th><th>.NET Name</th><th>Encoding</th></tr>')
		for codepage, dotnet_name in sorted(self.ms_codepage_index):
			lines.append('<tr><td>%d</td><td>%s</td><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (
				codepage, htmlgen.html_encode(dotnet_name),
				htmlgen.html_encode(self.ms_codepage_index[(codepage,dotnet_name)]),
				htmlgen.html_encode(self.display_name_map[self.ms_codepage_index[(codepage,dotnet_name)]][1])
			))
		lines.append('</table></div>')
		# By .NET Name
		lines.append('<hr id="dotNET">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By .NET Name</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>.NET Name</th><th>Code Page</th><th>Encoding</th></tr>')
		for codepage, dotnet_name in sorted(self.ms_codepage_index, key=lambda s: htmlgen.natural_sort_key(s[1])):
			lines.append('<tr><td>%s</td><td>%d</td><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (
				htmlgen.html_encode(dotnet_name), codepage,
				htmlgen.html_encode(self.ms_codepage_index[(codepage,dotnet_name)]),
				htmlgen.html_encode(self.display_name_map[self.ms_codepage_index[(codepage,dotnet_name)]][1])
			))
		lines.append('</table></div>')
		# By CFStringEncoding
		lines.append('<hr id="CFStringEncoding">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By CFStringEncoding</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>Identifier</th><th>Dec</th><th>Hex</th><th>Encoding</th></tr>')
		for v, k in sorted(self.cf_string_encoding_index):
			lines.append('<tr><td><code>%s</code></td><td>(%d)</td><td>[<code>0x%X</code>]</td><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (
				htmlgen.html_encode(k), v, v,
				htmlgen.html_encode(self.cf_string_encoding_index[(v,k)]),
				htmlgen.html_encode(self.display_name_map[self.cf_string_encoding_index[(v,k)]][1])
			))
		lines.append('</table></div>')
		# By NSStringEncoding
		lines.append('<hr id="NSStringEncoding">')
		lines.append(htmlgen.breadcrumb(None, ('/charset/', 'Character Encodings'), ('#top', 'Legacy Encodings')))
		lines.append('<h2>By NSStringEncoding</h2>')
		lines.append('<div class="enclist-wrapper"><table class="enclist">')
		lines.append('<tr><th>Identifier</th><th>Dec</th><th>Hex</th><th>Encoding</th></tr>')
		for v, k in sorted(self.ns_string_encoding_index):
			lines.append('<tr><td><code>%s</code></td><td>(%d)</td><td>[<code>0x%X</code>]</td><td><a href="/charset/encoding/%s/">%s</a></td></tr>' % (
				htmlgen.html_encode(k), v, v,
				htmlgen.html_encode(self.ns_string_encoding_index[(v,k)]),
				htmlgen.html_encode(self.display_name_map[self.ns_string_encoding_index[(v,k)]][1])
			))
		lines.append('</table></div>')
		# Page Tail
		lines.append(htmlgen.page_tail([]))
		with open(out_file, 'w') as f:
			f.write('\n'.join(lines))

	def write_dir(self, out_dir):
		os.makedirs(out_dir, exist_ok=True)
		for cs in self.charsets:
			cs = self.charsets[cs]
			# Encoding page
			cs.write_dir(os.path.join(out_dir, cs.name))
			# Redirects for aliases
			for alias in cs.aliases:
				redir_dir = os.path.join(out_dir, alias)
				os.makedirs(redir_dir, exist_ok=True)
				redir_file = os.path.join(redir_dir, 'index.php')
				htmlgen.create_redirect(redir_file, '/charset/encoding/%s/' % cs.name)
		# Redirects for old names
		for old_name in self.old_name_index:
			new_name = self.old_name_index[old_name]
			redir_dir = os.path.join(out_dir, old_name)
			os.makedirs(redir_dir, exist_ok=True)
			redir_file = os.path.join(redir_dir, 'index.php')
			htmlgen.create_redirect(redir_file, '/charset/encoding/%s/' % new_name)
		# Index page
		self.write_index(os.path.join(out_dir, 'index.shtml'))

	def write_encoding_php(self, php_file):
		print('Writing %s...' % php_file)
		lines = ['<?php']
		lines.append("if (isset($_GET['file'])) {")
		lines.append("\t$file = $_GET['file'];")
		lines.append("\tswitch ($file) {")
		for kte_file in self.kte_filename_index:
			lines.append("\t\tcase '%s': header('Location: /charset/encoding/%s/'); exit(0);" % (
				kte_file.replace('\\', '\\\\').replace("'", "\\'"),
				self.kte_filename_index[kte_file].replace('\\', '\\\\').replace("'", "\\'")
			))
		lines.append("\t}")
		lines.append("}")
		lines.append("if (isset($_GET['name'])) {")
		lines.append("\t$name = preg_replace('/[^A-Za-z0-9]+/', '', $_GET['name']);")
		lines.append("\tswitch ($name) {")
		for old_name in self.old_name_index:
			lines.append("\t\tcase '%s': header('Location: /charset/encoding/%s/'); exit(0);" % (
				old_name.replace('\\', '\\\\').replace("'", "\\'"),
				self.old_name_index[old_name].replace('\\', '\\\\').replace("'", "\\'")
			))
		lines.append("\t}")
		lines.append("}")
		lines.append("header('Location: /charset/encoding/');")
		with open(php_file, 'w') as f:
			f.write('\n'.join(lines))

def main():
	print('Reading unicode data...')
	ucd = unicodedotorg.UnicodeCharacterDatabase()
	ucd.read_blocks()
	ucd.read_unicodedata()
	print('Reading font data...')
	font_chars = {}
	for font in fontloader.load(thisrepo.charset_path('font-metadata'), verbosity=1, ignore_errors=True):
		if not fontloader.ignore_font(font):
			font_chars[font.name] = font.chars
	# We're cheating here. TODO: Port acquisition/fonts/* to python3.
	for font in fontloader.load(thisrepo.charset_path('.charset-cache', 'fonts.lst'), verbosity=1, ignore_errors=True):
		if not fontloader.ignore_font(font):
			font_chars[font.name] = font.chars
	print('Reading encoding data...')
	cic = CharsetInfoCollection(ucd, font_chars)
	toc_dir = thisrepo.charset_path('charsets', 'tocs')
	out_dir = thisrepo.charset_path('out', 'encoding')
	php_file = thisrepo.charset_path('out', 'encoding.php')
	args = sys.argv[1:]
	if args:
		parse_opts = True
		ok = True
		while args:
			arg = args.pop(0)
			if parse_opts and arg.startswith('-'):
				if arg == '--':
					parse_opts = False
				elif arg == '-t' and args:
					toc_dir = args.pop(0)
				elif arg == '-o' and args:
					out_dir = args.pop(0)
				elif arg == '-p' and args:
					php_file = args.pop(0)
				else:
					print('%s Unknown option: %s' % (tablint.ERROR, arg))
					ok = False
			elif not tablint.lint(arg, True, then_call=cic.add_charset_fn):
				ok = False
	else:
		tables = thisrepo.charset_path('charsets', 'tables')
		ok = tablint.lint(tables, True, then_call=cic.add_charset_fn)
	if ok:
		print(tablint.ALL_OK)
		cic.read_tocs(toc_dir)
		cic.write_dir(out_dir)
		cic.write_encoding_php(php_file)
	return ok

if __name__ == '__main__':
	if not main():
		sys.exit(1)
