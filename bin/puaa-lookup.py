#!/usr/bin/env python

from __future__ import print_function

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import ttf_file


def print_help():
	print()
	print('puaa_lookup - Look up Unicode Character Database properties in TrueType files.')
	print()
	print('  -i <path>     Specify source TrueType file.')
	print('  -p <prop>     Specify properties to look up.')
	print('  -c <cp>       Specify code points to look up.')
	print('  --            Process remaining arguments as code points.')
	print()


def parse_cp(s):
	s = re.sub(r'[Uu][+]|[0][Xx]|\s+', '', s)
	return int(s, 16)


def map_from_entries(entries):
	m = {}
	for entry in entries:
		for cp in range(entry.first_code_point, entry.last_code_point + 1):
			if cp in m:
				m[cp] += entry.get_property_string(cp)
			else:
				m[cp] = entry.get_property_string(cp)
	return m


def runs_from_entries(entries):
	m = map_from_entries(entries)
	runs = []
	run = None
	for cp in sorted(m):
		if run is None or run[1] + 1 != cp or run[2] != m[cp]:
			run = [cp, cp, m[cp]]
			runs.append(run)
		else:
			run[1] += 1
	return runs


def print_toc(tables):
	print('Properties:')
	for prop in sorted(tables):
		print('  %s' % prop)


def print_props(tables, properties):
	if len(properties) == 0:
		print_toc(tables)
		return
	for prop in sorted(tables):
		if prop in properties:
			print('%s:' % prop)
			for fcp, lcp, v in runs_from_entries(tables[prop]):
				r = ('%04X:' % fcp) if fcp == lcp else ('%04X..%04X:' % (fcp, lcp))
				print('  %-16s%s' % (r, v))


def print_chars(tables, properties, code_points):
	if len(code_points) == 0:
		print_props(tables, properties)
		return
	name_width = max(len(x) for x in list(tables))
	name_format = '  %%-%ds%%s' % (name_width + 2)
	for prop in list(tables):
		tables[prop] = map_from_entries(tables[prop])
	for cp in sorted(code_points):
		print('U+%04X:' % cp)
		for prop in sorted(tables):
			if len(properties) == 0 or prop in properties:
				if cp in tables[prop]:
					value = tables[prop][cp]
					print(name_format % ('%s:' % prop, value))


def puaa_lookup(args):
	if len(args) == 0:
		print_help()
		return

	tables = None
	properties = []
	code_points = []
	parsing_options = True

	argi = 0
	while argi < len(args):
		arg = args[argi]
		argi += 1
		if parsing_options and arg.startswith('-'):
			if arg == '--':
				parsing_options = False
			elif arg == '-i' and argi < len(args):
				with ttf_file(args[argi]) as ttf:
					tables = ttf.puaas()
				argi += 1
			elif arg == '-p' and argi < len(args):
				properties.append(args[argi])
				argi += 1
			elif arg == '-c' and argi < len(args):
				code_points.append(parse_cp(args[argi]))
				argi += 1
			elif arg == '--help':
				print_help()
			else:
				print('Unknown option: %s' % arg)
		else:
			code_points.append(parse_cp(arg))

	if tables is None:
		return

	print_chars(tables, properties, code_points)


if __name__ == '__main__':
	puaa_lookup(sys.argv[1:])
