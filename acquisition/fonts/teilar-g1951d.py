#!/usr/bin/env python

import io
import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'http://users.teilar.gr/~g1951d/'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf16') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.zip'):
			with zipfile.ZipFile(acquire(u + link, 'local'), 'r') as zip:
				for info in zip.infolist():
					if 'hint' not in info.filename and info.filename.endswith('.ttf'):
						name = info.filename[:-4].split('/')[-1]
						yield (name, zip.extract(info, cache_path()), u)
