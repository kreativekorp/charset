#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import charset_path, load_plugin, ls
from ttflib import ttf_file

def get_font_file_data(path):
	name = None
	chars = []
	vendorid = None
	ext = path.split('/')[-1].split('.')[-1].lower()
	if ext == 'bdf' or ext == 'bdfmeta':
		with open(path, 'r') as bdf:
			for line in bdf:
				if line[:12] == 'FAMILY_NAME ':
					name = line[12:].strip()
					if (name[0] == '"' and name[-1] == '"') or (name[0] == "'" and name[-1] == "'"):
						name = name[1:-1]
				if line[:9] == 'ENCODING ':
					try:
						cp = int(line[9:].strip())
						chars.append(cp)
					except ValueError:
						pass
				if line[:11] == 'OS2_VENDOR ':
					vendorid = line[11:].strip()
					if (vendorid[0] == '"' and vendorid[-1] == '"') or (vendorid[0] == "'" and vendorid[-1] == "'"):
						vendorid = vendorid[1:-1]
	if ext == 'ttf' or ext == 'ttfmeta' or ext == 'otf' or ext == 'otfmeta':
		with ttf_file(path) as ttf:
			name = ttf.name(False)
			if name[-8:] == ' Regular':
				name = name[:-8]
			for cmap in ttf.cmaps():
				for cp, glyph in cmap.glyphs():
					chars.append(cp)
				chars = list(set(chars))
			vendorid = ttf.vendorid()
	return name, chars, vendorid

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
		if font_data is not None and font_data[0] is not None and font_data[0][0] != '.':
			if font_data[0] in fonts:
				newchars = list(set(fonts[font_data[0]][1] + font_data[1]))
				newvendor = font_data[2] if fonts[font_data[0]][2] is None else fonts[font_data[0]][2]
				fonts[font_data[0]] = (font_data[0], newchars, newvendor)
			else:
				fonts[font_data[0]] = font_data
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
				if font_data is not None and font_data[0] is not None and font_data[0][0] != '.':
					if font_data[0] in fonts:
						newchars = list(set(fonts[font_data[0]][1] + font_data[1]))
						newvendor = font_data[2] if fonts[font_data[0]][2] is None else fonts[font_data[0]][2]
						fonts[font_data[0]] = (font_data[0], newchars, newvendor)
					else:
						fonts[font_data[0]] = font_data
	fonts = [fonts[k] for k in fonts]
	fonts.sort(key=lambda font: font[0].lower())
	return fonts

def main():
	for name, chars, vendorid in get_font_data():
		print('%s\t%s\t%s' % (name, vendorid, len(chars)))

if __name__ == '__main__':
	main()
