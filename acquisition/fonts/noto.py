#!/usr/bin/env python

import io
import os
import sys
import traceback

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector
from ttflib import ttf_file

def list_fonts():
	u = 'https://fonts.google.com/noto'
	du = 'https://notofonts.github.io/'
	collector = html_link_collector()
	with io.open(acquire(du, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.ttf') or link.endswith('.otf'):
			link = link.replace('[', '%5B')
			link = link.replace(']', '%5D')
			path = acquire(link, 'local')
			try:
				with ttf_file(path) as ttf:
					name = ttf.name(False)
			except Exception as e:
				name = 'FAILED READ: ' + link + ': ' + str(e)
				traceback.print_exc(file=sys.stderr)
			yield (name, path, u)
