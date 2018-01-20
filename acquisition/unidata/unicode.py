#!/usr/bin/env python

import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

__textfile_matcher = re.compile('<a href="([^"]+[.][Tt][Xx][Tt])">\\1</a>')
def list_files():
	files = []
	with open(acquire('http://www.unicode.org/Public/UNIDATA/', 'local'), 'r') as f:
		for line in f:
			m = __textfile_matcher.search(line)
			if m is not None:
				files.append(m.group(1))
	for file in files:
		yield (file, acquire('http://www.unicode.org/Public/UNIDATA/' + file, 'local'))
