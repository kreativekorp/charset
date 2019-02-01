#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from bitsetlib import BitSet
from parselib import charset_path, load_plugin, ls
from ttflib import ttf_file

def get_font_file_data(path):
	ext = path.split('/')[-1].split('.')[-1].lower()
	if ext == 'bdf' or ext == 'bdfmeta':
		name = None
		chars = BitSet()
		vendorid = None
		with open(path, 'r') as bdf:
			for line in bdf:
				if line[:12] == 'FAMILY_NAME ':
					name = line[12:].strip()
					if (name[0] == '"' and name[-1] == '"') or (name[0] == "'" and name[-1] == "'"):
						name = name[1:-1]
				if line[:9] == 'ENCODING ':
					try:
						cp = int(line[9:].strip())
						chars.set(cp)
					except ValueError:
						pass
				if line[:11] == 'OS2_VENDOR ':
					vendorid = line[11:].strip()
					if (vendorid[0] == '"' and vendorid[-1] == '"') or (vendorid[0] == "'" and vendorid[-1] == "'"):
						vendorid = vendorid[1:-1]
		return name, chars, vendorid
	elif ext == 'ttf' or ext == 'ttfmeta' or ext == 'otf' or ext == 'otfmeta':
		name = None
		chars = BitSet()
		vendorid = None
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
			words = name.split(' ')
			if words[0] == 'Noto' and words[-1] in ['Bk', 'Black', 'Blk', 'Bold', 'Cn', 'Cond', 'DemiLight', 'ExtBd', 'ExtCond', 'ExtLt', 'ExtraLight', 'Light', 'Lt', 'Md', 'Med', 'Medium', 'SemBd', 'SemCond', 'SemiBold', 'SmBd', 'SmCn', 'Th', 'Thin', 'XBd', 'XCn', 'XLt']:
				# We really don't need every weight of Noto.
				return None
			# End Blacklisting

			for cmap in ttf.cmaps():
				for cp, glyph in cmap.glyphs():
					chars.set(cp)
			vendorid = ttf.vendorid()
		return name, chars, vendorid
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
			fonts[font_data[0]] = (font_data[0], newchars, newvendor, None)
		else:
			fonts[font_data[0]] = (font_data[0], font_data[1], font_data[2], None)
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
					fonts[font_data[0]] = (font_data[0], newchars, newvendor, url)
				else:
					fonts[font_data[0]] = (font_data[0], font_data[1], font_data[2], url)
	fonts = [fonts[k] for k in fonts]
	fonts.sort(key=lambda font: font[0].lower())
	return fonts

def main():
	for name, chars, vendorid, url in get_font_data():
		print('%s\t%s\t%s\t%s' % (name, vendorid, chars.popcount(), url))

if __name__ == '__main__':
	main()
