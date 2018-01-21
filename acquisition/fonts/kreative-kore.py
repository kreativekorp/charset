#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	yield ('Constructium', acquire('http://www.kreativekorp.com/lib/font/Constructium.ttf', 'local'))
	yield ('Fairfax', acquire('http://www.kreativekorp.com/lib/font/Fairfax.ttf', 'local'))
	yield ('Fairfax Bold', acquire('http://www.kreativekorp.com/lib/font/FairfaxBold.ttf', 'local'))
	yield ('Fairfax Italic', acquire('http://www.kreativekorp.com/lib/font/FairfaxItalic.ttf', 'local'))
	yield ('Fairfax Serif', acquire('http://www.kreativekorp.com/lib/font/FairfaxSerif.ttf', 'local'))
	yield ('Fairfax HD', acquire('http://www.kreativekorp.com/lib/font/FairfaxHD.ttf', 'local'))
	yield ('Kreative Square', acquire('http://www.kreativekorp.com/lib/font/KreativeSquare.ttf', 'local'))
