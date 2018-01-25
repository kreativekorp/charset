#!/usr/bin/env python

import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path, html_link_collector

def list_fonts():
	u = 'http://junicode.sourceforge.net/'
	du = 'https://sourceforge.net/projects/junicode/files/latest/download'
	with zipfile.ZipFile(acquire(du, 'local', None), 'r') as zip:
		for info in zip.infolist():
			if info.filename.endswith('.ttf'):
				name = info.filename.split('/')[-1][:-4]
				name = re.sub('([a-z])([A-Z])', '\\1 \\2', name)
				name = re.sub('-', ' ', name)
				yield (name, zip.extract(info, cache_path()), u)
