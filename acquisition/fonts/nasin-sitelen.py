#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector
from ttflib import ttf_file

def list_fonts():
	u = 'https://github.com/lipu-linku/nasin-sitelen'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		m = re.search('^/lipu-linku/nasin-sitelen/blob/main/((.+)[.][OoTt][Tt][Ff])$', link)
		if m is not None:
			path = acquire('https://github.com/lipu-linku/nasin-sitelen/raw/main/' + m.group(1), 'local')
			try:
				with ttf_file(path) as ttf:
					name = ttf.name(False)
			except:
				name = 'FAILED READ: ' + m.group(2)
			yield (name, path, None)
