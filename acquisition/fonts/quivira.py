#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire

def list_fonts():
	yield ('Quivira', acquire('http://www.quivira-font.com/files/Quivira.otf', 'local'), 'http://www.quivira-font.com/')
