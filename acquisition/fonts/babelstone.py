#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector

def list_fonts():
	visited = []
	mu = 'https://www.babelstone.co.uk/Fonts/'
	mc = html_link_collector()
	with io.open(acquire(mu, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			mc.feed(line)
	mc.close()
	for ml in mc.links:
		if '/' not in ml and ml.endswith('.html') and ml not in visited:
			visited.append(ml)
			u = mu + ml
			c = html_link_collector()
			with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
				for line in f:
					c.feed(line)
			c.close()
			for l in c.links:
				if l.endswith('.ttf') and l not in visited:
					visited.append(l)
					name = l.split('/')[-1][:-4]
					name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
					yield (name.strip(), acquire(mu + l, 'local'), u)
