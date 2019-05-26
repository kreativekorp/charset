#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	for code in ['GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GH', 'GK', 'GV', 'GW', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MH', 'MK', 'MV', 'MW', 'VB', 'VF', 'VN']:
		name = 'Kreative Vexillo %s' % code
		url = 'https://github.com/kreativekorp/vexillo/raw/master/fonts/Vexillo/Vexillo%s.ttf.sbix.ttf' % code
		yield (name, acquire(url, 'local'), 'https://github.com/kreativekorp/vexillo')
