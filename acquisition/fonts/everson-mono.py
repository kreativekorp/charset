#!/usr/bin/env python

import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	with zipfile.ZipFile(acquire('http://www.evertype.com/emono/evermono.zip', 'local'), 'r') as zip:
		for info in zip.infolist():
			if '._' not in info.filename and info.filename.endswith('.ttf'):
				yield (info.filename[:-4].split('/')[-1], zip.extract(info, cache_path()))
