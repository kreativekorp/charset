#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys
import time

__dateline = re.compile('(#\\s+[Dd]ate:\\s+)([0-9A-Za-z,:/-]+( +[0-9A-Za-z,:/-]+)*)')
__codepoint = re.compile('\\b(0[Xx])([0-9A-Fa-f]{4,6})\\b')

def remap_line(line, remap):
	def __dateline_repl(m):
		t = time.strftime('%Y %B %e')
		t = re.sub('\\s+', ' ', t)
		return m.group(1) + t
	def __codepoint_repl(m):
		if m.start(0) > 0:
			v = int(m.group(2), 16)
			for s, e, ns in remap:
				if v >= s and v <= e:
					return '%s%04X' % (m.group(1), v - s + ns)
		return m.group(0)
	line = __dateline.sub(__dateline_repl, line)
	line = __codepoint.sub(__codepoint_repl, line)
	return line

__remapspec = re.compile('([0][Xx]|[Uu][+])?([0-9A-Fa-f]+)-([0][Xx]|[Uu][+])?([0-9A-Fa-f]+)=([<>:+-])?([0][Xx]|[Uu][+])?([0-9A-Fa-f]+)')

def main():
	outdir = None
	remap = []
	for arg in sys.argv[1:]:
		if arg == '--help':
			print('remap.py -- remap code points in Format A mapping files')
			print()
			print('usage:')
			print('  remap.py [-D=<path>] [<start>-<end>=[(+|-)]<newstart> [...]] [<file> [...]]')
			print()
			print('options:')
			print('  -D=<path>                   specify output directory')
			print('  <start>-<end>=<newstart>    remap <start>-<end> to <newstart>')
			print('  <start>-<end>=+<offset>     remap <start>-<end> forward <offset> code points')
			print('  <start>-<end>=-<offset>     remap <start>-<end> backward <offset> code points')
		elif arg.startswith('-D='):
			outdir = arg[3:]
		else:
			m = __remapspec.match(arg)
			if m is not None:
				s = int(m.group(2), 16)
				e = int(m.group(4), 16)
				op = m.group(5)
				ns = int(m.group(7), 16)
				if op == '+':
					remap.append((s, e, s + ns))
				elif op == '-':
					remap.append((s, e, s - ns))
				else:
					remap.append((s, e, ns))
			else:
				if outdir is not None:
					out = os.path.join(outdir, os.path.basename(arg))
				elif arg.lower().endswith('.txt'):
					out = arg[:-4] + '-2' + arg[-4:]
				else:
					out = arg + '-2'
				with open(arg, 'r') as inf:
					with open(out, 'w') as outf:
						for line in inf:
							outf.write(remap_line(line, remap))

if __name__ == '__main__':
	main()
