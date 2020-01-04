#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from bitsetlib import BitSet
from parselib import cd, charset_path, expand, load_plugin, ls, split_atline, split_mapline
from ttflib import ttf_file
from unicodelib import hex_dump

def get_unidata():
	ranges = {}
	chars = {}
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
	return ranges, chars

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
						if (cp >= 0x20 and cp < 0x80) or cp >= 0xA0:
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
			if re.match('^YOz[A-Z][A-Za-z0-9]+$', name):
				# We really don't need every weight of YOzFont.
				return None
			words = name.split(' ')
			if words[0] == 'Noto' and words[-1] in ['Bk', 'Black', 'Blk', 'Bold', 'Cn', 'Cond', 'DemiLight', 'ExtBd', 'ExtCond', 'ExtLt', 'ExtraLight', 'Light', 'Lt', 'Md', 'Med', 'Medium', 'SemBd', 'SemCond', 'SemiBold', 'SmBd', 'SmCn', 'Th', 'Thin', 'XBd', 'XCn', 'XLt']:
				# We really don't need every weight of Noto.
				return None
			# End Blacklisting

			for cmap in ttf.cmaps():
				for cp, glyph in cmap.glyphs():
					if (cp >= 0x20 and cp < 0x80) or cp >= 0xA0:
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

def read_encoding(path):
	meta = {}
	map = {}
	print('Reading encoding data: %s' % path)
	for line in expand(path):
		k, v = split_atline(line)
		if k is not None and v is not None:
			if k in meta:
				meta[k].append(v)
			else:
				meta[k] = [v]
			continue
		b, c, ba, ca = split_mapline(line)
		if b is not None and c is not None:
			if not ba or tuple(b) not in map:
				map[tuple(b)] = tuple(c)
			continue

	if 'category' in meta and len(meta['category']) > 0:
		category = meta['category'][0]
	else:
		category = 'Unsorted'
	meta['category'] = category

	display = []
	name = []
	if 'display' in meta:
		display += meta['display']
	if 'name' in meta:
		display += meta['name']
		name += meta['name']
	if 'display' in meta:
		name += meta['display']
	if 'alias' in meta:
		display += meta['alias']
		name += meta['alias']
	if 'charset' in meta:
		display += meta['charset']
		name += meta['charset']
	if len(display) > 0:
		display_other = display[1:]
		display = display[0]
	else:
		display_other = None
		display = None
	if len(name) > 0:
		name_other = [re.sub('[^A-Za-z0-9]+', '', n) for n in name[1:]]
		name = re.sub('[^A-Za-z0-9]+', '', name[0])
	else:
		name_other = None
		name = None
	meta['display'] = display
	meta['display_other'] = display_other
	meta['name'] = name
	meta['name_other'] = name_other

	def tree_insert(tree, k, v):
		if len(k) == 1:
			tree['leaf'][k[0]] = v
		if len(k) > 1:
			if k[0] not in tree['branch']:
				tree['branch'][k[0]] = {'leaf': {}, 'branch': {}}
			tree_insert(tree['branch'][k[0]], k[1:], v)

	root = {'leaf': {}, 'branch': {}}
	for k in map:
		tree_insert(root, k, map[k])
	return meta, root

def nat_key(s):
	def pad_num(m):
		n = m.group(0)
		while len(n) < 20:
			n = '0' + n
		return n
	return re.sub('[0-9]+', pad_num, s.lower())

def html_encode(s):
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def char_cell(cp, ranges, chars, root, prefix, url):
	if cp in root['branch']:
		return '<td class="char-subtable"><a href="%s/%02X" class="char-subtable-link">%02X</a></td>' % (url, cp, cp)
	if cp not in root['leaf']:
		return '<td class="char-nonchar"><div class="char-empty"></div></td>'
	classes = ['char-uni', 'char-def']
	cps = root['leaf'][cp]
	title = []
	glyphs = []
	cptext = []
	if cps[0] == 0x202D and cps[-1] == 0x202C:
		classes.append('char-ltr')
		cps = cps[1:-1]
		title.append('&lt;Left-to-Right&gt;')
	elif cps[0] == 0x202E and cps[-1] == 0x202C:
		classes.append('char-rtl')
		cps = cps[1:-1]
		title.append('&lt;Right-to-Left&gt;')
	if cps[-1] == 0xFE0D:
		classes.append('char-rev')
		cps = cps[:-1]
		title.append('&lt;Reverse-Video&gt;')
	for cp in cps:
		if cp < 0x20 or (cp >= 0x7F and cp < 0xA0):
			classes[0] = 'char-control'
			title.append(html_encode(chars[cp][10]))
		else:
			if (cp >= 0xE000 and cp < 0xF900) or cp >= 0xF0000:
				classes[0] = 'char-pua'
			if cp in chars:
				title.append(html_encode(chars[cp][1]))
			else:
				for rangename in ranges:
					r = ranges[rangename]
					if cp >= r[0] and cp <= r[1]:
						if rangename[-11:] == 'Private Use':
							title.append('PRIVATE USE-%04X' % cp)
						elif rangename[:13] == 'CJK Ideograph':
							title.append('CJK UNIFIED IDEOGRAPH-%04X' % cp)
						else:
							title.append('%s-%04X' % (html_encode(rangename.upper()), cp))
						break
				else:
					classes[1] = 'char-undef'
					title.append('UNDEFINED-%04X' % cp)
			glyphs.append('&#%s;' % cp)
		cptext.append('%04X' % cp)
	if classes[0] == 'char-control':
		classes.pop(1)
	return '<td class="%s" data-codepoint="%s" title="%s"><div class="char-glyph">%s</div><div class="char-code">%s</div></td>' % (' '.join(classes), ','.join(str(cp) for cp in cps), ', '.join(title), ''.join(glyphs), '+'.join(cptext))

def char_row(cp, ranges, chars, root, prefix, url):
	bcell = '<td class="charlist-codepoint">%s</td>' % ''.join('%02X' % b for b in prefix + [cp])
	if cp in root['branch']:
		cpcell = '<td class="charlist-codepoint"></td>'
		gcell = '<td class="charlist-charglyph"></td>'
		ncell = '<td class="charlist-charname"><a href="%s/%02X">&lt;Subtable <code>%s</code>&gt;</a></td>' % (url, cp, hex_dump(prefix + [cp]))
	else:
		cptext = []
		classes = ['charlist-charglyph']
		cps = root['leaf'][cp]
		glyphs = []
		title = []
		if cps[0] == 0x202D and cps[-1] == 0x202C:
			classes.append('charlist-charglyph-ltr')
			cps = cps[1:-1]
			title.append('&lt;Left-to-Right&gt;')
		elif cps[0] == 0x202E and cps[-1] == 0x202C:
			classes.append('charlist-charglyph-rtl')
			cps = cps[1:-1]
			title.append('&lt;Right-to-Left&gt;')
		if cps[-1] == 0xFE0D:
			classes.append('charlist-charglyph-rev')
			cps = cps[:-1]
			title.append('&lt;Reverse-Video&gt;')
		for cp in cps:
			cptext.append('%04X' % cp)
			if cp < 0x20 or (cp >= 0x7F and cp < 0xA0):
				title.append('<a href="/charset/unicode/char/%04X">%s</a>' % (cp, html_encode(chars[cp][10])))
			else:
				glyphs.append('&#%s;' % cp)
				if cp in chars:
					title.append('<a href="/charset/unicode/char/%04X">%s</a>' % (cp, html_encode(chars[cp][1])))
				else:
					for rangename in ranges:
						r = ranges[rangename]
						if cp >= r[0] and cp <= r[1]:
							if rangename[-11:] == 'Private Use':
								title.append('PRIVATE USE-%04X' % cp)
							elif rangename[:13] == 'CJK Ideograph':
								title.append('CJK UNIFIED IDEOGRAPH-%04X' % cp)
							else:
								title.append('%s-%04X' % (html_encode(rangename.upper()), cp))
							break
					else:
						title.append('UNDEFINED-%04X' % cp)
		cpcell = '<td class="charlist-codepoint">%s</td>' % '+'.join(cptext)
		gcell = '<td class="%s" data-codepoint="%s"><span>%s</span></td>' % (' '.join(classes), ','.join(str(cp) for cp in cps), ''.join(glyphs))
		ncell = '<td class="charlist-charname">%s</td>' % ', '.join(title)
	return '<tr>' + bcell + cpcell + gcell + ncell + '</tr>'

def font_supports(fd1, leaf):
	for k in leaf:
		cps = leaf[k]
		if (cps[0] == 0x202D or cps[0] == 0x202E) and cps[-1] == 0x202C:
			cps = cps[1:-1]
		if cps[-1] == 0xFE0D:
			cps = cps[:-1]
		for cp in cps:
			if fd1.get(cp):
				return True
	return False

def encoding_link(meta):
	link = '<a href="/charset/encoding/%s">%s</a>' % (html_encode(meta['name']), html_encode(meta['display']))
	if 'display_other' in meta:
		dn = meta['display_other']
		if 'charset' in meta:
			for cs in meta['charset']:
				if cs in dn:
					dn.remove(cs)
		if len(dn) > 0:
			link += '<span class="encoding-aka">, %s</span>' % ', '.join(html_encode(n) for n in dn)
	return link

def build_encoding(ranges, chars, fonts, meta, root, basedir, prefix=[]):
	if not os.path.exists(basedir):
		os.makedirs(basedir)
	path = os.path.join(basedir, 'index.shtml')
	print('Writing encoding page: %s' % path)
	with open(path, 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		if len(prefix) > 0:
			print('<title>Character Encodings - Legacy Encodings - %s - Starting with %s</title>' % (html_encode(meta['display']), hex_dump(prefix)), file=f)
		else:
			print('<title>Character Encodings - Legacy Encodings - %s</title>' % html_encode(meta['display']), file=f)
		print('<link rel="stylesheet" href="/charset/shared/unicopy.css">', file=f)
		print('<link rel="stylesheet" href="/charset/shared/charlist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		if len(prefix) > 0:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/encoding/">Legacy Encodings</a> &raquo; <a href="/charset/encoding/%s">%s</a> &raquo;</p>' % (html_encode(meta['name']), html_encode(meta['display'])), file=f)
			print('<h1>Starting with <code>%s</code></h1>' % hex_dump(prefix), file=f)
		else:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/encoding/">Legacy Encodings</a> &raquo;</p>', file=f)
			print('<h1>%s</h1>' % html_encode(meta['display']), file=f)
		table_rows = []
		if 'display_other' in meta:
			dn = meta['display_other']
			if 'charset' in meta:
				for cs in meta['charset']:
					if cs in dn:
						dn.remove(cs)
			if len(dn) > 0:
				table_rows.append('<tr><td>Also Known As:</td><td>%s</td></tr>' % ', '.join(html_encode(n) for n in dn))
		if 'charset' in meta and len(meta['charset']) > 0:
			table_rows.append('<tr><td>IANA Charset:</td><td>%s</td></tr>' % ', '.join('<code>%s</code>' % html_encode(cs) for cs in meta['charset']))
		if 'mibenum' in meta and len(meta['mibenum']) > 0:
			table_rows.append('<tr><td>IANA MIBenum:</td><td>%s</td></tr>' % ', '.join(html_encode(i) for i in meta['mibenum']))
		if 'codepage' in meta and len(meta['codepage']) > 0:
			table_rows.append('<tr><td>Code Page:</td><td>%s</td></tr>' % ', '.join(html_encode(i) for i in meta['codepage']))
		if 'cfstringencoding' in meta and len(meta['cfstringencoding']) > 0:
			table_rows.append('<tr><td>CFStringEncoding:</td><td>%s</td></tr>' % ', '.join(html_encode(i) for i in meta['cfstringencoding']))
		if 'nsstringencoding' in meta and len(meta['nsstringencoding']) > 0:
			table_rows.append('<tr><td>NSStringEncoding:</td><td>%s</td></tr>' % ', '.join(html_encode(i) for i in meta['nsstringencoding']))
		if len(table_rows) > 0:
			print('<table>', file=f)
			for table_row in table_rows:
				print(table_row, file=f)
			print('</table>', file=f)
		if len(prefix) > 0:
			print('<p>Showing multibyte sequences starting with <code>%s</code>. <a href="/charset/encoding/%s%s">Go back.</a></p>' % (hex_dump(prefix), html_encode(meta['name']), ''.join('/%02X' % b for b in prefix[:-1])), file=f)
		print('<table class="block-subheader"><tr>', file=f)
		print('<td class="block-fonts">Font: <select id="font-selector">', file=f)
		print('<option selected value="inherit">Default</option>', file=f)
		for font_data in fonts:
			if font_supports(font_data[1], root['leaf']):
				font_name = html_encode(font_data[0])
				print('<option value="%s">%s</option>' % (font_name, font_name), file=f)
		print('</select></td>', file=f)
		if 'verify-against' in meta and len(meta['verify-against']) > 0:
			print('<td class="block-links"><a href="%s" target="_blank">Mapping File</a></td>' % html_encode(meta['verify-against'][0]), file=f)
		elif 'generate-txt' in meta and len(meta['generate-txt']) > 0:
			print('<td class="block-links"><a href="/charset/MAPPINGS/%s" target="_blank">Mapping File</a></td>' % html_encode(meta['generate-txt'][0]), file=f)
		else:
			print('<td class="block-links"></td>', file=f)
		print('</tr></table>', file=f)
		baseurl = '/charset/encoding/%s%s' % (html_encode(meta['name']), ''.join('/%02X' % b for b in prefix))
		print('<table class="char-table">', file=f)
		print('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>', file=f)
		for j in range(0, 16):
			cells = [char_cell(k, ranges, chars, root, prefix, baseurl) for k in range(j << 4, (j + 1) << 4)]
			print('<tr><th>%01X</th>%s</tr>' % (j, ''.join(cells)), file=f)
		print('</table>', file=f)
		codepoints = sorted(list(set([cp for cp in root['leaf']] + [cp for cp in root['branch']])))
		if len(codepoints) > 0:
			midpoint = (len(codepoints) + 1) >> 1
			print('<div class="charlist-outer-div">', file=f)
			print('<div class="charlist-inner-div">', file=f)
			print('<table class="charlist">', file=f)
			for cp in codepoints[:midpoint]:
				print(char_row(cp, ranges, chars, root, prefix, baseurl), file=f)
			print('</table>', file=f)
			print('</div><div class="charlist-inner-div">', file=f)
			print('<table class="charlist">', file=f)
			for cp in codepoints[midpoint:]:
				print(char_row(cp, ranges, chars, root, prefix, baseurl), file=f)
			print('</table>', file=f)
			print('</div>', file=f)
			print('</div>', file=f)
		print('<script src="/charset/shared/jquery.js"></script>', file=f)
		print('<script src="/charset/shared/ucd.js"></script>', file=f)
		print('<script src="/charset/shared/pua.js"></script>', file=f)
		print('<script src="/charset/shared/entitydb.js"></script>', file=f)
		print('<script src="/charset/shared/unicopy.js"></script>', file=f)
		print('<script src="/charset/shared/charlist.js"></script>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)
	for k in root['branch']:
		build_encoding(ranges, chars, fonts, meta, root['branch'][k], os.path.join(basedir, '%02X' % k), prefix + [k])

def main():
	categories = {}
	by_charset = {}
	by_mibenum = {}
	by_codepage = {}
	by_cfstrenc = {}
	by_nsstrenc = {}
	by_name = {}
	by_kte = {}
	ranges, chars = get_unidata()
	fonts = get_font_data()
	with cd(charset_path('mappings')):
		for path in ls('.'):
			meta, root = read_encoding(path)
			if meta['display'] is None or meta['name'] is None:
				print('Skipping: Is a fragment or encoding has no name.')
				continue
			basedir = charset_path('out', 'encoding', meta['name'])
			build_encoding(ranges, chars, fonts, meta, root, basedir)
			if meta['category'] in categories:
				categories[meta['category']].append(meta)
			else:
				categories[meta['category']] = [meta]
			if 'charset' in meta:
				for cs in meta['charset']:
					by_charset[cs] = meta
			if 'mibenum' in meta:
				for i in meta['mibenum']:
					try:
						by_mibenum[int(i)] = meta
					except ValueError:
						pass
			if 'codepage' in meta:
				for i in meta['codepage']:
					try:
						by_codepage[int(i)] = meta
					except ValueError:
						pass
			if 'cfstringencoding' in meta:
				for i in meta['cfstringencoding']:
					try:
						by_cfstrenc[int(i)] = meta
					except ValueError:
						pass
			if 'nsstringencoding' in meta:
				for i in meta['nsstringencoding']:
					try:
						by_nsstrenc[int(i)] = meta
					except ValueError:
						pass
			by_name[meta['name']] = meta
			for n in meta['name_other']:
				by_name[n] = meta
			if 'filename-kte' in meta:
				for n in meta['filename-kte']:
					by_kte[n] = meta

	basedir = charset_path('out', 'encoding')
	if not os.path.exists(basedir):
		os.makedirs(basedir)
	path = os.path.join(basedir, 'index.shtml')
	print('Writing encoding index: %s' % path)
	with open(path, 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		print('<title>Character Encodings - Legacy Encodings</title>', file=f)
		print('<link rel="stylesheet" href="/charset/shared/enclist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo;</p>', file=f)
		print('<h1>Legacy Encodings</h1>', file=f)
		for category in sorted(categories, key=nat_key):
			print('<h2>%s</h2>' % html_encode(category), file=f)
			print('<div class="enclist-wrapper"><table class="enclist">', file=f)
			for m in sorted(categories[category], key=lambda m: nat_key(m['display'])):
				print('<tr><td>%s</td></tr>' % encoding_link(m), file=f)
			print('</table></div>', file=f)
		print('<h2>By IANA Charset</h2>', file=f)
		print('<div class="enclist-wrapper"><table class="enclist">', file=f)
		for cs in sorted(by_charset, key=nat_key):
			print('<tr><td class="charset">%s</td><td>%s</td></tr>' % (cs, encoding_link(by_charset[cs])), file=f)
		print('</table></div>', file=f)
		print('<h2>By IANA MIBenum</h2>', file=f)
		print('<div class="enclist-wrapper"><table class="enclist">', file=f)
		for i in sorted(by_mibenum):
			print('<tr><td>%d</td><td>%s</td></tr>' % (i, encoding_link(by_mibenum[i])), file=f)
		print('</table></div>', file=f)
		print('<h2>By Code Page</h2>', file=f)
		print('<div class="enclist-wrapper"><table class="enclist">', file=f)
		for i in sorted(by_codepage):
			print('<tr><td>%03d</td><td>%s</td></tr>' % (i, encoding_link(by_codepage[i])), file=f)
		print('</table></div>', file=f)
		print('<h2>By CFStringEncoding</h2>', file=f)
		print('<div class="enclist-wrapper"><table class="enclist">', file=f)
		for i in sorted(by_cfstrenc):
			print('<tr><td>%d</td><td>%s</td></tr>' % (i, encoding_link(by_cfstrenc[i])), file=f)
		print('</table></div>', file=f)
		print('<h2>By NSStringEncoding</h2>', file=f)
		print('<div class="enclist-wrapper"><table class="enclist">', file=f)
		for i in sorted(by_nsstrenc):
			print('<tr><td>%d</td><td>%s</td></tr>' % (i, encoding_link(by_nsstrenc[i])), file=f)
		print('</table></div>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

	path = charset_path('out', 'encoding.php')
	print('Writing encoding redirect: %s' % path)
	with open(path, 'w') as f:
		print('<?php', file=f)
		print('if (isset($_GET[\'file\'])) {', file=f)
		print('\t$file = $_GET[\'file\'];', file=f)
		print('\tswitch ($file) {', file=f)
		for k in sorted(by_kte):
			print('\t\tcase \'%s\': header(\'Location: /charset/encoding/%s\'); exit(0);' % (k, by_kte[k]['name']), file=f)
		print('\t}', file=f)
		print('}', file=f)
		print('if (isset($_GET[\'name\'])) {', file=f)
		print('\t$name = preg_replace(\'/[^A-Za-z0-9]+/\', \'\', $_GET[\'name\']);', file=f)
		print('\tswitch ($name) {', file=f)
		for k in sorted(by_name):
			print('\t\tcase \'%s\': header(\'Location: /charset/encoding/%s\'); exit(0);' % (k, by_name[k]['name']), file=f)
		print('\t}', file=f)
		print('}', file=f)
		print('header(\'Location: /charset/encoding/\');', file=f)

if __name__ == '__main__':
	main()
