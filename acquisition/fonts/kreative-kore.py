#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	yield ('Constructium', acquire('http://www.kreativekorp.com/lib/font/Constructium.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/constructium.shtml')
	yield ('Fairfax', acquire('http://www.kreativekorp.com/lib/font/Fairfax.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/fairfax.shtml')
	yield ('Fairfax Bold', acquire('http://www.kreativekorp.com/lib/font/FairfaxBold.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/fairfax.shtml')
	yield ('Fairfax Italic', acquire('http://www.kreativekorp.com/lib/font/FairfaxItalic.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/fairfax.shtml')
	yield ('Fairfax Serif', acquire('http://www.kreativekorp.com/lib/font/FairfaxSerif.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/fairfax.shtml')
	yield ('Fairfax HD', acquire('http://www.kreativekorp.com/lib/font/FairfaxHD.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/fairfax.shtml')
	yield ('Kreative Square', acquire('http://www.kreativekorp.com/lib/font/KreativeSquare.ttf', 'local'), 'http://www.kreativekorp.com/software/fonts/')
