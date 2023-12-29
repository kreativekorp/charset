#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from datalib import get_entities, get_psnames

def main():
	entities = get_entities()
	psnames = get_psnames()
	for cp in range(0, 0x110000):
		if cp in entities:
			print('U+%04X\tHTML_Entity\t%s' % (cp, entities[cp]))
		if cp in psnames:
			print('U+%04X\tPostScript_Name\t%s' % (cp, psnames[cp]))

if __name__ == '__main__':
	main()
