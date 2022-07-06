#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

__matcher = re.compile(r'^([0-9A-Fa-f]+);([^;]+);')
def list_psnames():
	with io.open(acquire('https://raw.githubusercontent.com/adobe-type-tools/agl-aglfn/master/aglfn.txt', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			m = __matcher.search(line)
			if m:
				yield int(m.group(1), 16), m.group(2)
