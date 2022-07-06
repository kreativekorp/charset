#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import charset_path, load_plugin, ls

def get_entities():
	entities = {}
	path = charset_path('acquisition', 'entities')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for cp, entity in mod.list_entities():
				entities[cp] = entity
	return entities

def get_psnames():
	psnames = {}
	path = charset_path('acquisition', 'psnames')
	for modfile in ls(path):
		mod = load_plugin(modfile)
		if mod is not None:
			for cp, psname in mod.list_psnames():
				psnames[cp] = psname
	return psnames

def main():
	entities = get_entities()
	psnames = get_psnames()
	for cp in range(0, 0x110000):
		if cp in entities:
			print('U+%X\tHTML_Entity\t%s' % (cp, entities[cp]))
		if cp in psnames:
			print('U+%X\tPostScript_Name\t%s' % (cp, psnames[cp]))

if __name__ == '__main__':
	main()
