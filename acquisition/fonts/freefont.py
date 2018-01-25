#!/usr/bin/env python

import io
import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'http://savannah.gnu.org/projects/freefont/'
	du = 'http://ftp.gnu.org/gnu/freefont/'
	collector = html_link_collector()
	with io.open(acquire(du, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	latestDate = None
	latestLink = None
	for link in collector.links:
		m = re.match('^freefont-[ot]tf-([0-9]+)[.]zip$', link)
		if m is not None:
			if latestDate is None or m.group(1) > latestDate:
				latestDate = m.group(1)
				latestLink = link
	with zipfile.ZipFile(acquire(du + latestLink, 'local'), 'r') as zip:
		for info in zip.infolist():
			if info.filename.endswith('.ttf') or info.filename.endswith('.otf'):
				name = info.filename.split('/')[-1][:-4]
				name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
				name = re.sub('Free (Sans|Serif|Mono)', 'Free\\1', name)
				yield (name, zip.extract(info, cache_path()), u)
