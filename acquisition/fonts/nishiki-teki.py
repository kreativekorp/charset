#!/usr/bin/env python

import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	with zipfile.ZipFile(acquire('https://umihotaru.work/nishiki-teki.zip', 'local'), 'r') as zip:
		for info in zip.infolist():
			if info.filename.endswith('.ttf'):
				yield ('Nishiki-teki', zip.extract(info, cache_path()), 'https://umihotaru.work/')
