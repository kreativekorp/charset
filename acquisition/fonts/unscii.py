#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	u = 'http://pelulamu.net/unscii/'
	du = 'http://pelulamu.net/unscii/unscii-16.ttf'
	yield ('unscii', acquire(du, 'local'), u)
