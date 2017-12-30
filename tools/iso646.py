#!/usr/bin/env python

from __future__ import print_function

import re
import sys
import unicodedata

def iso646_line(a, m):
	u = m[a] if a in m else [a]
	h = '+'.join('0x%04X' % u for u in u)
	n = ', '.join(unicodedata.name(unichr(u)) for u in u)
	return '0x%02X\t%s\t# %s' % (a, h, n)

def iso646(cc, ir, cs, cp, mib, m):
	print('@category\tISO 646')
	if len(cc) > 1: print('@display\tISO 646-%s' % '/'.join(cc.upper() for cc in cc))
	for x in cc: print('@name\tISO 646-%s' % x.upper())
	for x in cc: print('@alias\t646-%s' % x.upper())
	for x in ir: print('@alias\tISO IR-%d' % x)
	for x in ir: print('@alias\tIR-%d' % x)
	for x in cs: print('@charset\t%s' % x)
	for x in cp: print('@codepage\t%d' % x)
	for x in mib: print('@mibenum\t%d' % x)
	for x in cc: print('@filename-kte\tiso-646-%s.kte' % re.sub('[^A-Za-z0-9]+', '-', x).lower())
	print('@import\tfragments/ascii-c0.txt\t# NULL .. UNIT SEPARATOR')
	print('@import\tfragments/ascii-sq.txt\t# SPACE .. QUOTATION MARK')
	print(iso646_line(0x23, m))
	print(iso646_line(0x24, m))
	print('@import\tfragments/ascii-pq.txt\t# PERCENT SIGN .. QUESTION MARK')
	print(iso646_line(0x40, m))
	print('@import\tfragments/ascii-uc.txt\t# LATIN CAPITAL LETTER A .. LATIN CAPITAL LETTER Z')
	print(iso646_line(0x5B, m))
	print(iso646_line(0x5C, m))
	print(iso646_line(0x5D, m))
	print(iso646_line(0x5E, m))
	print(iso646_line(0x5F, m))
	print(iso646_line(0x60, m))
	print('@import\tfragments/ascii-lc.txt\t# LATIN SMALL LETTER A .. LATIN SMALL LETTER Z')
	print(iso646_line(0x7B, m))
	print(iso646_line(0x7C, m))
	print(iso646_line(0x7D, m))
	print(iso646_line(0x7E, m))
	print('@import\tfragments/ascii-del.txt\t# DELETE')

def parse_codepoints(x):
	m = re.match('([0][Xx]|[Uu][+]|[$])([0-9A-Fa-f]+([+][0-9A-Fa-f]+)*)', x)
	if m: return [int(x, 16) for x in m.group(2).split('+')]
	m = re.match('(#?)([0-9]+([+][0-9]+)*)', x)
	if m: return [int(x) for x in m.group(2).split('+')]
	return [ord(x) for x in unicode(x, 'UTF-8')]

def help():
	print('usage: iso646.py <options>')
	print('  --cc <country-code>   the ISO country code')
	print('  --ir <ir-number>      the ISO IR number')
	print('  --cs <charset-name>   the IANA charset name')
	print('  --cp <codepage-num>   the IBM code page number')
	print('  --mib <mibenum>       the IANA MIB enum number')
	print('  -3 <code-point>       the replacement character for 0x23 / #')
	print('  -4 <code-point>       the replacement character for 0x24 / $')
	print('  -A <code-point>       the replacement character for 0x40 / @')
	print('  -B <code-point>       the replacement character for 0x5B / [')
	print('  -C <code-point>       the replacement character for 0x5C / \\')
	print('  -D <code-point>       the replacement character for 0x5D / ]')
	print('  -E <code-point>       the replacement character for 0x5E / ^')
	print('  -F <code-point>       the replacement character for 0x5F / _')
	print('  -a <code-point>       the replacement character for 0x60 / `')
	print('  -b <code-point>       the replacement character for 0x7B / {')
	print('  -c <code-point>       the replacement character for 0x7C / |')
	print('  -d <code-point>       the replacement character for 0x7D / }')
	print('  -e <code-point>       the replacement character for 0x7E / ~')

def main():
	cc = []
	ir = []
	cs = []
	cp = []
	mib = []
	m = {}
	i = 1
	while i < len(sys.argv):
		arg = sys.argv[i]
		i += 1
		if arg == '--help':
			help()
			sys.exit(0)
		elif arg == '--cc' and i < len(sys.argv):
			cc.append(sys.argv[i])
			i += 1
		elif arg == '--ir' and i < len(sys.argv):
			ir.append(int(sys.argv[i]))
			i += 1
		elif (arg == '--cs' or arg == '--charset') and i < len(sys.argv):
			cs.append(sys.argv[i])
			i += 1
		elif (arg == '--cp' or arg == '--codepage') and i < len(sys.argv):
			cp.append(int(sys.argv[i]))
			i += 1
		elif (arg == '--mib' or arg == '--mibenum') and i < len(sys.argv):
			mib.append(int(sys.argv[i]))
			i += 1
		elif arg == '-3' and i < len(sys.argv):
			m[0x23] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-4' and i < len(sys.argv):
			m[0x24] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-A' and i < len(sys.argv):
			m[0x40] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-B' and i < len(sys.argv):
			m[0x5B] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-C' and i < len(sys.argv):
			m[0x5C] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-D' and i < len(sys.argv):
			m[0x5D] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-E' and i < len(sys.argv):
			m[0x5E] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-F' and i < len(sys.argv):
			m[0x5F] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-a' and i < len(sys.argv):
			m[0x60] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-b' and i < len(sys.argv):
			m[0x7B] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-c' and i < len(sys.argv):
			m[0x7C] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-d' and i < len(sys.argv):
			m[0x7D] = parse_codepoints(sys.argv[i])
			i += 1
		elif arg == '-e' and i < len(sys.argv):
			m[0x7E] = parse_codepoints(sys.argv[i])
			i += 1
		elif len(cc) < 1:
			cc.append(arg)
		elif 0x23 not in m:
			m[0x23] = parse_codepoints(arg)
		elif 0x24 not in m:
			m[0x24] = parse_codepoints(arg)
		elif 0x40 not in m:
			m[0x40] = parse_codepoints(arg)
		elif 0x5B not in m:
			m[0x5B] = parse_codepoints(arg)
		elif 0x5C not in m:
			m[0x5C] = parse_codepoints(arg)
		elif 0x5D not in m:
			m[0x5D] = parse_codepoints(arg)
		elif 0x5E not in m:
			m[0x5E] = parse_codepoints(arg)
		elif 0x5F not in m:
			m[0x5F] = parse_codepoints(arg)
		elif 0x60 not in m:
			m[0x60] = parse_codepoints(arg)
		elif 0x7B not in m:
			m[0x7B] = parse_codepoints(arg)
		elif 0x7C not in m:
			m[0x7C] = parse_codepoints(arg)
		elif 0x7D not in m:
			m[0x7D] = parse_codepoints(arg)
		elif 0x7E not in m:
			m[0x7E] = parse_codepoints(arg)
		else:
			cs.append(arg)
	if len(cc) < 1:
		help()
	else:
		iso646(sorted(cc), sorted(ir), cs, sorted(cp), sorted(mib), m)

if __name__ == '__main__':
	main()
