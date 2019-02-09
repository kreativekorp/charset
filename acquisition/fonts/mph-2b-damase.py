#!/usr/bin/env python

import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	with zipfile.ZipFile(acquire('http://www.wazu.jp/downloads/damase_v.2.zip', 'local'), 'r') as zip:
		for info in zip.infolist():
			if '._' not in info.filename and info.filename.endswith('.ttf'):
				yield ('MPH 2B Damase', zip.extract(info, cache_path()), 'http://www.wazu.jp/gallery/views/View_MPH2BDamase.html')
