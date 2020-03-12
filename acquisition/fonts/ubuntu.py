#!/usr/bin/env python

import io
import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'https://design.ubuntu.com/font/'
	collector = html_link_collector()
	with io.open(acquire(u, 'local', compressed=True), mode='r', encoding='iso-8859-1') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.zip'):
			with zipfile.ZipFile(acquire(link, 'local'), 'r') as zip:
				for info in zip.infolist():
					if '__MACOSX' in info.filename:
						continue
					if info.filename.endswith('.ttf'):
						name = info.filename.split('/')[-1][:-4]
						name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
						name = re.sub('-', ' ', name)
						yield (name, zip.extract(info, cache_path()), u)
			break
