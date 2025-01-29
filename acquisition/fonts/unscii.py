#!/usr/bin/env python

import io
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector

def list_fonts():
	u = 'http://viznut.fi/unscii/'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.ttf'):
			du = u + link
			yield ('unscii', acquire(du, 'local'), u)
