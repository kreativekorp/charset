#!/usr/bin/env python

import io
import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'https://www.kurinto.com/'
	collector = html_link_collector()
	with io.open(acquire(u + 'download.htm', 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('_Full.zip'):
			with zipfile.ZipFile(acquire(u + link, 'local'), 'r') as zip:
				for info in zip.infolist():
					if info.filename.endswith('-Rg.ttf'):
						name = info.filename[:-7].split('/')[-1]
						yield (name, zip.extract(info, cache_path()), u)
