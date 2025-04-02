#!/usr/bin/env python

import io
import json
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	with io.open(acquire('https://api.linku.la/v1/fonts', 'local'), mode='r', encoding='utf-8') as f:
		data = json.load(f)
	for name in data:
		if 'links' in data[name]:
			links = data[name]['links']
			if 'fontfile' in links:
				url = links['webpage'] if 'webpage' in links else links['repo'] if 'repo' in links else None
				try:
					yield (name, acquire(links['fontfile'], 'local'), url)
				except Exception as e:
					print('FAILED READ: ' + links['fontfile'] + ': ' + str(e))
