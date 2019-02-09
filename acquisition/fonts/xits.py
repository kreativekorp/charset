#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	for name in ['XITS-Regular', 'XITS-Bold', 'XITS-Italic', 'XITS-BoldItalic', 'XITSMath-Regular', 'XITSMath-Bold']:
		url = 'https://github.com/alif-type/xits/blob/master/%s.otf' % name
		yield (name.replace('-', ' '), acquire(url, 'local'), 'https://github.com/alif-type/xits')
