#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import cd, charset_path, expand, load_plugin, ls

def get_unidata():
	ranges = {}
	chars = {}
	blocks = []
	path = charset_path('acquisition', 'unidata')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
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

def get_puadata():
	with cd(charset_path('puadata')):
		for path in ls('.'):
			if os.path.basename(path) == 'sources.txt':
				meta = {}
				chars = {}
				blocks = []
				for line in expand(path):
					if line:
						fields = line.split(':', 2)
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

def get_entities():
	entities = {}
	path = charset_path('acquisition', 'entities')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for cp, entity in mod.list_entities():
				if cp not in entities:
					entities[cp] = entity
	return entities

def html_encode(s):
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def plane_name(p):
	if p == 0:
		return 'Basic Multilingual Plane (BMP)'
	if p == 1:
		return 'Supplementary Multilingual Plane (SMP)'
	if p == 2:
		return 'Supplementary Ideographic Plane (SIP)'
	if p == 3:
		return 'Tertiary Ideographic Plane (TIP)'
	if p == 14:
		return 'Supplementary Special-Purpose Plane (SSP)'
	if p == 15:
		return 'Supplementary Private Use Area-A'
	if p == 16:
		return 'Supplementary Private Use Area-B'
	return 'Plane ' + str(p)

def char_cell(cp, ranges, chars, url):
	if cp < 0 or (cp >= 0xFDD0 and cp < 0xFDF0) or cp >= 0x110000 or (cp & 0xFFFF) >= 0xFFFE:
		return '<td class="char-nonchar" data-codepoint="%s"><div class="char-glyph"></div><div class="char-code">%04X</div></td>' % (cp, cp)
	if cp >= 0xD800 and cp < 0xE000:
		return '<td class="char-surrogate" data-codepoint="%s"><div class="char-glyph"></div><div class="char-code">%04X</div></td>' % (cp, cp)
	if cp < 0x20 or (cp >= 0x7F and cp < 0xA0):
		return '<td class="char-control" data-codepoint="%s" title="%s"><div class="char-glyph"></div><div class="char-code">%04X</div></td>' % (cp, html_encode(chars[cp][10]), cp)
	if (cp >= 0xE000 and cp < 0xF900) or cp >= 0xF0000:
		classes = ['char-pua']
	else:
		classes = ['char-uni']
	if cp in chars:
		classes.append('char-def')
		htmlname = html_encode(chars[cp][1])
	elif ranges is not None:
		for rangename in ranges:
			r = ranges[rangename]
			if cp >= r[0] and cp <= r[1]:
				classes.append('char-def')
				if rangename[-11:] == 'Private Use':
					htmlname = 'PRIVATE USE-%04X' % cp
				elif rangename[:13] == 'CJK Ideograph':
					htmlname = 'CJK UNIFIED IDEOGRAPH-%04X' % cp
				else:
					htmlname = '%s-%04X' % (html_encode(rangename.upper()), cp)
				break
		else:
			classes.append('char-undef')
			htmlname = ''
	else:
		classes.append('char-undef')
		htmlname = ''
	return '<td class="%s" data-codepoint="%s" title="%s"><div class="char-glyph">&#%s;</div><div class="char-code">%04X</div></td>' % (' '.join(classes), cp, htmlname, cp, cp)

def char_row(cp, data, url):
	cpcell = '<td class="charlist-codepoint">%04X</td>' % cp
	if cp < 0x20 or (cp >= 0x7F and cp < 0xA0):
		gcell = '<td class="charlist-charglyph" data-codepoint="%s"></td>' % cp
		ncell = '<td class="charlist-charname"><a href="%s%04X">%s</a></td>' % (url, cp, data[10])
	else:
		gcell = '<td class="charlist-charglyph" data-codepoint="%s">&#%s;</td>' % (cp, cp)
		ncell = '<td class="charlist-charname"><a href="%s%04X">%s</a></td>' % (url, cp, data[1])
	return '<tr>' + cpcell + gcell + ncell + '</tr>'

def build_roadmap(complete, blocks, plane, urlbase, f):
	blocks = [b for b in blocks if (b[0] >> 16) == plane]
	minrow = (plane << 8) if complete else (min(b[0] for b in blocks) >> 8)
	maxrow = ((minrow | 0xFF) if complete else (max(b[1] for b in blocks) >> 8)) + 1
	print('<table class="block-roadmap hidden" id="block-roadmap-%s">' % plane, file=f)
	print('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>', file=f)
	for i in range(minrow, maxrow):
		blocks_in_row = [b for b in blocks if (b[0] >> 8) <= i and (b[1] >> 8) >= i]
		blocks_by_col = [[b for b in blocks_in_row if (b[0] >> 4) <= j and (b[1] >> 4) >= j] for j in range(i << 4, (i + 1) << 4)]
		blocks_by_col = [(b[0] if len(b) > 0 else None) for b in blocks_by_col]
		block_spans = []
		for b in blocks_by_col:
			if len(block_spans) > 0 and block_spans[-1][0] == b:
				block_spans[-1][1] += 1
			else:
				block_spans.append([b, 1])
		block_cells = []
		for b, colspan in block_spans:
			if b is None:
				block_cells.append('<td colspan="%s" class="block-undef">???</td>' % colspan)
			elif complete and 'Private Use Area' in b[2]:
				block_cells.append('<td colspan="%s"><a href="/charset/pua/">%s</a></td>' % (colspan, html_encode(b[2])))
			else:
				block_cells.append('<td colspan="%s"><a href="%s%04X">%s</a></td>' % (colspan, urlbase, b[0], html_encode(b[2])))
		print('<tr><th>%02X</th>%s</tr>' % (i, ''.join(block_cells)), file=f)
	print('</table>', file=f)

def build_dir(meta, ranges, chars, blocks, entities, basedir):
	blockdir = os.path.join(basedir, 'block')
	if not os.path.exists(blockdir):
		os.makedirs(blockdir)

	chardir = os.path.join(basedir, 'char')
	if not os.path.exists(chardir):
		os.makedirs(chardir)

	if meta is None:
		blockurlprefix = '/charset/unicode/block/'
		charurlprefix = '/charset/unicode/char/'
	else:
		htmlname = html_encode(meta['Agreement-Name'])
		urlname = re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name'])
		blockurlprefix = '/charset/pua/%s/block/' % urlname
		charurlprefix = '/charset/pua/%s/char/' % urlname

	for i in range(0, len(blocks)):
		block = blocks[i]
		prevblock = blocks[i - 1] if i - 1 >= 0 else None
		nextblock = blocks[i + 1] if i + 1 < len(blocks) else None
		dirpath = os.path.join(blockdir, '%04X' % block[0])
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		with open(os.path.join(dirpath, 'index.shtml'), 'w') as f:
			print('<!--#include virtual="/static/head.html"-->', file=f)
			if meta is None:
				print('<title>Character Encodings - Unicode - %s</title>' % html_encode(block[2]), file=f)
			else:
				print('<title>Character Encodings - Private Use Agreements - %s - %s</title>' % (htmlname, html_encode(block[2])), file=f)
			print('<link rel="stylesheet" href="/charset/shared/unicopy.css">', file=f)
			print('<link rel="stylesheet" href="/charset/shared/charlist.css">', file=f)
			print('<!--#include virtual="/static/body.html"-->', file=f)
			if meta is None:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/unicode/">Unicode</a> &raquo;</p>', file=f)
				print('<h1>%s</h1>' % html_encode(block[2]), file=f)
			else:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/pua/">Private Use Agreements</a> &raquo; <a href="/charset/pua/%s/">%s</a> &raquo;</p>' % (urlname, htmlname), file=f)
				print('<h1>%s</h1>' % html_encode(block[2]), file=f)
				print('<p class="pua-notice" data-pua-name="%s">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>' % htmlname, file=f)
			print('<table class="block-header"><tr>', file=f)
			if prevblock is None:
				print('<td class="block-prev-arr"></td><td class="block-prev"></td>', file=f)
			else:
				print('<td class="block-prev-arr"><a href="%s%04X">&larr;</a></td>' % (blockurlprefix, prevblock[0]), file=f)
				print('<td class="block-prev"><a href="%s%04X">%04X - %04X<br>%s</a></td>' % (blockurlprefix, prevblock[0], prevblock[0], prevblock[1], html_encode(prevblock[2])), file=f)
			print('<td class="block-curr">%04X - %04X<br>%s</td>' % (block[0], block[1], html_encode(block[2])), file=f)
			if nextblock is None:
				print('<td class="block-next"></td><td class="block-next-arr"></td>', file=f)
			else:
				print('<td class="block-next"><a href="%s%04X">%04X - %04X<br>%s</a></td>' % (blockurlprefix, nextblock[0], nextblock[0], nextblock[1], html_encode(nextblock[2])), file=f)
				print('<td class="block-next-arr"><a href="%s%04X">&rarr;</a></td>' % (blockurlprefix, nextblock[0]), file=f)
			print('</tr></table>', file=f)
			print('<table class="char-table">', file=f)
			print('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>', file=f)
			for j in range(block[0] >> 4, (block[1] >> 4) + 1):
				cells = [char_cell(k, ranges, chars, charurlprefix) for k in range(j << 4, (j + 1) << 4)]
				print('<tr><th>%02X</th>%s</tr>' % (j, ''.join(cells)), file=f)
			print('</table>', file=f)
			codepoints = sorted([cp for cp in chars if cp >= block[0] and cp <= block[1]])
			if len(codepoints) > 0:
				midpoint = (len(codepoints) + 1) >> 1
				print('<div class="charlist-outer-div">', file=f)
				print('<div class="charlist-inner-div">', file=f)
				print('<table class="charlist">', file=f)
				for cp in codepoints[:midpoint]:
					print(char_row(cp, chars[cp], charurlprefix), file=f)
				print('</table>', file=f)
				print('</div><div class="charlist-inner-div">', file=f)
				print('<table class="charlist">', file=f)
				for cp in codepoints[midpoint:]:
					print(char_row(cp, chars[cp], charurlprefix), file=f)
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

	with open(os.path.join(basedir, 'index.shtml'), 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		if meta is None:
			print('<title>Character Encodings - Unicode</title>', file=f)
		else:
			print('<title>Character Encodings - Private Use Agreements - %s</title>' % htmlname, file=f)
		print('<link rel="stylesheet" href="/charset/shared/blocklist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		if meta is None:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo;</p>', file=f)
			print('<h1>Unicode</h1>', file=f)
			print('<p>To find a Unicode character by name, use <a href="/charset/whereis/">Unicode Character Search</a>.</p>', file=f)
			print('<p>To list all the characters in a piece of text, use <a href="/charset/whatis/">Unicode String Decoder</a>.</p>', file=f)
		else:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/pua/">Private Use Agreements</a> &raquo;</p>', file=f)
			print('<h1>%s</h1>' % htmlname, file=f)
			print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
		last_plane = -1
		last_cp = -1
		for start, stop, blockname in blocks:
			plane = start >> 16
			if plane != last_plane:
				if last_plane >= 0:
					if meta is None and (last_cp & 0xFFFF) != 0:
						print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td class="block-undef">UNDEFINED</td></tr>' % (last_cp, last_cp | 0xFFFF), file=f)
					print('</table>', file=f)
					if meta is None:
						build_roadmap(True, blocks, last_plane, '/charset/unicode/block/', f)
					else:
						build_roadmap(False, blocks, last_plane, '/charset/pua/%s/block/' % urlname, f)
				print('<h2>%s</h2>' % html_encode(plane_name(plane)), file=f)
				print('<div class="hidden" id="block-list-switch-%s"><a href="#">List</a> - <b>Roadmap</b></div>' % plane, file=f)
				print('<div id="block-roadmap-switch-%s"><b>List</b> - <a href="#">Roadmap</a></div>' % plane, file=f)
				print('<table class="block-list" id="block-list-%s">' % plane, file=f)
				last_plane = plane
				last_cp = -1
			if meta is None:
				if start != last_cp and last_cp >= 0:
					print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td class="block-undef">UNDEFINED</td></tr>' % (last_cp, start - 1), file=f)
				if 'Private Use Area' in blockname:
					print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td><a href="/charset/pua/">%s</a></td></tr>' % (start, stop, html_encode(blockname)), file=f)
				else:
					print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td><a href="/charset/unicode/block/%04X">%s</a></td></tr>' % (start, stop, start, html_encode(blockname)), file=f)
			else:
				print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td><a href="/charset/pua/%s/block/%04X">%s</a></td></tr>' % (start, stop, urlname, start, html_encode(blockname)), file=f)
			last_cp = stop + 1
		if last_plane >= 0:
			if meta is None and (last_cp & 0xFFFF) != 0:
				print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td class="block-undef">UNDEFINED</td></tr>' % (last_cp, last_cp | 0xFFFF), file=f)
			print('</table>', file=f)
			if meta is None:
				build_roadmap(True, blocks, last_plane, '/charset/unicode/block/', f)
			else:
				build_roadmap(False, blocks, last_plane, '/charset/pua/%s/block/' % urlname, f)
		print('<script src="/charset/shared/jquery.js"></script>', file=f)
		print('<script src="/charset/shared/blocklist.js"></script>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

def main():
	ranges, chars, blocks = get_unidata()
	entities = get_entities()
	basedir = charset_path('out', 'unicode')
	build_dir(None, ranges, chars, blocks, entities, basedir)

	pua_meta = []
	for meta, chars, blocks in get_puadata():
		if 'Agreement-Type' in meta:
			if meta['Agreement-Type'] == 'Please-Ignore':
				continue
		basedir = charset_path('out', 'pua', re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name']))
		build_dir(meta, None, chars, blocks, entities, basedir)
		pua_meta.append(meta)
	pua_meta.sort(key=lambda meta: meta['Agreement-Name'])

	puadir = charset_path('out', 'pua')
	if not os.path.exists(puadir):
		os.makedirs(puadir)
	with open(os.path.join(puadir, 'index.shtml'), 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		print('<title>Character Encodings - Private Use Agreements</title>', file=f)
		print('<link rel="stylesheet" href="/charset/shared/blocklist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo;</p>', file=f)
		print('<h1>Private Use Agreements</h1>', file=f)
		print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
		print('<table class="pua-list">', file=f)
		for meta in pua_meta:
			print('<tr><td><a href="/charset/pua/%s">%s</a></td></tr>' % (re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name']), html_encode(meta['Agreement-Name'])), file=f)
		print('</table>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

if __name__ == '__main__':
	main()
