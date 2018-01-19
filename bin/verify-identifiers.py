#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import cd, charset_path, expand, is_atline, ls, split_atline, strip_comment

def get_assertions():
	assertions = {}
	with cd(charset_path('identifiers')):
		for path in ls('.'):
			headers = []
			dotdotdot = False
			for line in expand(path):
				if is_atline(line):
					headers = []
					dotdotdot = False
					for field in strip_comment(line).split():
						if field == '...':
							dotdotdot = True
							break
						elif field[0] == '@':
							headers.append(field[1:].lower())
						else:
							headers.append(field.lower())
				else:
					aa = []
					fields = strip_comment(line).split()
					for i in range(0, len(fields)):
						if dotdotdot or i < len(headers):
							if fields[i] != '--':
								aa.append((headers[i if i < len(headers) else -1], fields[i].lower()))
					for a in aa:
						if a not in assertions:
							assertions[a] = []
						assertions[a].extend(aa)
	return assertions

def verify(path, assertions):
	atlines = []
	for line in expand(path):
		k, v = split_atline(line)
		if k is not None and v is not None:
			atlines.append((k.lower(), v.lower()))
	if len(atlines) == 0:
		return None
	else:
		errors = []
		for a in atlines:
			if a in assertions:
				for b in assertions[a]:
					if b not in atlines:
						errors.append((a[0], a[1], b[0], b[1]))
		return errors

def main():
	assertions = get_assertions()
	with cd(charset_path('mappings')):
		for path in ls('.'):
			errors = verify(path, assertions)
			if errors is not None:
				if len(errors) > 0:
					print('mappings/%s: FAILED:' % path[2:])
					for e in errors:
						print('Encoding with %s %s must have %s %s.' % e)
				else:
					print('mappings/%s: PASSED' % path[2:])

if __name__ == '__main__':
	main()
