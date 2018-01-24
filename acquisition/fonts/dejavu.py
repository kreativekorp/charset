#!/usr/bin/env python

import io
import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'https://dejavu-fonts.github.io/'
	du = 'https://dejavu-fonts.github.io/Download.html'
	collector = html_link_collector()
	with io.open(acquire(du, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		bn = link.split('/')[-1]
		if bn.startswith('dejavu-fonts-ttf') and bn.endswith('.zip'):
			du = 'https://downloads.sourceforge.net/project/dejavu/dejavu/%s/%s' % (bn[17:-4], bn)
			with zipfile.ZipFile(acquire(du, 'local', None), 'r') as zip:
				for info in zip.infolist():
					if info.filename.endswith('.ttf'):
						name = info.filename.split('/')[-1][:-4]
						name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
						name = re.sub('Deja Vu', 'DejaVu', name)
						name = re.sub('-', ' ', name)
						yield (name, zip.extract(info, cache_path()), u)
