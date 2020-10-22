#!/usr/bin/env python

from __future__ import print_function

import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib')))
from parselib import atline_matcher, cd, charset_path, expand, ls, strip_comment

def get_puadata():
	with cd(charset_path('puadata')):
		for path in ls('.'):
			if os.path.basename(path) == 'sources.txt':
				meta = {}
				chars = {}
				blocks = []
				for line in expand(path):
					if line:
						fields = strip_comment(line).split(':', 2)
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
				for line in expand(os.path.join(os.path.dirname(path), 'blocks.txt')):
					fields = line.split(';')
					if len(fields) == 2:
						blockname = fields[1].strip()
						fields = fields[0].split('..')
						if len(fields) == 2:
							try:
								start = int(fields[0], 16)
								stop = int(fields[1], 16)
								blocks.append((start, stop, blockname))
							except ValueError:
								continue
				blocks.sort()
				yield meta, chars, blocks

def build_table(fonts, chars, blocks):
	print('<!--#include virtual="/static/head.html"-->')
	print('<title>CSUR/UCSUR Font Support</title>')
	print('<style>')
	print('table { border-collapse: collapse; width: 100%; }')
	print('th, td { border: 1px solid #a2a9b1; margin: 0; padding: 4px; }')
	print('tr:nth-child(even) { background: #f8f8f8; }')
	print('tr.block-name { background: #5f6177; color: white; }')
	print('tr.block-name th { padding: 4px 8px; text-align: left; }')
	print('tr.block-header { background: #eaecf0; }')
	print('.cp-column { text-align: left; width: 50px; }')
	print('.name-column { text-align: left; }')
	print('.font-column { text-align: center; width: 50px; }')
	for tla, fontname in fonts:
		if ' ' in fontname:
			fontname = '"%s"' % fontname
		print('.font-column.%s { font-family: %s, "Adobe Blank"; font-size: 20px; }' % (tla.lower(), fontname))
	print('</style>')
	print('<!--#include virtual="/static/body.html"-->')
	print('<h1>CSUR/UCSUR Font Support</h1>')
	print('<table>')
	for start, stop, blockname in blocks:
		if blockname != 'Private Use Area':
			print('<tr class="block-name"><th colspan="%s">%s</th></tr>' % (len(fonts) + 2, blockname))
			print('<tr class="block-header">')
			print('<th class="cp-column">CP</th>')
			print('<th class="name-column">Name</th>')
			for tla, fontname in fonts:
				print('<th title="%s" class="font-column">%s</th>' % (fontname, tla.upper()))
			print('</tr>')
			for cp in range(start, stop + 1):
				print('<tr>')
				print('<td class="cp-column"><code>%04X</code></td>' % cp)
				if cp in chars:
					print('<td class="name-column"><code>%s</code></td>' % chars[cp][1])
				else:
					print('<td class="name-column"></td>')
				for tla, fontname in fonts:
					print('<td title="%s" class="font-column %s">&#%s;</td>' % (fontname, tla.lower(), cp))
				print('</tr>')
	print('</table>')
	print('<!--#include virtual="/static/tail.html"-->')

def main():
	fonts = [
		('ALC', 'Alco Sans'),
		('CLG', 'Conlang Unicode'),
		('CON', 'Constructium'),
		('EVM', 'Everson Mono'),
		('FFX', 'Fairfax'),
		('FFS', 'Fairfax Serif'),
		('FHD', 'Fairfax HD'),
		('NSK', 'Nishiki-teki'),
		('UNI', 'Unifont CSUR'),
	]
	for meta, chars, blocks in get_puadata():
		if meta['Agreement-Name'] == 'Under-ConScript Unicode Registry (Extended)':
			build_table(fonts, chars, blocks)

if __name__ == '__main__':
	main()
