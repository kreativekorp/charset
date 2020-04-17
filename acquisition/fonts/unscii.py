#!/usr/bin/env python

import io
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector

def list_fonts():
	u = 'http://pelulamu.net/unscii/'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='UTF-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.ttf'):
			yield (link[:-4], acquire(u + link, 'local'), u)
