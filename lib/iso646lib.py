#!/usr/bin/env python

import re
import unicodedata

def __iso646_line(a, m):
	u = m[a] if a in m else [a]
	h = '+'.join('0x%04X' % u for u in u)
	n = ', '.join(unicodedata.name(unichr(u)) for u in u)
	return '0x%02X\t%s\t# %s' % (a, h, n)

def iso646_encoding(cc, ir, cs, cp, mib, m):
	yield '@category\tISO 646'
	if len(cc) > 1: yield '@display\tISO 646-%s' % '/'.join(cc.upper() for cc in cc)
	for x in cc: yield '@name\tISO 646-%s' % x.upper()
	for x in cc: yield '@alias\t646-%s' % x.upper()
	for x in ir: yield '@alias\tISO IR-%d' % x
	for x in ir: yield '@alias\tIR-%d' % x
	for x in cs: yield '@charset\t%s' % x
	for x in cp: yield '@codepage\t%d' % x
	for x in mib: yield '@mibenum\t%d' % x
	for x in cc: yield '@filename-kte\tiso-646-%s.kte' % re.sub('[^A-Za-z0-9]+', '-', x).lower()
	yield '@import\tfragments/ascii-c0.txt\t# NULL .. UNIT SEPARATOR'
	yield '@import\tfragments/ascii-sq.txt\t# SPACE .. QUOTATION MARK'
	yield __iso646_line(0x23, m)
	yield __iso646_line(0x24, m)
	yield '@import\tfragments/ascii-pq.txt\t# PERCENT SIGN .. QUESTION MARK'
	yield __iso646_line(0x40, m)
	yield '@import\tfragments/ascii-uc.txt\t# LATIN CAPITAL LETTER A .. LATIN CAPITAL LETTER Z'
	yield __iso646_line(0x5B, m)
	yield __iso646_line(0x5C, m)
	yield __iso646_line(0x5D, m)
	yield __iso646_line(0x5E, m)
	yield __iso646_line(0x5F, m)
	yield __iso646_line(0x60, m)
	yield '@import\tfragments/ascii-lc.txt\t# LATIN SMALL LETTER A .. LATIN SMALL LETTER Z'
	yield __iso646_line(0x7B, m)
	yield __iso646_line(0x7C, m)
	yield __iso646_line(0x7D, m)
	yield __iso646_line(0x7E, m)
	yield '@import\tfragments/ascii-del.txt\t# DELETE'
