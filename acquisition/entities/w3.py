#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

__matcher = re.compile(r'"&([^;"]+);":\s*\{\s*"codepoints":\s*\[\s*([0-9]+)\s*\]')
def list_entities():
	with io.open(acquire('https://html.spec.whatwg.org/entities.json', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			m = __matcher.search(line)
			if m:
				yield int(m.group(2)), '&%s;' % m.group(1)
