#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from acquisitionlib import acquire
from parselib import atline_matcher, cd, charset_path, expand, ls, split_mapline

__verify_matcher = atline_matcher('verify-against')
__jis_x_0208_matcher = re.compile('^\\s*([0][Xx][0-9A-Fa-f]+)\\s+([0][Xx][0-9A-Fa-f]+)\\s+([0][Xx][0-9A-Fa-f]+)')
__adobe_line_matcher = re.compile('^\\s*([0-9A-Fa-f]+)\\s+([0-9A-Fa-f]+)')
__delimited_byte_matcher = re.compile('^\\s*([0][Xx][0-9A-Fa-f]{2}([+][0][Xx][0-9A-Fa-f]{2})+)\\s+[0][Xx]')
__delimited_byte_sub = re.compile('[+][0][Xx]')
__odd_hex_digits_sub = re.compile('^(\\s*[0][Xx])([0-9A-Fa-f]([0-9A-Fa-f]{2})*\\s+)')
__apple_lr_sub = re.compile('(\\s+)<LR>(([+][0][Xx][0-9A-Fa-f]+)+)')
__apple_rl_sub = re.compile('(\\s+)<RL>(([+][0][Xx][0-9A-Fa-f]+)+)')

def verify(path):
	url = None
	map = {}
	for line in expand(path):
		u = __verify_matcher.match(line)
		if u is not None:
			url = u
		else:
			b, c, ba, ca = split_mapline(line)
			if b is not None and c is not None:
				if not ba or tuple(b) not in map:
					map[tuple(b)] = tuple(c)
	if url is None:
		return None
	else:
		expmap = {}
		with open(acquire(url, 'local'), 'r') as f:
			for line in f:
				# Hacks for reference encodings: JIS X 0208 has three columns.
				if url.endswith('/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT'):
					m = __jis_x_0208_matcher.match(line)
					if m is not None:
						line = line[:m.start(1)] + m.group(2) + '\t' + m.group(3) + line[m.end(3):]
				# Hacks for reference encodings: Adobe reverses bytes and chars.
				if '/MAPPINGS/VENDORS/ADOBE/' in url:
					m = __adobe_line_matcher.match(line)
					if m is not None:
						if (int(m.group(2), 16),) in expmap:
							continue
						elif url.endswith('/symbol.txt') and m.group(1) == '00B5' and m.group(2) == '6D':
							continue
						else:
							line = line[:m.start(1)] + '0x' + m.group(2) + '\t0x' + m.group(1) + line[m.end(2):]
				# Hacks for reference encodings: Bytes delimited by +0x.
				m = __delimited_byte_matcher.match(line)
				if m is not None:
					line = line[:m.start(1)] + __delimited_byte_sub.sub('', m.group(1)) + line[m.end(1):]
				# Hacks for reference encodings: Odd number of hex digits in bytes.
				line = __odd_hex_digits_sub.sub('\\g<1>0\\g<2>', line)
				# Hacks for reference encodings: Apple's <LR> and <RL> markup.
				line = __apple_lr_sub.sub('\\g<1>0x202D\\g<2>+0x202C', line)
				line = __apple_rl_sub.sub('\\g<1>0x202E\\g<2>+0x202C', line)
				# End hacks.
				b, c, ba, ca = split_mapline(line)
				if b is not None and c is not None:
					expmap[tuple(b)] = tuple(c)
		if not url.endswith('/MAPPINGS/OBSOLETE/EASTASIA/OTHER/CNS11643.TXT'):
			# Hacks for reference encodings: No ASCII characters.
			if all((x,) not in expmap and (x,x) not in expmap for x in range(0, 128)):
				for x in range(0, 128):
					expmap[(x,)] = (x,)
			# Hacks for reference encodings: No C0 control characters.
			if all((x,) not in expmap and (x,x) not in expmap for x in range(0, 32) + [127]):
				for x in range(0, 32) + [127]:
					expmap[(x,)] = (x,)
			# Hacks for reference encodings: No C1 control characters.
			if '/MAPPINGS/VENDORS/ADOBE/' in url or '/MAPPINGS/OBSOLETE/EASTASIA/' in url:
				if any((x,) in expmap for x in range(160, 256)) or url.endswith('/BIG5.TXT'):
					if all((x,) not in expmap and (x,x) not in expmap for x in range(128, 160)):
						for x in range(128, 160):
							expmap[(x,)] = (x,)
		# Hacks for reference encodings: Undefined characters mapped to U+FFFD.
		for k, v in expmap.items():
			if v == (0xFFFD,):
				del expmap[k]
		# End hacks.
		return set(map.items()) ^ set(expmap.items())

def main():
	with cd(charset_path('mappings')):
		for path in ls('.'):
			result = verify(path)
			if result is not None:
				if len(result) > 0:
					print('mappings/%s: FAILED:\n%r' % (path[2:], result))
				else:
					print('mappings/%s: PASSED' % path[2:])

if __name__ == '__main__':
	main()
