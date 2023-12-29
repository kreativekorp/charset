#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from datalib import get_entities, get_psnames, get_puadata, get_unidata
from parselib import charset_path

def main():
	shared = charset_path('out', 'shared')
	if not os.path.exists(shared):
		os.makedirs(shared)

	ucd = {}
	ucd['ranges'], ucd['chars'], ucd['blocks'] = get_unidata()
	path = os.path.join(shared, 'ucd.js')
	print('Writing Unicode data: %s' % path)
	with open(path, 'w') as f:
		f.write('UCD=%s;' % json.dumps(ucd, separators=(',', ':')))

	pua = {}
	for meta, chars, blocks in get_puadata():
		if 'Agreement-Type' in meta:
			if meta['Agreement-Type'] == 'Please-Ignore':
				continue
		meta['chars'] = chars
		meta['blocks'] = blocks
		pua[meta['Agreement-Name']] = meta
	path = os.path.join(shared, 'pua.js')
	print('Writing Private Use Area data: %s' % path)
	with open(path, 'w') as f:
		f.write('PUA=%s;' % json.dumps(pua, separators=(',', ':')))

	entities = get_entities()
	path = os.path.join(shared, 'entitydb.js')
	print('Writing named character entity data: %s' % path)
	with open(path, 'w') as f:
		f.write('ENTITYDB=%s;' % json.dumps(entities, separators=(',', ':')))

	psnames = get_psnames()
	path = os.path.join(shared, 'psnamedb.js')
	print('Writing PostScript name data: %s' % path)
	with open(path, 'w') as f:
		f.write('PSNAMEDB=%s;' % json.dumps(psnames, separators=(',', ':')))

if __name__ == '__main__':
	main()
