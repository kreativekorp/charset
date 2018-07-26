#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	for id in ['source-code-pro', 'source-sans-pro', 'source-serif-pro']:
		u = 'https://github.com/adobe-fonts/' + id
		collector = html_link_collector()
		with io.open(acquire(u + '/releases', 'local'), mode='r', encoding='utf-8') as f:
			for line in f:
				collector.feed(line)
		collector.close()
		for link in collector.links:
			if link.endswith('.ttf') or link.endswith('.otf'):
				du = 'https://github.com' + link
				name = link.split('/')[-1][:-4]
				name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
				name = re.sub('( *Variable)?-(Roman)?', ' Pro ', name)
				yield (name.strip(), acquire(du, 'local'), u)
			elif link.endswith('.zip') or link.endswith('.tar.gz'):
				break
