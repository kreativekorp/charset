#!/usr/bin/env python

from __future__ import print_function

import json
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from datalib import get_entities, get_font_data, get_psnames, get_puadata, get_unidata
from keyboardlib import keystroke_mac_us, keystroke_mac_us_ext, keystroke_superlatin
from parselib import charset_path
from unicodelib import bidi_class, char_to_utf8, char_to_utf16, combining_class, decomposition_tag, general_category, hex_dump, plane_name

def merge_blocks(*blockses):
	merged = [(0, 'UNDEFINED'), (0x110000, 'END')]
	def block_name(cp):
		for i in reversed(range(0, len(merged))):
			if cp >= merged[i][0]:
				return merged[i][1]
	def block_insert(cp, name):
		for i in reversed(range(0, len(merged))):
			if merged[i][0] == cp:
				merged[i] = (cp, name)
				return
			elif merged[i][0] < cp:
				merged.insert(i + 1, (cp, name))
				return
	def block_remove(a, b):
		for i in reversed(range(0, len(merged))):
			if merged[i][0] >= a and merged[i][0] <= b:
				merged.pop(i)
	for blocks in blockses:
		for block in blocks:
			block_insert(block[1]+1, block_name(block[1]+1))
			block_remove(block[0]+1, block[1])
			block_insert(block[0], block[2])
	return [(merged[i][0], merged[i+1][0]-1, merged[i][1]) for i in range(0, len(merged)-1)]

def html_encode(s):
	return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

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

def char_case_property(title, field, chars, url):
	try:
		cp = int(field, 16)
		if cp in chars:
			name = chars[cp][1]
			return '<tr><td>%s:</td><td colspan="2"><code>%04X</code> <a href="%s%04X">%s</a></td></tr>' % (title, cp, url, cp, html_encode(name))
		else:
			return '<tr><td>%s:</td><td colspan="2"><code>%04X</code></td></tr>' % (title, cp)
	except ValueError:
		return '<tr><td>%s:</td><td colspan="2"><code>%s</code></td></tr>' % (title, html_encode(field))

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

def build_dir(meta, ranges, chars, blocks, entities, psnames, fonts, basedir):
	blockdir = os.path.join(basedir, 'block')
	if not os.path.exists(blockdir):
		os.makedirs(blockdir)

	chardir = os.path.join(basedir, 'char')
	if not os.path.exists(chardir):
		os.makedirs(chardir)

	if meta is None:
		blockurlprefix = '/charset/unicode/block/'
		charurlprefix = '/charset/unicode/char/'
		isPUAA = False
	else:
		htmlname = html_encode(meta['Agreement-Name'])
		urlname = re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name'])
		if 'Agreement-Type' in meta and meta['Agreement-Type'] == 'Font-Internal':
			blockurlprefix = '/charset/font/%s/block/' % urlname
			charurlprefix = '/charset/font/%s/char/' % urlname
			puascript = '<script src="/charset/font/%s/pua.js"></script>' % urlname
			isPUAA = True
		else:
			blockurlprefix = '/charset/pua/%s/block/' % urlname
			charurlprefix = '/charset/pua/%s/char/' % urlname
			isPUAA = False

	for cp in chars:
		ch = chars[cp]
		prevcp = cp
		nextcp = cp
		prevch = None
		nextch = None
		while prevcp > 0 and prevch is None:
			prevcp -= 1
			if prevcp in chars:
				prevch = chars[prevcp]
		while nextcp < 0x110000 and nextch is None:
			nextcp += 1
			if nextcp in chars:
				nextch = chars[nextcp]
		blockstart = cp
		blockstop = cp
		blockname = '???'
		blockurl = re.sub('/block/', '/', blockurlprefix)
		for b in blocks:
			if cp >= b[0] and cp <= b[1]:
				blockstart, blockstop, blockname = b
				blockurl = '%s%04X' % (blockurlprefix, b[0])
				break
		charname = ch[10] if ch[1] == '<control>' and ch[10] != '' else ch[1]

		dirpath = os.path.join(chardir, '%04X' % cp)
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		path = os.path.join(dirpath, 'index.shtml')
		print('Writing char page: %s' % path)
		with open(path, 'w') as f:
			print('<!--#include virtual="/static/head.html"-->', file=f)
			if meta is None:
				print('<title>Character Encodings - Unicode - %s - %s</title>' % (html_encode(blockname), html_encode(charname)), file=f)
			elif isPUAA:
				print('<title>Character Encodings - Fonts - %s - %s - %s</title>' % (htmlname, html_encode(blockname), html_encode(charname)), file=f)
			else:
				print('<title>Character Encodings - Private Use Agreements - %s - %s - %s</title>' % (htmlname, html_encode(blockname), html_encode(charname)), file=f)
			print('<link rel="stylesheet" href="/charset/shared/character.css">', file=f)
			print('<!--#include virtual="/static/body.html"-->', file=f)
			if meta is None:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/unicode/">Unicode</a> &raquo; <a href="%s">%s</a> &raquo;</p>' % (html_encode(blockurl), html_encode(blockname)), file=f)
				print('<h1>%s</h1>' % html_encode(charname), file=f)
			elif isPUAA:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/font/">Fonts</a> &raquo; <a href="/charset/font/%s/">%s</a> &raquo; <a href="%s">%s</a> &raquo;</p>' % (urlname, htmlname, html_encode(blockurl), html_encode(blockname)), file=f)
				print('<h1>%s</h1>' % html_encode(charname), file=f)
				print('<p class="pua-notice">This is a private use character. Its use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretation shown here is only one of many possible interpretations.</p>', file=f)
			else:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/pua/">Private Use Agreements</a> &raquo; <a href="/charset/pua/%s/">%s</a> &raquo; <a href="%s">%s</a> &raquo;</p>' % (urlname, htmlname, html_encode(blockurl), html_encode(blockname)), file=f)
				print('<h1>%s</h1>' % html_encode(charname), file=f)
				print('<p class="pua-notice">This is a private use character. Its use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretation shown here is only one of many possible interpretations.</p>', file=f)
			print('<div class="char-data-outer-div">', file=f)
			print('<div class="char-data-inner-div" id="char-data-inner-div-1">', file=f)
			print('<h2>Properties</h2>', file=f)
			print('<table>', file=f)
			print('<tr><td>Character Name:</td><td colspan="2">%s</td></tr>' % html_encode(ch[1]), file=f)
			if len(ch) > 2:
				print('<tr><td>General Category:</td><td><code>%s</code></td><td>%s</td></tr>' % (ch[2], general_category[ch[2]] if ch[2] in general_category else ''), file=f)
			if len(ch) > 3:
				print('<tr><td>Combining Class:</td><td><code>%s</code></td><td>%s</td></tr>' % (ch[3], combining_class[ch[3]] if ch[3] in combining_class else ''), file=f)
			if len(ch) > 4:
				print('<tr><td>Bidi Class:</td><td><code>%s</code></td><td>%s</td></tr>' % (ch[4], bidi_class[ch[4]] if ch[4] in bidi_class else ''), file=f)
			if len(ch) > 5 and len(ch[5]) > 0:
				tokens = []
				for token in ch[5].split(' '):
					if token[0] == '<' and token[-1] == '>':
						if token[1:-1] in decomposition_tag:
							tokens.append('<span title="%s">%s</span>' % (html_encode(decomposition_tag[token[1:-1]]), html_encode(token)))
						else:
							tokens.append(html_encode(token))
					else:
						try:
							dcp = int(token, 16)
							tokens.append('<a href="/charset/unicode/char/%04X">%04X</a>' % (dcp, dcp))
						except ValueError:
							tokens.append(html_encode(token))
				print('<tr><td>Decomposition:</td><td colspan="2"><code>%s</code></td></tr>' % ' '.join(tokens), file=f)
			if len(ch) > 8 and len(ch[8]) > 0:
				print('<tr><td>Numeric Value:</td><td colspan="2">%s</td></tr>' % html_encode(ch[8]), file=f)
			if len(ch) > 9:
				print('<tr><td>Bidi Mirrored:</td><td colspan="2">%s</td></tr>' % html_encode(ch[9]), file=f)
			if len(ch) > 10 and len(ch[10]) > 0:
				print('<tr><td>Unicode 1.0 Name:</td><td colspan="2">%s</td></tr>' % html_encode(ch[10]), file=f)
			if len(ch) > 11 and len(ch[11]) > 0:
				print('<tr><td>ISO Comment:</td><td colspan="2">%s</td></tr>' % html_encode(ch[11]), file=f)
			if len(ch) > 12 and len(ch[12]) > 0:
				print(char_case_property('Uppercase', ch[12], chars, charurlprefix), file=f)
			if len(ch) > 13 and len(ch[13]) > 0:
				print(char_case_property('Lowercase', ch[13], chars, charurlprefix), file=f)
			if len(ch) > 14 and len(ch[14]) > 0:
				print(char_case_property('Titlecase', ch[14], chars, charurlprefix), file=f)
			print('</table>', file=f)
			print('<h2>How to Type</h2>', file=f)
			print('<table>', file=f)
			print('<tr><td>Windows:</td><td>Alt+0%s</td></tr>' % cp, file=f)
			if cp in keystroke_superlatin:
				print('<tr><td>Windows, <a href="http://www.kreativekorp.com/software/keyboards/superlatin/" target="_blank">SuperLatin</a>:</td><td>%s</td></tr>' % html_encode(keystroke_superlatin[cp].replace('Shift-', 'Shift+').replace('Ctrl-', 'Ctrl+').replace('Alt-', 'AltGr+')), file=f)
			if cp in keystroke_mac_us:
				print('<tr><td>Mac, U.S.:</td><td>%s</td></tr>' % html_encode(keystroke_mac_us[cp]), file=f)
			if cp in keystroke_mac_us_ext:
				print('<tr><td>Mac, U.S. Extended:</td><td>%s</td></tr>' % html_encode(keystroke_mac_us_ext[cp]), file=f)
			if cp in keystroke_superlatin:
				print('<tr><td>Mac, <a href="http://www.kreativekorp.com/software/keyboards/superlatin/" target="_blank">SuperLatin</a>:</td><td>%s</td></tr>' % html_encode(keystroke_superlatin[cp].replace('Alt-', 'Option-')), file=f)
			if cp < 0x10000:
				print('<tr><td>Mac, Unicode Hex:</td><td>Option-%04X</td></tr>' % cp, file=f)
			elif cp < 0x110000:
				print('<tr><td>Mac, Unicode Hex:</td><td>Option-%04X-%04X</td></tr>' % (0xD800 | ((cp - 0x10000) >> 10), 0xDC00 | ((cp - 0x10000) & 0x3FF)), file=f)
			print('</table>', file=f)
			print('</div><div class="char-data-inner-div" id="char-data-inner-div-2">', file=f)
			print('<h2>Encoding</h2>', file=f)
			print('<table>', file=f)
			print('<tr><td>Decimal:</td><td>%s</td></tr>' % cp, file=f)
			print('<tr><td>Hexadecimal:</td><td>U+%04X</td></tr>' % cp, file=f)
			if cp in psnames:
				print('<tr><td>PostScript Name:</td><td>%s</td></tr>' % html_encode(psnames[cp]), file=f)
			elif cp < 0x10000:
				print('<tr><td>PostScript Name:</td><td>uni%04X</td></tr>' % cp, file=f)
			else:
				print('<tr><td>PostScript Name:</td><td>u%05X</td></tr>' % cp, file=f)
			if cp in entities:
				print('<tr><td>HTML Name:</td><td><code>%s</code></td></tr>' % html_encode(entities[cp]), file=f)
			print('<tr><td>HTML Dec:</td><td><code>&amp;#%s;</code></td></tr>' % cp, file=f)
			print('<tr><td>HTML Hex:</td><td><code>&amp;#x%X;</code></td></tr>' % cp, file=f)
			chu8 = char_to_utf8(cp)
			chu16 = char_to_utf16(cp)
			print('<tr><td>URL:</td><td><code>%s</code></td></tr>' % ''.join('%%%02X' % b for b in chu8), file=f)
			print('<tr><td>C/C++:</td><td><code>%s</code></td></tr>' % ''.join('\\x%02X' % b for b in chu8), file=f)
			print('<tr><td>Java:</td><td><code>%s</code></td></tr>' % ''.join('\\u%04X' % w for w in chu16), file=f)
			print('<tr><td>Python:</td><td><code>u\'%s\'</code></td></tr>' % ('\\u%04X' % cp if cp < 0x10000 else '\\U%08X' % cp), file=f)
			print('<tr><td>UTF-8:</td><td><code>%s</code></td></tr>' % hex_dump(chu8, 2), file=f)
			print('<tr><td>UTF-16BE:</td><td><code>%s</code></td></tr>' % hex_dump(chu16, 4, False), file=f)
			print('<tr><td>UTF-16LE:</td><td><code>%s</code></td></tr>' % hex_dump(chu16, 4, True), file=f)
			print('<tr><td>UTF-32BE:</td><td><code>%s</code></td></tr>' % hex_dump([cp], 8, False), file=f)
			print('<tr><td>UTF-32LE:</td><td><code>%s</code></td></tr>' % hex_dump([cp], 8, True), file=f)
			print('</table>', file=f)
			print('</div>', file=f)
			if (cp > 0x20 and cp < 0x7F) or (cp > 0xA0 and cp < 0xD800) or (cp >= 0xE000 and cp < 0xFDD0) or (cp >= 0xFDF0 and cp < 0xFFFE) or (cp >= 0x10000 and cp < 0x110000 and (cp & 0xFFFF) < 0xFFFE):
				print('<h2>Appearance</h2>', file=f)
				print('<div class="char-glyph-panel"><!--', file=f)
				for font_data in fonts:
					if font_data[1].get(cp):
						font_name = html_encode(font_data[0])
						font_url = html_encode('/charset/font/%s' % re.sub('[^A-Za-z0-9]+', '', font_data[0]))
						print('--><div class="char-glyph-item" data-font-name="%s"><div class="char-glyph" style="font-family: \'%s\', \'Adobe Blank\';">&#%s;</div><div class="char-glyph-font"><a href="%s">%s</a></div></div><!--' % (font_name, font_name, cp, font_url, font_name), file=f)
				print('--></div>', file=f)
			print('<script src="/charset/shared/jquery.js"></script>', file=f)
			print('<script src="/charset/shared/character.js"></script>', file=f)
			print('<!--#include virtual="/static/tail.html"-->', file=f)

	for i in range(0, len(blocks)):
		block = blocks[i]
		prevblock = blocks[i - 1] if i - 1 >= 0 else None
		nextblock = blocks[i + 1] if i + 1 < len(blocks) else None
		dirpath = os.path.join(blockdir, '%04X' % block[0])
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		path = os.path.join(dirpath, 'index.shtml')
		print('Writing block page: %s' % path)
		with open(path, 'w') as f:
			print('<!--#include virtual="/static/head.html"-->', file=f)
			if meta is None:
				print('<title>Character Encodings - Unicode - %s</title>' % html_encode(block[2]), file=f)
			elif isPUAA:
				print('<title>Character Encodings - Fonts - %s - %s</title>' % (htmlname, html_encode(block[2])), file=f)
			else:
				print('<title>Character Encodings - Private Use Agreements - %s - %s</title>' % (htmlname, html_encode(block[2])), file=f)
			print('<link rel="stylesheet" href="/charset/shared/unicopy.css">', file=f)
			print('<link rel="stylesheet" href="/charset/shared/charlist.css">', file=f)
			if isPUAA:
				print('<style>.char-table td, .charlist-charglyph, .unicopy-h1 { font-family: "%s"; }</style>' % meta['Agreement-Name'], file=f)
			print('<!--#include virtual="/static/body.html"-->', file=f)
			if meta is None:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/unicode/">Unicode</a> &raquo;</p>', file=f)
				print('<h1>%s</h1>' % html_encode(block[2]), file=f)
			elif isPUAA:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/font/">Fonts</a> &raquo; <a href="/charset/font/%s/">%s</a> &raquo;</p>' % (urlname, htmlname), file=f)
				print('<h1>%s</h1>' % html_encode(block[2]), file=f)
				print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
			else:
				print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/pua/">Private Use Agreements</a> &raquo; <a href="/charset/pua/%s/">%s</a> &raquo;</p>' % (urlname, htmlname), file=f)
				print('<h1>%s</h1>' % html_encode(block[2]), file=f)
				print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
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
			if not isPUAA:
				print('<table class="block-subheader"><tr>', file=f)
				print('<td class="block-fonts">Font: <select id="font-selector">', file=f)
				print('<option selected value="inherit">Default</option>', file=f)
				for font_data in fonts:
					if font_data[1].getAny(block[0], block[1]):
						font_name = html_encode(font_data[0])
						print('<option value="%s">%s</option>' % (font_name, font_name), file=f)
				print('</select></td>', file=f)
				if meta is None:
					print('<td class="block-links"><a href="http://www.unicode.org/charts/PDF/U%04X.pdf" target="_blank">Code Chart PDF</a></td>' % block[0], file=f)
				else:
					print('<td class="block-links"></td>', file=f)
				print('</tr></table>', file=f)
			if meta is None:
				print('<table class="char-table">', file=f)
			else:
				print('<table class="char-table" data-pua-name="%s">' % htmlname, file=f)
			print('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>', file=f)
			for j in range(block[0] >> 4, (block[1] >> 4) + 1):
				cells = [char_cell(k, ranges, chars, charurlprefix) for k in range(j << 4, (j + 1) << 4)]
				print('<tr><th>%03X</th>%s</tr>' % (j, ''.join(cells)), file=f)
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
			print(puascript if isPUAA else '<script src="/charset/shared/pua.js"></script>', file=f)
			print('<script src="/charset/shared/entitydb.js"></script>', file=f)
			print('<script src="/charset/shared/psnamedb.js"></script>', file=f)
			print('<script src="/charset/shared/unicopy.js"></script>', file=f)
			print('<script src="/charset/shared/charlist.js"></script>', file=f)
			print('<!--#include virtual="/static/tail.html"-->', file=f)

	path = os.path.join(blockdir if isPUAA else basedir, 'index.shtml')
	print('Writing block index: %s' % path)
	with open(path, 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		if meta is None:
			print('<title>Character Encodings - Unicode</title>', file=f)
		elif isPUAA:
			print('<title>Character Encodings - Fonts - %s</title>' % htmlname, file=f)
		else:
			print('<title>Character Encodings - Private Use Agreements - %s</title>' % htmlname, file=f)
		print('<link rel="stylesheet" href="/charset/shared/blocklist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		if meta is None:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo;</p>', file=f)
			print('<h1>Unicode</h1>', file=f)
			print('<p>To find a Unicode character by name, use <a href="/charset/whereis/">Unicode Character Search</a>.</p>', file=f)
			print('<p>To list all the characters in a piece of text, use <a href="/charset/whatis/">Unicode String Decoder</a>.</p>', file=f)
		elif isPUAA:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/font/">Fonts</a> &raquo;</p>', file=f)
			print('<h1>%s</h1>' % htmlname, file=f)
			print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
			if 'Agreement-URL' in meta and meta['Agreement-URL']:
				print('<p><a href="%s" target="_blank">%s Home Page</a><br>' % (html_encode(meta['Agreement-URL']), htmlname), file=f)
				print('<a href="/charset/font/%s/">Character Repertoire Index</a></p>' % urlname, file=f)
			else:
				print('<p><a href="/charset/font/%s/">Character Repertoire Index</a></p>' % urlname, file=f)
		else:
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/pua/">Private Use Agreements</a> &raquo;</p>', file=f)
			print('<h1>%s</h1>' % htmlname, file=f)
			print('<p class="pua-notice">These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.</p>', file=f)
			if 'Agreement-URL' in meta and meta['Agreement-URL']:
				print('<p><a href="%s" target="_blank">%s Home Page</a></p>' % (html_encode(meta['Agreement-URL']), htmlname), file=f)
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
					elif isPUAA:
						build_roadmap(False, blocks, last_plane, '/charset/font/%s/block/' % urlname, f)
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
			elif isPUAA:
				print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td><a href="/charset/font/%s/block/%04X">%s</a></td></tr>' % (start, stop, urlname, start, html_encode(blockname)), file=f)
			else:
				print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td><a href="/charset/pua/%s/block/%04X">%s</a></td></tr>' % (start, stop, urlname, start, html_encode(blockname)), file=f)
			last_cp = stop + 1
		if last_plane >= 0:
			if meta is None and (last_cp & 0xFFFF) != 0:
				print('<tr><td class="block-cp">%04X</td><td class="block-cp">%04X</td><td class="block-undef">UNDEFINED</td></tr>' % (last_cp, last_cp | 0xFFFF), file=f)
			print('</table>', file=f)
			if meta is None:
				build_roadmap(True, blocks, last_plane, '/charset/unicode/block/', f)
			elif isPUAA:
				build_roadmap(False, blocks, last_plane, '/charset/font/%s/block/' % urlname, f)
			else:
				build_roadmap(False, blocks, last_plane, '/charset/pua/%s/block/' % urlname, f)
		print('<script src="/charset/shared/jquery.js"></script>', file=f)
		print('<script src="/charset/shared/blocklist.js"></script>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

def redirect_dir(urlprefix, chars, blocks, basedir):
	blockdir = os.path.join(basedir, 'block')
	if not os.path.exists(blockdir):
		os.makedirs(blockdir)

	chardir = os.path.join(basedir, 'char')
	if not os.path.exists(chardir):
		os.makedirs(chardir)

	blockurlprefix = urlprefix + 'block/' if urlprefix[-1] == '/' else urlprefix + '/block/'
	charurlprefix = urlprefix + 'char/' if urlprefix[-1] == '/' else urlprefix + '/char/'

	for cp in chars:
		dirpath = os.path.join(chardir, '%04X' % cp)
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		path = os.path.join(dirpath, 'index.php')
		print('Writing char page redirect: %s' % path)
		with open(path, 'w') as f:
			print('<?php header(\'Location: %s%04X\');' % (charurlprefix, cp), file=f)

	for block in blocks:
		dirpath = os.path.join(blockdir, '%04X' % block[0])
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		path = os.path.join(dirpath, 'index.php')
		print('Writing block page redirect: %s' % path)
		with open(path, 'w') as f:
			print('<?php header(\'Location: %s%04X\');' % (blockurlprefix, block[0]), file=f)

	path = os.path.join(chardir, 'index.php')
	print('Writing char index redirect: %s' % path)
	with open(path, 'w') as f:
		print('<?php header(\'Location: %s\');' % charurlprefix, file=f)

	path = os.path.join(blockdir, 'index.php')
	print('Writing block index redirect: %s' % path)
	with open(path, 'w') as f:
		print('<?php header(\'Location: %s\');' % blockurlprefix, file=f)

	path = os.path.join(basedir, 'index.php')
	print('Writing index redirect: %s' % path)
	with open(path, 'w') as f:
		print('<?php header(\'Location: %s\');' % urlprefix, file=f)

def main():
	pua_to_font_redirects = [
		# FCC --- PUA Name -------- Font Name ------ Ch, Bk
		['Alco', 'Alco',           'AlcoSans',       {}, []],
		['Cons', 'Constructium',   'Constructium',   {}, []],
		['Fair', 'Fairfax',        'Fairfax',        {}, []],
		['FfHD', 'FairfaxHD',      'FairfaxHD',      {}, []],
		['KSqu', 'KreativeSquare', 'KreativeSquare', {}, []],
	]

	ranges, chars, blocks = get_unidata()
	entities = get_entities()
	psnames = get_psnames()
	fonts = get_font_data()
	basedir = charset_path('out', 'unicode')
	build_dir(None, ranges, chars, blocks, entities, psnames, fonts, basedir)

	pua_meta = []
	pua_chars = {}
	pua_blocks = {}
	for meta, pchars, pblocks in get_puadata():
		if 'Agreement-Type' in meta:
			if meta['Agreement-Type'] == 'Please-Ignore':
				continue
		basedir = charset_path('out', 'pua', re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name']))
		build_dir(meta, None, pchars, pblocks, entities, psnames, fonts, basedir)
		pua_meta.append(meta)
		pua_chars[meta['Agreement-Name']] = pchars
		pua_blocks[meta['Agreement-Name']] = pblocks
	pua_meta.sort(key=lambda meta: meta['Agreement-Name'])

	puadir = charset_path('out', 'pua')
	if not os.path.exists(puadir):
		os.makedirs(puadir)
	path = os.path.join(puadir, 'index.shtml')
	print('Writing Private Use Area index: %s' % path)
	with open(path, 'w') as f:
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
		pua_fonts = [font for font in fonts if (font[3] and 'Blocks' in font[3] and 'UnicodeData' in font[3] and font[3]['Blocks'] and font[3]['UnicodeData'])]
		if pua_fonts:
			print('<h2>Fonts with Private Use Area Attributes</h2>', file=f)
			print('<table class="pua-list">', file=f)
			for font in pua_fonts:
				print('<tr><td><a href="/charset/font/%s">%s</a></td></tr>' % (re.sub('[^A-Za-z0-9]+', '', font[0]), html_encode(font[0])), file=f)
			print('</table>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

	fontblocks = {font[0]: [] for font in fonts}
	fontdir = charset_path('out', 'font')
	if not os.path.exists(fontdir):
		os.makedirs(fontdir)
	for font in fonts:
		urlname = re.sub('[^A-Za-z0-9]+', '', font[0])
		fdir = os.path.join(fontdir, urlname)
		if not os.path.exists(fdir):
			os.makedirs(fdir)
		hasPUAA = (font[3] and 'Blocks' in font[3] and 'UnicodeData' in font[3] and font[3]['Blocks'] and font[3]['UnicodeData'])
		if hasPUAA:
			for i in range(0, len(pua_to_font_redirects)):
				if pua_to_font_redirects[i][2] == urlname:
					pua_to_font_redirects[i][3] = font[3]['UnicodeData']
					pua_to_font_redirects[i][4] = font[3]['Blocks']
			puascript = '<script src="/charset/font/%s/pua.js"></script>' % urlname
			meta = {'Agreement-Name': font[0], 'Agreement-Type': 'Font-Internal'}
			if font[4]:
				meta['Agreement-URL'] = font[4]
			build_dir(meta, None, font[3]['UnicodeData'], font[3]['Blocks'], entities, psnames, fonts, fdir)
			meta['chars'] = font[3]['UnicodeData']
			meta['blocks'] = font[3]['Blocks']
			path = os.path.join(fdir, 'pua.js')
			print('Writing Private Use Area data: %s' % path)
			with open(path, 'w') as f:
				f.write('PUA=%s;' % json.dumps({font[0]: meta}, separators=(',', ':')))
		path = os.path.join(fdir, 'index.shtml')
		print('Writing font page: %s' % path)
		with open(path, 'w') as f:
			print('<!--#include virtual="/static/head.html"-->', file=f)
			print('<title>Character Encodings - Fonts - %s</title>' % html_encode(font[0]), file=f)
			print('<link rel="stylesheet" href="/charset/shared/unicopy.css">', file=f)
			print('<link rel="stylesheet" href="/charset/shared/charlist.css">', file=f)
			print('<style>.char-table td, .charlist-charglyph, .unicopy-h1 { font-family: "%s"; }</style>' % font[0], file=f)
			print('<!--#include virtual="/static/body.html"-->', file=f)
			print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo; <a href="/charset/font/">Fonts</a> &raquo;</p>', file=f)
			print('<h1>%s</h1>' % html_encode(font[0]), file=f)
			if font[4] and hasPUAA:
				print('<p><a href="%s" target="_blank">%s Home Page</a><br>' % (html_encode(font[4]), html_encode(font[0])), file=f)
				print('<a href="/charset/font/%s/block/">Private Use Area Block Index</a></p>' % urlname, file=f)
			elif font[4]:
				print('<p><a href="%s" target="_blank">%s Home Page</a></p>' % (html_encode(font[4]), html_encode(font[0])), file=f)
			elif hasPUAA:
				print('<p><a href="/charset/font/%s/block/">Private Use Area Block Index</a></p>' % urlname, file=f)
			blockses = []
			charses = []
			blockurls = []
			charurls = []
			agreements = []
			if hasPUAA:
				blockses.append(font[3]['Blocks'])
				charses.append(font[3]['UnicodeData'])
				blockurls.append('/charset/font/%s/block/' % urlname)
				charurls.append('/charset/font/%s/char/' % urlname)
				agreements.append(font[0])
			else:
				for vendor_agreement in [meta['Agreement-Name'] for meta in pua_meta if font[2] in meta['Vendor-IDs']]:
					blockses.append(pua_blocks[vendor_agreement])
					charses.append(pua_chars[vendor_agreement])
					blockurls.append('/charset/pua/%s/block/' % re.sub('[^A-Za-z0-9]+', '', vendor_agreement))
					charurls.append('/charset/pua/%s/char/' % re.sub('[^A-Za-z0-9]+', '', vendor_agreement))
					agreements.append(vendor_agreement)
				for font_agreement in [meta['Agreement-Name'] for meta in pua_meta if font[0] in meta['Font-Names']]:
					blockses.append(pua_blocks[font_agreement])
					charses.append(pua_chars[font_agreement])
					blockurls.append('/charset/pua/%s/block/' % re.sub('[^A-Za-z0-9]+', '', font_agreement))
					charurls.append('/charset/pua/%s/char/' % re.sub('[^A-Za-z0-9]+', '', font_agreement))
					agreements.append(font_agreement)
			if agreements:
				print('<table class="char-table" data-pua-name="%s">' % html_encode(','.join(reversed(agreements))), file=f)
			else:
				print('<table class="char-table">', file=f)
			font_blocks = merge_blocks(blocks, *blockses)
			for block in font_blocks:
				pc = font[1].popcountBetween(block[0], block[1])
				if pc > 0:
					fontblocks[font[0]].append((block[2], pc))
					if block[2] == 'UNDEFINED':
						print('<tr><th class="char-table-block-name" colspan="17">%s (%s)</th></tr>' % (block[2], pc), file=f)
					elif 'Private Use Area' in block[2]:
						pua_tag = '<div class="char-table-tag" title="These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.">PUA</div>'
						print('<tr><th class="char-table-block-name" colspan="17">%s<a href="/charset/pua/">%s</a> (%s)</th></tr>' % (pua_tag, block[2], pc), file=f)
					else:
						blockurl = '/charset/unicode/block/'
						pua_name = None
						for i in range(0, len(blockses)):
							if block in blockses[i]:
								blockurl = blockurls[i]
								pua_name = agreements[i]
						if pua_name is not None:
							pua_tag = '<div class="char-table-tag" title="These are private use characters. Their use and interpretation is not specified by the Unicode Standard but may be determined by private agreement among cooperating users. The interpretations shown here are only some of many possible interpretations.\n\nThis interpretation: %s">PUA</div>' % html_encode(pua_name)
							print('<tr><th class="char-table-block-name" colspan="17">%s<a href="%s%04X">%s</a> (%s)</th></tr>' % (pua_tag, blockurl, block[0], block[2], pc), file=f)
						else:
							print('<tr><th class="char-table-block-name" colspan="17"><a href="%s%04X">%s</a> (%s)</th></tr>' % (blockurl, block[0], block[2], pc), file=f)
					print('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>', file=f)
					skipped = False
					for j in range(block[0] >> 4, (block[1] >> 4) + 1):
						if not font[1].getAny((j << 4), (j << 4) | 0xF):
							if not skipped:
								print('<tr><td class="char-table-row-skip" colspan="17"></td></tr>', file=f)
								skipped = True
						else:
							cells = []
							for k in range(j << 4, (j + 1) << 4):
								cellchars = chars
								cellurl = '/charset/unicode/char/'
								for l in range(0, len(charses)):
									if k in charses[l]:
										cellchars = charses[l]
										cellurl = charurls[l]
								if font[1].get(k):
									cell = char_cell(k, ranges, cellchars, cellurl)
								else:
									cell = '<td class="char-not-in-font"><div class="char-empty"></div></td>'
								cells.append(cell)
							print('<tr><th>%03X</th>%s</tr>' % (j, ''.join(cells)), file=f)
							skipped = False
			print('</table>', file=f)
			print('<script src="/charset/shared/jquery.js"></script>', file=f)
			print('<script src="/charset/shared/ucd.js"></script>', file=f)
			print(puascript if hasPUAA else '<script src="/charset/shared/pua.js"></script>', file=f)
			print('<script src="/charset/shared/entitydb.js"></script>', file=f)
			print('<script src="/charset/shared/psnamedb.js"></script>', file=f)
			print('<script src="/charset/shared/unicopy.js"></script>', file=f)
			print('<script src="/charset/shared/charlist.js"></script>', file=f)
			print('<!--#include virtual="/static/tail.html"-->', file=f)

	path = os.path.join(fontdir, 'index.shtml')
	print('Writing font index: %s' % path)
	with open(path, 'w') as f:
		print('<!--#include virtual="/static/head.html"-->', file=f)
		print('<title>Character Encodings - Fonts</title>', file=f)
		print('<link rel="stylesheet" href="/charset/shared/fontlist.css">', file=f)
		print('<!--#include virtual="/static/body.html"-->', file=f)
		print('<p class="breadcrumb"><a href="/charset/">Character Encodings</a> &raquo;</p>', file=f)
		print('<h1>Fonts</h1>', file=f)
		print('<p class="font-options">', file=f)
		print('Filter: <input type="text" name="q" class="font-filter-input" style="width: 300px;">', file=f)
		print('Order By: <label><input type="radio" name="s" value="n" checked>Name</label>', file=f)
		print('<label><input type="radio" name="s" value="c">Coverage</label>', file=f)
		print('</p>', file=f)
		print('<div class="font-list">', file=f)
		for font in fonts:
			fontname = html_encode(font[0])
			fonturl = html_encode('/charset/font/%s' % re.sub('[^A-Za-z0-9]+', '', font[0]))
			fontblockstring = html_encode(', '.join('%s (%s)' % (b[0], b[1]) for b in fontblocks[font[0]]))
			print('<div class="font-item" data-font-name="%s">' % fontname, file=f)
			print('<div class="font-header">', file=f)
			print('<span class="font-link"><a href="%s">%s</a></span>' % (fonturl, fontname), file=f)
			print('<span class="font-ccount"><span class="label">Chars: </span><span class="value">%s</span></span>' % font[1].popcount(), file=f)
			print('<span class="font-bcount"><a href="%s"><span class="label">Blocks: </span><span class="value">%s</span></a></span>' % (fonturl, len(fontblocks[font[0]])), file=f)
			print('<span class="font-pswitch"><a href="%s">Preview</a></span>' % fonturl, file=f)
			print('</div>', file=f)
			print('<div class="font-blocks hidden">%s</div>' % fontblockstring, file=f)
			print('<div class="font-preview hidden" style="font-family: \'%s\', \'Adobe Blank\';">How razorback-jumping frogs can level six piqued gymnasts!</div>' % fontname, file=f);
			print('</div>', file=f)
		print('</div>', file=f)
		print('<script src="/charset/shared/jquery.js"></script>', file=f)
		print('<script src="/charset/shared/fontlist.js"></script>', file=f)
		print('<!--#include virtual="/static/tail.html"-->', file=f)

	for meta in pua_to_font_redirects:
		redirect_dir('/charset/font/%s' % meta[2], meta[3], meta[4], charset_path('out', 'pua', meta[1]))

	path = charset_path('out', 'unicode.php')
	print('Writing unicode redirect: %s' % path)
	with open(path, 'w') as f:
		print('<?php', file=f)
		print('if (isset($_GET[\'pua\'])) {', file=f)
		print('\t$pua = $_GET[\'pua\'];', file=f)
		print('\tswitch ($pua) {', file=f)
		for meta in pua_meta:
			if 'Agreement-FCC' in meta:
				urlname = html_encode(re.sub('[^A-Za-z0-9]+', '', meta['Agreement-Name']))
				print('\t\tcase \'%s\':' % meta['Agreement-FCC'], file=f)
				print('\t\t\tif (isset($_GET[\'char\'])) {', file=f)
				print('\t\t\t\t$ch = strtoupper(dechex(hexdec($_GET[\'char\'])));', file=f)
				print('\t\t\t\twhile (strlen($ch) < 4) { $ch = \'0\' . $ch; }', file=f)
				print('\t\t\t\tif (file_exists(\'pua/%s/char/\' . $ch)) {' % urlname, file=f)
				print('\t\t\t\t\theader(\'Location: /charset/pua/%s/char/\' . $ch);' % urlname, file=f)
				print('\t\t\t\t\texit(0);', file=f)
				print('\t\t\t\t}', file=f)
				print('\t\t\t}', file=f)
				print('\t\t\tif (isset($_GET[\'block\'])) {', file=f)
				print('\t\t\t\t$ch = hexdec($_GET[\'block\']);', file=f)
				for block in pua_blocks[meta['Agreement-Name']]:
					print('\t\t\t\tif ($ch >= %s && $ch <= %s && file_exists(\'pua/%s/block/%04X\')) {' % (block[0], block[1], urlname, block[0]), file=f)
					print('\t\t\t\t\theader(\'Location: /charset/pua/%s/block/%04X\');' % (urlname, block[0]), file=f)
					print('\t\t\t\t\texit(0);', file=f)
					print('\t\t\t\t}', file=f)
				print('\t\t\t}', file=f)
				print('\t\t\theader(\'Location: /charset/pua/%s\');' % urlname, file=f)
				print('\t\t\texit(0);', file=f)
		for meta in pua_to_font_redirects:
			print('\t\tcase \'%s\':' % meta[0], file=f)
			print('\t\t\tif (isset($_GET[\'char\'])) {', file=f)
			print('\t\t\t\t$ch = strtoupper(dechex(hexdec($_GET[\'char\'])));', file=f)
			print('\t\t\t\twhile (strlen($ch) < 4) { $ch = \'0\' . $ch; }', file=f)
			print('\t\t\t\tif (file_exists(\'font/%s/char/\' . $ch)) {' % meta[2], file=f)
			print('\t\t\t\t\theader(\'Location: /charset/font/%s/char/\' . $ch);' % meta[2], file=f)
			print('\t\t\t\t\texit(0);', file=f)
			print('\t\t\t\t}', file=f)
			print('\t\t\t}', file=f)
			print('\t\t\tif (isset($_GET[\'block\'])) {', file=f)
			print('\t\t\t\t$ch = hexdec($_GET[\'block\']);', file=f)
			for block in meta[4]:
				print('\t\t\t\tif ($ch >= %s && $ch <= %s && file_exists(\'font/%s/block/%04X\')) {' % (block[0], block[1], meta[2], block[0]), file=f)
				print('\t\t\t\t\theader(\'Location: /charset/font/%s/block/%04X\');' % (meta[2], block[0]), file=f)
				print('\t\t\t\t\texit(0);', file=f)
				print('\t\t\t\t}', file=f)
			print('\t\t\t}', file=f)
			print('\t\t\theader(\'Location: /charset/font/%s\');' % meta[2], file=f)
			print('\t\t\texit(0);', file=f)
		print('\t}', file=f)
		print('\theader(\'Location: /charset/pua/\');', file=f)
		print('\texit(0);', file=f)
		print('}', file=f)
		print('if (isset($_GET[\'char\'])) {', file=f)
		print('\t$ch = strtoupper(dechex(hexdec($_GET[\'char\'])));', file=f)
		print('\twhile (strlen($ch) < 4) { $ch = \'0\' . $ch; }', file=f)
		print('\tif (file_exists(\'unicode/char/\' . $ch)) {', file=f)
		print('\t\theader(\'Location: /charset/unicode/char/\' . $ch);', file=f)
		print('\t\texit(0);', file=f)
		print('\t}', file=f)
		print('}', file=f)
		print('if (isset($_GET[\'block\'])) {', file=f)
		print('\t$ch = hexdec($_GET[\'block\']);', file=f)
		for block in blocks:
			print('\tif ($ch >= %s && $ch <= %s && file_exists(\'unicode/block/%04X\')) {' % (block[0], block[1], block[0]), file=f)
			print('\t\theader(\'Location: /charset/unicode/block/%04X\');' % block[0], file=f)
			print('\t\texit(0);', file=f)
			print('\t}', file=f)
		print('}', file=f)
		print('header(\'Location: /charset/unicode/\');', file=f)

if __name__ == '__main__':
	main()
