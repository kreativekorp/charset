#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from ttflib import dfont_file

def main():
	for arg in sys.argv[1:]:
		with dfont_file(arg) as dfont:
			print('Type\tID\tOffset\tLength\tName')
			for type in dfont.types:
				for resource in type.resources:
					name = '' if resource.name is None else resource.name
					print('%s\t%d\t%d\t%d\t%s' % (type.type, resource.id, resource.offset, resource.length, name))

if __name__ == '__main__':
	main()
