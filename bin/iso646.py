#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from iso646lib import iso646_encoding

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

def parse_codepoints(x):
	m = re.match('([0][Xx]|[Uu][+]|[$])([0-9A-Fa-f]+([+][0-9A-Fa-f]+)*)', x)
	if m: return [int(x, 16) for x in m.group(2).split('+')]
	m = re.match('(#?)([0-9]+([+][0-9]+)*)', x)
	if m: return [int(x) for x in m.group(2).split('+')]
	return [ord(x) for x in unicode(x, 'UTF-8')]

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
		for line in iso646_encoding(sorted(cc), sorted(ir), cs, sorted(cp), sorted(mib), m):
			print(line)

if __name__ == '__main__':
	main()
