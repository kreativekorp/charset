#!/usr/bin/env python

import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	things = [
		(
			'https://web.archive.org/web/20101122142710/http://code2000.net/code2000_page.htm',
			'https://web.archive.org/web/20101122151653/http://code2000.net/CODE2000.ZIP'
		),
		(
			'https://web.archive.org/web/20101122142330/http://code2000.net/code2001.htm',
			'https://web.archive.org/web/20101122142911/http://code2000.net/CODE2001.ZIP'
		),
		(
			'https://web.archive.org/web/20110108105420/http://code2000.net/',
			'https://web.archive.org/web/20101215114012/http://code2000.net/CODE2002.ZIP'
		)
	]
	for hu, du in things:
		with zipfile.ZipFile(acquire(du, 'local'), 'r') as zip:
			for info in zip.infolist():
				if info.filename.endswith('.TTF'):
					yield (info.filename[:-4], zip.extract(info, cache_path()), hu)
