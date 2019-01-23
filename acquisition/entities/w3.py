#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

__dec_matcher = re.compile('<td class="dec"><code>&amp;#([0-9]+);')
__named_matcher = re.compile('<td class="named"><code>&amp;([^;]+);')
def list_entities():
	with io.open(acquire('https://dev.w3.org/html5/html-author/charref', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			dm = __dec_matcher.search(line)
			if dm is not None:
				cp = int(dm.group(1))
				nm = __named_matcher.search(line)
				if nm is not None:
					yield cp, '&' + nm.group(1) + ';'
