#!/usr/bin/env python3

import re
import unicodedata

def html_encode(s):
	return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&#34;').replace("'",'&#39;')

def page_head(title, styles):
	lines = []
	lines.append('<!--#include virtual="/static/head.html"-->')
	lines.append('<title>%s</title>' % html_encode(title))
	lines.extend('<link rel="stylesheet" href="/charset/shared/%s.css">' % html_encode(style) for style in styles)
	lines.append('<!--#include virtual="/static/body.html"-->')
	return '\n'.join(lines)

def page_tail(scripts):
	lines = []
	lines.extend('<script src="/charset/shared/%s.js"></script>' % html_encode(script) for script in scripts)
	lines.append('<!--#include virtual="/static/tail.html"-->')
	return '\n'.join(lines)

def breadcrumb(id, *links):
	ia = ' id="%s"' % html_encode(id) if id else ''
	pc = ' '.join('<a href="%s">%s</a> &raquo;' % tuple(html_encode(s) for s in link) for link in links)
	return '<p%s class="breadcrumb">%s</p>' % (ia, pc)

def create_redirect(php_file, url):
	with open(php_file, 'w') as f:
		f.write("<?php header('Location: %s');" % url.replace('\\', '\\\\').replace("'", "\\'"))

def is_control(cp):
	return 0x00 <= cp <= 0x1F or 0x7F <= cp <= 0x9F

def is_high_surrogate(cp):
	return 0xD800 <= cp <= 0xDBFF

def is_low_surrogate(cp):
	return 0xDC00 <= cp <= 0xDFFF

def is_surrogate(cp):
	return 0xD800 <= cp <= 0xDFFF

def is_private(cp):
	return 0xE000 <= cp <= 0xF8FF or cp >= 0xF0000

def is_nonchar(cp):
	return 0xFDD0 <= cp <= 0xFDEF or (cp & 0xFFFF) >= 0xFFFE

def default_name(cp):
	if is_nonchar(cp):
		return 'NONCHARACTER-%04X' % cp
	elif is_high_surrogate(cp):
		return 'HIGH SURROGATE-%04X' % cp
	elif is_low_surrogate(cp):
		return 'LOW SURROGATE-%04X' % cp
	elif is_control(cp):
		return 'CONTROL-%04X' % cp
	elif is_private(cp):
		return 'PRIVATE USE-%04X' % cp
	else:
		return 'UNDEFINED-%04X' % cp

def html_glyph(cp, acro_fn=None):
	if is_nonchar(cp) or is_surrogate(cp):
		return ''
	if is_control(cp):
		if acro_fn:
			acro = acro_fn(cp)
			if acro:
				return '<abbr>%s</abbr>' % html_encode(acro)
		return ''
	return '&#%d;' % cp

def char_box(cps, canon=None, name_fn=lambda cp: unicodedata.name(chr(cp), None), acro_fn=None):
	is_ltr = (len(cps) > 2 and cps[0] == 0x202D and cps[-1] == 0x202C)
	is_rtl = (len(cps) > 2 and cps[0] == 0x202E and cps[-1] == 0x202C)
	if is_ltr or is_rtl:
		cps = cps[1:-1]
	is_rev = (len(cps) > 1 and cps[-1] == 0xFE0D)
	if is_rev:
		cps = cps[0:-1]
	classes = ['char-box']
	names = [(name_fn(cp), default_name(cp)) for cp in cps]
	titles = [html_encode(n if n else dn) for n, dn in names]
	if canon is True:
		classes.append('char-canon')
	elif canon is False:
		classes.append('char-alt')
	elif canon is not None:
		classes.append(html_encode(canon))
	if any(is_nonchar(cp) for cp in cps):
		classes.append('char-nonchar')
	elif any(is_surrogate(cp) for cp in cps):
		classes.append('char-surrogate')
	elif any(is_control(cp) for cp in cps):
		classes.append('char-control')
	elif any(is_private(cp) for cp in cps):
		classes.append('char-pua')
		classes.append('char-def' if all(n for n, dn in names) else 'char-undef')
	else:
		classes.append('char-uni')
		classes.append('char-def' if all(n for n, dn in names) else 'char-undef')
	if is_ltr:
		classes.append('char-ltr')
		titles.append('&lt;Left-to-Right&gt;')
	if is_rtl:
		classes.append('char-rtl')
		titles.append('&lt;Right-to-Left&gt;')
	if is_rev:
		classes.append('char-rev')
		titles.append('&lt;Reverse-Video&gt;')
	class_attr = ' class="%s"' % ' '.join(classes)
	title_attr = ' title="%s"' % ', '.join(titles)
	code_attr = ' data-codepoint="%s"' % ','.join('%d' % cp for cp in cps)
	glyph_div = '<div class="char-glyph">%s</div>' % ''.join(html_glyph(cp, acro_fn) for cp in cps)
	code_div = '<div class="char-code">%s</div>' % '+'.join('%04X' % cp for cp in cps)
	return '<div%s%s%s>%s%s</div>' % (class_attr, title_attr, code_attr, glyph_div, code_div)

def subtable_box(bs, url_prefix='#', url_delim='', url_suffix=''):
	bs_url = url_prefix + url_delim.join('%02X' % b for b in bs) + url_suffix
	link = '<a href="%s" class="char-subtable-link">%02X</a>' % (bs_url, bs[-1])
	return '<div class="char-box char-subtable">%s</div>' % link

def subtable_row(bs, url_prefix='#', url_delim='', url_suffix=''):
	bs_text = ' '.join('%02X' % b for b in bs)
	bs_url = url_prefix + url_delim.join('%02X' % b for b in bs) + url_suffix
	link = '<a href="%s">&lt;Subtable <code>%s</code>&gt;</a>' % (bs_url, bs_text)
	bcell = '<td class="charlist-codepoint">%s</td>' % bs_text
	ccell = '<td class="charlist-codepoint"></td>'
	gcell = '<td class="charlist-charglyph"></td>'
	ncell = '<td class="charlist-charname">%s</td>' % link
	return '<tr class="charlist-row">%s%s%s%s</tr>' % (bcell, ccell, gcell, ncell)

def char_row(cps, bs=None, canon=None, url_prefix='/charset/unicode/char/', name_fn=lambda cp: unicodedata.name(chr(cp), None), acro_fn=None):
	is_ltr = (len(cps) > 2 and cps[0] == 0x202D and cps[-1] == 0x202C)
	is_rtl = (len(cps) > 2 and cps[0] == 0x202E and cps[-1] == 0x202C)
	if is_ltr or is_rtl:
		cps = cps[1:-1]
	is_rev = (len(cps) > 1 and cps[-1] == 0xFE0D)
	if is_rev:
		cps = cps[0:-1]
	rclasses = ['charlist-row']
	gclasses = ['charlist-charglyph']
	names = [(cp, name_fn(cp), default_name(cp)) for cp in cps]
	links = ['<a href="%s%04X">%s</a>' % (url_prefix, cp, html_encode(n if n else dn)) for cp, n, dn in names]
	if canon is True:
		rclasses.append('charlist-row-canon')
	elif canon is False:
		rclasses.append('charlist-row-alt')
	elif canon is not None:
		rclasses.append(html_encode(canon))
	if is_ltr:
		gclasses.append('charlist-charglyph-ltr')
		links.append('&lt;Left-to-Right&gt;')
	if is_rtl:
		gclasses.append('charlist-charglyph-rtl')
		links.append('&lt;Right-to-Left&gt;')
	if is_rev:
		gclasses.append('charlist-charglyph-rev')
		links.append('&lt;Reverse-Video&gt;')
	rclass_attr = ' class="%s"' % ' '.join(rclasses)
	gclass_attr = ' class="%s"' % ' '.join(gclasses)
	code_attr = ' data-codepoint="%s"' % ','.join('%d' % cp for cp in cps)
	glyph_span = '<span>%s</span>' % ''.join(html_glyph(cp, acro_fn) for cp in cps)
	bcell = '' if bs is None else '<td class="charlist-codepoint">%s</td>' % ' '.join('%02X' % b for b in bs)
	ccell = '<td class="charlist-codepoint">%s</td>' % '+'.join('%04X' % cp for cp in cps)
	gcell = '<td%s%s>%s</td>' % (gclass_attr, code_attr, glyph_span)
	ncell = '<td class="charlist-charname">%s</td>' % ', '.join(links)
	return '<tr%s>%s%s%s%s</tr>' % (rclass_attr, bcell, ccell, gcell, ncell)

EMPTY_CHAR_CELL = '<td><div class="char-box char-nonchar"><div class="char-empty"></div></div></td>'

def char_cell(boxes):
	return ('<td>%s</td>' % ''.join(boxes)) if boxes else EMPTY_CHAR_CELL

def char_table(cells):
	lines = []
	lines.append('<table class="char-table">')
	lines.append('<tr><th></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>')
	lines.extend('<tr><th>%X</th>%s</tr>' % (j, ''.join(cells[(j << 4) : ((j + 1) << 4)])) for j in range(
		16 if any(cell != EMPTY_CHAR_CELL for cell in cells[128:256]) else
		8 if any(cell != EMPTY_CHAR_CELL for cell in cells[64:128]) else
		4 if any(cell != EMPTY_CHAR_CELL for cell in cells[32:64]) else
		2 if any(cell != EMPTY_CHAR_CELL for cell in cells[16:32]) else 1
	))
	lines.append('</table>')
	return '\n'.join(lines)

def char_list(rows):
	midpoint = (len(rows) + 1) >> 1
	lines = []
	lines.append('<div class="charlist-outer-div"><div class="charlist-inner-div"><table class="charlist">')
	lines.extend(rows[:midpoint])
	lines.append('</table></div><div class="charlist-inner-div"><table class="charlist">')
	lines.extend(rows[midpoint:])
	lines.append('</table></div></div>')
	return '\n'.join(lines)

def natural_sort_key(s):
	return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def font_selector(chars, font_chars):
	lines = []
	lines.append('<select id="font-selector">')
	lines.append('<option selected value="inherit">Default</option>')
	total = chars.popcount()
	fonts = [(-font_chars[k].popcount(), natural_sort_key(k), html_encode(k)) for k in font_chars]
	options1 = [(font[2], font[2]) for font in sorted(fonts) if font[0] and -font[0] >= total]
	if options1:
		lines.append('<optgroup label="Full Support">')
		lines.extend('<option value="%s">%s</option>' % option for option in options1)
		lines.append('</optgroup>')
	options2 = [(font[2], font[2], -font[0], total) for font in sorted(fonts) if font[0] and -font[0] < total]
	if options2:
		lines.append('<optgroup label="Partial Support">')
		lines.extend('<option value="%s">%s (%d/%d)</option>' % option for option in options2)
		lines.append('</optgroup>')
	lines.append('</select>')
	return '\n'.join(lines)
