#!/usr/bin/env python

import io
import os
import re
import sys
import tarfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'https://pagure.io/liberation-fonts'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if '-ttf-' in link and link.endswith('.tar.gz'):
			with tarfile.open(acquire(link, 'local'), 'r') as tar:
				for name in tar.getnames():
					if name.endswith('.ttf'):
						tar.extract(name, cache_path())
						path = os.path.join(cache_path(), name)
						name = name.split('/')[-1][:-4]
						name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
						name = re.sub('-', ' ', name)
						yield (name, path, u)
			break
