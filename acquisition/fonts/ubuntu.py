#!/usr/bin/env python

import io
import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	# For some reason cURL fails to SSL handshake with the live site.
	u = 'https://design.ubuntu.com/font/'
	wcu = 'http://webcache.googleusercontent.com/search?q=cache:' + u
	collector = html_link_collector()
	with io.open(acquire(wcu, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.zip'):
			with zipfile.ZipFile(acquire(link, 'local'), 'r') as zip:
				for info in zip.infolist():
					if info.filename.endswith('.ttf'):
						name = info.filename.split('/')[-1][:-4]
						name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
						name = re.sub('-', ' ', name)
						yield (name, zip.extract(info, cache_path()), u)
			break
