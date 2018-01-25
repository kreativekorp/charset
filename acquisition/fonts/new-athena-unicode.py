#!/usr/bin/env python

import io
import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'https://apagreekkeys.org/NAUdownload.html'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	latestDate = None
	latestLink = None
	for link in collector.links:
		m = re.search('/NAU([0-9_]+)[.]zip$', link)
		if m is not None:
			if latestDate is None or m.group(1) > latestDate:
				latestDate = m.group(1)
				latestLink = link
	with zipfile.ZipFile(acquire('https://apagreekkeys.org/' + latestLink, 'local'), 'r') as zip:
		for info in zip.infolist():
			if info.filename.endswith('.ttf'):
				name = info.filename.split('/')[-1][:-4]
				name = re.sub('newathu', 'New Athena Unicode', name)
				name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
				name = re.sub('[0-9_]+', '', name)
				yield (name, zip.extract(info, cache_path()), u)
