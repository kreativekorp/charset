#!/usr/bin/env python

import os
import sys
import zipfile

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, cache_path

def list_fonts():
	yield ('Nishiki-teki', acquire('http://umihotaru.fool.jp/nishiki-teki.ttf', 'local'), 'https://umihotaru.work/')
