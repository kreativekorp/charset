#!/usr/bin/env python

import os
import re

from bitsetlib import BitSet
from parselib import atline_matcher, cd, charset_path, expand, load_plugin, ls, strip_comment
from ttflib import ttf_file

def get_unidata():
	ranges = {}
	chars = {}
	blocks = []
	path = charset_path('acquisition', 'unidata')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			print('Reading Unicode data: %s' % modfile)
			for name, path in mod.list_files():
				if name == 'UnicodeData.txt':
					with open(path, 'r') as ucd:
						for line in ucd:
							fields = line.strip().split(';')
							try:
								cp = int(fields[0], 16)
								if fields[1][:1] == '<' and fields[1][-3:] == 'st>':
									range_name = fields[1][1:-1].split(', ')
									if range_name[0] not in ranges:
										ranges[range_name[0]] = [cp, cp, fields, fields]
									elif range_name[1] == 'First':
										ranges[range_name[0]][0] = cp
										ranges[range_name[0]][2] = fields
									elif range_name[1] == 'Last':
										ranges[range_name[0]][1] = cp
										ranges[range_name[0]][3] = fields
								else:
									chars[cp] = fields
							except ValueError:
								continue
				if name == 'Blocks.txt':
					with open(path, 'r') as bf:
						for line in bf:
							fields = line.strip().split(';')
							if len(fields) == 2:
								blockname = fields[1].strip()
								fields = fields[0].split('..')
								if len(fields) == 2:
									try:
										start = int(fields[0], 16)
										stop = int(fields[1], 16)
										blocks.append((start, stop, blockname))
									except ValueError:
										continue
	blocks.sort()
	return ranges, chars, blocks

def get_entities():
	entities = {}
	path = charset_path('acquisition', 'entities')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			print('Reading named HTML entities: %s' % modfile)
			for cp, entity in mod.list_entities():
				entities[cp] = entity
	return entities

def get_psnames():
	psnames = {}
	path = charset_path('acquisition', 'psnames')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			print('Reading PostScript names: %s' % modfile)
			for cp, psname in mod.list_psnames():
				psnames[cp] = psname
	return psnames

def _puaa_to_map(puadata, prop):
	map = {}
	if prop in puadata:
		for e in puadata[prop]:
			for cp in range(e.first_code_point, e.last_code_point + 1):
				if cp in map:
					map[cp] += e.get_property_string(cp)
				else:
					map[cp] = e.get_property_string(cp)
	return map

def _get_font_file_pua_data(puadata):
	if puadata is not None:
		puadata['Blocks'] = [(e.first_code_point, e.last_code_point, e.value) for e in puadata['Block']] if 'Block' in puadata else []
		names = _puaa_to_map(puadata, 'Name')
		categories = _puaa_to_map(puadata, 'General_Category')
		combClasses = _puaa_to_map(puadata, 'Canonical_Combining_Class')
		bidiClasses = _puaa_to_map(puadata, 'Bidi_Class')
		decompTypes = _puaa_to_map(puadata, 'Decomposition_Type')
		decompMappings = _puaa_to_map(puadata, 'Decomposition_Mapping')
		numericTypes = _puaa_to_map(puadata, 'Numeric_Type')
		numericValues = _puaa_to_map(puadata, 'Numeric_Value')
		bidiMirrored = _puaa_to_map(puadata, 'Bidi_Mirrored')
		uni1Names = _puaa_to_map(puadata, 'Unicode_1_Name')
		comments = _puaa_to_map(puadata, 'ISO_Comment')
		uppercase = _puaa_to_map(puadata, 'Simple_Uppercase_Mapping')
		lowercase = _puaa_to_map(puadata, 'Simple_Lowercase_Mapping')
		titlecase = _puaa_to_map(puadata, 'Simple_Titlecase_Mapping')
		puadata['UnicodeData'] = {cp: (
			('%04X' % cp),
			names[cp] if cp in names else ('UNDEFINED-%04X' % cp),
			categories[cp] if cp in categories else 'Cn',
			combClasses[cp] if cp in combClasses else '0',
			bidiClasses[cp] if cp in bidiClasses else 'N',
			(
				('%s %s' % (decompTypes[cp], decompMappings[cp])) if
				(cp in decompTypes and cp in decompMappings) else
				decompMappings[cp] if cp in decompMappings else ''
			),
			numericValues[cp] if (cp in numericValues and cp in numericTypes and numericTypes[cp] in ['Decimal']) else '',
			numericValues[cp] if (cp in numericValues and cp in numericTypes and numericTypes[cp] in ['Decimal', 'Digit']) else '',
			numericValues[cp] if (cp in numericValues and cp in numericTypes and numericTypes[cp] in ['Decimal', 'Digit', 'Numeric']) else '',
			bidiMirrored[cp] if cp in bidiMirrored else 'N',
			uni1Names[cp] if cp in uni1Names else '',
			comments[cp] if cp in comments else '',
			uppercase[cp] if cp in uppercase else '',
			lowercase[cp] if cp in lowercase else '',
			titlecase[cp] if cp in titlecase else ''
		) for cp in set().union(
			names.keys(), categories.keys(), combClasses.keys(),
			bidiClasses.keys(), decompTypes.keys(), decompMappings.keys(),
			numericTypes.keys(), numericValues.keys(), bidiMirrored.keys(),
			uni1Names.keys(), comments.keys(), uppercase.keys(),
			lowercase.keys(), titlecase.keys()
		)}
	return puadata

def get_font_file_data(path):
	ext = path.split('/')[-1].split('.')[-1].lower()
	if ext == 'bdf' or ext == 'bdfmeta':
		name = None
		chars = BitSet()
		vendorid = None
		puadata = None
		with open(path, 'r') as bdf:
			for line in bdf:
				if line[:12] == 'FAMILY_NAME ':
					name = line[12:].strip()
					if (name[0] == '"' and name[-1] == '"') or (name[0] == "'" and name[-1] == "'"):
						name = name[1:-1]
				if line[:9] == 'ENCODING ':
					try:
						cp = int(line[9:].strip())
						if (cp >= 0x20 and cp < 0x80) or cp >= 0xA0:
							chars.set(cp)
					except ValueError:
						pass
				if line[:11] == 'OS2_VENDOR ':
					vendorid = line[11:].strip()
					if (vendorid[0] == '"' and vendorid[-1] == '"') or (vendorid[0] == "'" and vendorid[-1] == "'"):
						vendorid = vendorid[1:-1]
		return name, chars, vendorid, puadata
	elif ext == 'ttf' or ext == 'ttfmeta' or ext == 'otf' or ext == 'otfmeta':
		name = None
		chars = BitSet()
		vendorid = None
		puadata = None
		with ttf_file(path) as ttf:
			name = ttf.name(False)
			if name[-8:] == ' Regular':
				name = name[:-8]

			# Start Blacklisting
			if name[0] == '.':
				# Font is private to system and normally inaccessible.
				return None
			if re.match('^[.]?Last[ ]?Resort$', name):
				# No. Just no.
				return None
			if re.match('^YOz[A-Z][A-Za-z0-9]+$', name):
				# We really don't need every weight of YOzFont.
				return None
			words = name.split(' ')
			if words[0] == 'Noto' and words[-1] in [
				'Bk', 'Black', 'Blk', 'Bold', 'Cn', 'Cond', 'Condensed', 'DemiLight',
				'ExBd', 'ExCd', 'ExLt', 'ExtBd', 'ExtCond', 'ExtLight', 'ExtLt',
				'ExtraBold', 'ExtraCond', 'ExtraCondensed', 'ExtraLight', 'Italic',
				'Light', 'Lt', 'Md', 'Med', 'Medium', 'SemBd', 'SemCond',
				'Semi', 'SemiBold', 'SemiCond', 'SemiCondensed', 'Semibold',
				'SmBd', 'SmCd', 'SmCn', 'Th', 'Thin', 'XBd', 'XCn', 'XLt'
			]:
				# We really don't need every weight of Noto.
				return None
			# End Blacklisting

			for cmap in ttf.cmaps():
				if cmap.isUnicode or cmap.isMacRoman:
					for cp, glyph in cmap.glyphs():
						if (cp >= 0x20 and cp < 0x80) or cp >= 0xA0:
							chars.set(cp)
			vendorid = ttf.vendorid()
			puadata = _get_font_file_pua_data(ttf.puaas())
		return name, chars, vendorid, puadata
	else:
		raise ValueError('Not a supported font format.')

def get_font_data():
	fonts = {}
	path = charset_path('font-metadata')
	for path in ls(path):
		print('Reading font data: %s' % path)
		try:
			font_data = get_font_file_data(path)
		except Exception as e:
			print('Error: %s' % e)
			continue
		if font_data is None:
			print('Skipping this font because reasons.')
		elif font_data[0] is None:
			print('Error: Font has no name.')
		elif font_data[0] in fonts:
			newchars = fonts[font_data[0]][1].update(font_data[1])
			newvendor = font_data[2] if fonts[font_data[0]][2] is None else fonts[font_data[0]][2]
			newpuadata = font_data[3] if fonts[font_data[0]][3] is None else fonts[font_data[0]][3]
			fonts[font_data[0]] = (font_data[0], newchars, newvendor, newpuadata, None)
		else:
			fonts[font_data[0]] = (font_data[0], font_data[1], font_data[2], font_data[3], None)
	path = charset_path('acquisition', 'fonts')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for name, path, url in mod.list_fonts():
				print('Reading font data: %s' % path)
				try:
					font_data = get_font_file_data(path)
				except Exception as e:
					print('Error: %s' % e)
					continue
				if font_data is None:
					print('Skipping this font because reasons.')
				elif font_data[0] is None:
					print('Error: Font has no name.')
				elif font_data[0] in fonts:
					newchars = fonts[font_data[0]][1].update(font_data[1])
					newvendor = font_data[2] if fonts[font_data[0]][2] is None else fonts[font_data[0]][2]
					newpuadata = font_data[3] if fonts[font_data[0]][3] is None else fonts[font_data[0]][3]
					newurl = url if fonts[font_data[0]][4] is None else fonts[font_data[0]][4]
					fonts[font_data[0]] = (font_data[0], newchars, newvendor, newpuadata, newurl)
				else:
					fonts[font_data[0]] = (font_data[0], font_data[1], font_data[2], font_data[3], url)
	fonts = [fonts[k] for k in fonts]
	fonts.sort(key=lambda font: font[0].lower())
	return fonts

def get_puadata():
	font_matcher = atline_matcher('font-name')
	vendor_matcher = atline_matcher('vendor-id')
	with cd(charset_path('puadata')):
		for path in ls('.'):
			if os.path.basename(path) == 'sources.txt':
				print('Reading Private Use Area data: %s' % path)
				meta = {'Font-Names': [], 'Vendor-IDs': []}
				chars = {}
				blocks = []
				for line in expand(path):
					if line:
						font_name = font_matcher.match(line)
						if font_name is not None:
							meta['Font-Names'].append(font_name)
							continue
						vendor_id = vendor_matcher.match(line)
						if vendor_id is not None:
							meta['Vendor-IDs'].append(vendor_id)
							continue
						fields = strip_comment(line).split(':', 2)
						if len(fields) == 2:
							meta[fields[0].strip()] = fields[1].strip()
					else:
						break
				for line in expand(os.path.join(os.path.dirname(path), 'unicodedata.txt')):
					fields = line.split(';')
					try:
						cp = int(fields[0], 16)
						chars[cp] = fields
					except ValueError:
						continue
				for line in expand(os.path.join(os.path.dirname(path), 'blocks.txt')):
					fields = line.split(';')
					if len(fields) == 2:
						blockname = fields[1].strip()
						fields = fields[0].split('..')
						if len(fields) == 2:
							try:
								start = int(fields[0], 16)
								stop = int(fields[1], 16)
								blocks.append((start, stop, blockname))
							except ValueError:
								continue
				blocks.sort()
				yield meta, chars, blocks
