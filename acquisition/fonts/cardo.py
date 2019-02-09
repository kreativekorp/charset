#!/usr/bin/env python

import io
import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	bu = 'http://scholarsfonts.net/'
	u = bu + 'cardofnt.html'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='windows-1252') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	for link in collector.links:
		if link.endswith('.zip'):
			with zipfile.ZipFile(acquire(bu + link, 'local'), 'r') as zip:
				for info in zip.infolist():
					if info.filename.endswith('.ttf'):
						name = info.filename[:-4].split('/')[-1]
						if name.startswith('Cardob'):
							name = 'Cardo Bold'
						elif name.startswith('Cardoi'):
							name = 'Cardo Italic'
						else:
							name = 'Cardo'
						yield (name, zip.extract(info, cache_path()), u)
			break
