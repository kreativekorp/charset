#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector

def list_fonts():
	u = 'http://unifoundry.com/unifont/index.html'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='iso-8859-1') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if 'sample' not in link and link.endswith('.ttf'):
			name = link.split('/')[-1].split('-')[0]
			name = re.sub('unifont', 'Unifont', name)
			name = re.sub('upper', 'Upper', name)
			name = re.sub('csur', 'CSUR', name)
			name = re.sub('_', ' ', name)
			yield (name, acquire(link, 'local'), u)
