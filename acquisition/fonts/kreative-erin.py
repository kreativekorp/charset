#!/usr/bin/env python

import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	for name in ['magdalena', 'mcmillen', 'mischke', 'monterey']:
		with zipfile.ZipFile(acquire('http://www.kreativekorp.com/swdownload/fonts/relaybm/%s.zip' % name, 'local'), 'r') as zip:
			for info in zip.infolist():
				if info.filename.endswith('.ttf'):
					yield (re.sub('Bold', ' Bold', info.filename[:-4]), zip.extract(info, cache_path()), 'http://www.kreativekorp.com/software/fonts/')
