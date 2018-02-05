#!/usr/bin/env python

import io
import os
import sys
import tarfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'http://sofia.nmsu.edu/~mleisher/Software/cu/'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.tgz'):
			with tarfile.open(acquire(link, 'local'), 'r') as tar:
				for name in tar.getnames():
					if name.endswith('.bdf'):
						tar.extract(name, cache_path())
						path = os.path.join(cache_path(), name)
						name = name.split('/')[-1][:-4]
						with open(path, 'r') as bdf:
							for line in bdf:
								if line.startswith('FAMILY_NAME'):
									name = line[11:].strip()
									if name.startswith('"') and name.endswith('"'):
										name = name[1:-1]
						yield (name, path, u)
