#!/usr/bin/env python

import io
import os
import re
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'lib')))
from acquisitionlib import acquire, html_link_collector
from ttflib import ttf_file

def list_fonts():
	u = 'https://github.com/lipu-linku/sona/tree/main/fonts/metadata'
	collector = html_link_collector()
	with io.open(acquire(u, 'local'), mode='r', encoding='utf-8') as f:
		for line in f:
			collector.feed(line)
	collector.close()
	tomls = list(set([link for link in collector.links if link.endswith('.toml')]))
	for toml in tomls:
		toml_url = 'https://raw.githubusercontent.com' + re.sub('/blob/', '/refs/heads/', toml)
		toml_path = acquire(toml_url, 'local')
		font_url = None
		repo_url = None
		webpage_url = None
		with io.open(toml_path, mode='r', encoding='utf-8') as f:
			for line in f:
				m = re.search('^fontfile\\s*=\\s*"(.+)"$', line)
				if m is not None:
					font_url = m.group(1)
				m = re.search('^repo\\s*=\\s*"(.+)"$', line)
				if m is not None:
					repo_url = m.group(1)
				m = re.search('^webpage\\s*=\\s*"(.+)"$', line)
				if m is not None:
					webpage_url = m.group(1)
		if font_url is not None:
			try:
				font_path = acquire(font_url, 'local')
				with ttf_file(font_path) as ttf:
					name = ttf.name(False)
				yield (name, font_path, webpage_url if webpage_url is not None else repo_url)
			except Exception as e:
				print('FAILED READ: ' + font_url + ': ' + str(e))
