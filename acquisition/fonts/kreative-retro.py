#!/usr/bin/env python

import os
import re
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	for name in ['pr', 'petme']:
		with zipfile.ZipFile(acquire('http://www.kreativekorp.com/swdownload/fonts/retro/%s.zip' % name, 'local'), 'r') as zip:
			for info in zip.infolist():
				if info.filename.endswith('.ttf'):
					name = info.filename[:-4]
					name = re.sub('PrintChar', 'Print Char ', name)
					name = re.sub('PRNumber', 'PR Number ', name)
					name = re.sub('PetMe', 'Pet Me ', name)
					name = re.sub('(64|128)(2X|2Y)', '\\1 \\2', name)
					yield (name.strip(), zip.extract(info, cache_path()), 'http://www.kreativekorp.com/software/fonts/')
