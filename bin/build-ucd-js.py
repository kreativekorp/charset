#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import cd, charset_path, expand, load_plugin, ls

def get_unidata():
	ranges = {}
	chars = {}
	path = charset_path('acquisition', 'unidata')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for name, path in mod.list_files():
				if name == 'UnicodeData.txt':
					with open(path, 'r') as ucd:
						for line in ucd:
							fields = line.strip().split(';')
							try:
								cp = int(fields[0], 16)
								if fields[1][:1] == '<' and fields[1][-3:] == 'st>':
									range_name = fields[1][1:-1].split(', ')
									if range_name[0] not in ranges:
										ranges[range_name[0]] = [cp, cp, fields, fields]
									elif range_name[1] == 'First':
										ranges[range_name[0]][0] = cp
										ranges[range_name[0]][2] = fields
									elif range_name[1] == 'Last':
										ranges[range_name[0]][1] = cp
										ranges[range_name[0]][3] = fields
								else:
									chars[cp] = fields
							except ValueError:
								continue
	return ranges, chars

def get_puadata():
	puadata = charset_path('out', 'PUADATA')
	with cd(charset_path('puadata')):
		for path in ls('.'):
			if os.path.basename(path) == 'sources.txt':
				meta = {}
				chars = {}
				for line in expand(path):
					if line:
						fields = line.split(':', 2)
						if len(fields) == 2:
							meta[fields[0].strip()] = fields[1].strip()
					else:
						break
				for line in expand(os.path.join(os.path.dirname(path), 'unicodedata.txt')):
					fields = line.split(';')
					try:
						cp = int(fields[0], 16)
						chars[cp] = fields
					except ValueError:
						continue
				yield meta, chars

def get_entities():
	entities = {}
	path = charset_path('acquisition', 'entities')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for cp, entity in mod.list_entities():
				if cp not in entities:
					entities[cp] = entity
	return entities

def main():
	ucd = {}
	ucd['ranges'], ucd['chars'] = get_unidata()

	path = charset_path('out', 'ucd.js')
	with open(path, 'w') as f:
		f.write('UCD=%s;' % json.dumps(ucd, separators=(',', ':')))
	print(path)

	pua = {}
	for meta, chars in get_puadata():
		if 'Agreement-Type' in meta:
			if meta['Agreement-Type'] == 'Please-Ignore':
				continue
		meta['chars'] = chars
		if 'Agreement-Name' in meta:
			pua[meta['Agreement-Name']] = meta
		else:
			pua[len(pua)] = meta

	path = charset_path('out', 'pua.js')
	with open(path, 'w') as f:
		f.write('PUA=%s;' % json.dumps(pua, separators=(',', ':')))
	print(path)

	entities = get_entities()

	path = charset_path('out', 'entitydb.js')
	with open(path, 'w') as f:
		f.write('ENTITYDB=%s;' % json.dumps(entities, separators=(',', ':')))
	print(path)

if __name__ == '__main__':
	main()
