#!/usr/bin/env python

def plane_name(p):
	if p == 0:
		return 'Basic Multilingual Plane (BMP)'
	if p == 1:
		return 'Supplementary Multilingual Plane (SMP)'
	if p == 2:
		return 'Supplementary Ideographic Plane (SIP)'
	if p == 3:
		return 'Tertiary Ideographic Plane (TIP)'
	if p == 14:
		return 'Supplementary Special-Purpose Plane (SSP)'
	if p == 15:
		return 'Supplementary Private Use Area-A'
	if p == 16:
		return 'Supplementary Private Use Area-B'
	return 'Plane ' + str(p)

general_category = {
	'Cc': 'Control Character',
	'Cf': 'Format Character',
	'Cn': 'Unassigned',
	'Co': 'Private Use',
	'Cs': 'Surrogate',
	'Ll': 'Lowercase Letter',
	'Lm': 'Modifier Letter',
	'Lo': 'Other Letter',
	'Lt': 'Titlecase Letter',
	'Lu': 'Uppercase Letter',
	'Mc': 'Spacing Combining Mark',
	'Me': 'Enclosing Combining Mark',
	'Mn': 'Non-Spacing Combining Mark',
	'Nd': 'Decimal Digit',
	'Nl': 'Letterlike Number',
	'No': 'Other Number',
	'Pc': 'Connecting Punctuation',
	'Pd': 'Dash Punctuation',
	'Pe': 'Closing Punctuation',
	'Pf': 'Final Quotation Mark',
	'Pi': 'Initial Quotation Mark',
	'Po': 'Other Punctuation',
	'Ps': 'Opening Punctuation',
	'Sc': 'Currency Symbol',
	'Sk': 'Modifier Symbol',
	'Sm': 'Math Symbol',
	'So': 'Other Symbol',
	'Zl': 'Line Separator',
	'Zp': 'Paragraph Separator',
	'Zs': 'Space Separator',
}

combining_class = {
	'0': 'Spacing and Enclosing Marks',
	'1': 'Overlay',
	'7': 'Nukta',
	'8': 'Kana Voicing',
	'9': 'Virama',
	'200': 'Attached Below Left',
	'202': 'Attached Below',
	'204': 'Attached Below Right',
	'208': 'Attached Left',
	'210': 'Attached Right',
	'212': 'Attached Above Left',
	'214': 'Attached Above',
	'216': 'Attached Above Right',
	'218': 'Below Left',
	'220': 'Below',
	'222': 'Below Right',
	'224': 'Left',
	'226': 'Right',
	'228': 'Above Left',
	'230': 'Above',
	'232': 'Above Right',
	'233': 'Double Below',
	'234': 'Double Above',
	'240': 'Greek Iota Subscript',
}

bidi_class = {
	'AL': 'Arabic Letter',
	'AN': 'Arabic Number',
	'B': 'Paragraph Separator',
	'BN': 'Boundary-Neutral',
	'CS': 'Common Separator',
	'EN': 'European Number',
	'ES': 'European Separator',
	'ET': 'European Terminator',
	'FSI': 'First Strong Isolate',
	'L': 'Left-to-Right',
	'LRE': 'Left-to-Right Embedding',
	'LRI': 'Left-to-Right Isolate',
	'LRO': 'Left-to-Right Override',
	'NSM': 'Non-Spacing Mark',
	'ON': 'Neutral',
	'PDF': 'Pop Directional Format',
	'PDI': 'Pop Directional Isolate',
	'R': 'Right-to-Left',
	'RLE': 'Right-to-Left Embedding',
	'RLI': 'Right-to-Left Isolate',
	'RLO': 'Right-to-Left Override',
	'S': 'Segment Separator',
	'WS': 'Whitespace',
}

decomposition_tag = {
	'circle': 'Encircled Form',
	'compat': 'Compatibility Character',
	'final': 'Final Presentation Form',
	'font': 'Font Variant',
	'fraction': 'Vulgar Fraction',
	'initial': 'Initial Presentation Form',
	'isolated': 'Isolated Presentation Form',
	'medial': 'Medial Presentation Form',
	'narrow': 'Narrow (Hankaku) Form',
	'noBreak': 'No-Break Space or Hyphen',
	'small': 'Small Variant Form',
	'square': 'Squared Form',
	'sub': 'Subscript Form',
	'super': 'Superscript Form',
	'vertical': 'Vertical Presentation Form',
	'wide': 'Wide (Zenkaku) Form',
}

def char_to_utf8(cp):
	if cp < 0:
		return None
	elif cp < 0x80:
		return [cp]
	elif cp < 0x800:
		return [0xC0 | (cp >> 6),
		        0x80 | (cp & 0x3F)]
	elif cp < 0x10000:
		return [0xE0 | (cp >> 12),
		        0x80 | ((cp >> 6) & 0x3F),
		        0x80 | (cp & 0x3F)]
	elif cp < 0x110000:
		return [0xF0 | (cp >> 18),
		        0x80 | ((cp >> 12) & 0x3F),
		        0x80 | ((cp >> 6) & 0x3F),
		        0x80 | (cp & 0x3F)]
	else:
		return None

def char_to_utf16(cp):
	if cp < 0:
		return None
	elif cp < 0x10000:
		return [cp]
	elif cp < 0x110000:
		return [0xD800 | ((cp - 0x10000) >> 10),
		        0xDC00 | ((cp - 0x10000) & 0x3FF)]
	else:
		return None

def hex_dump(a, p=2, le=False):
	b = []
	for i in a:
		if p > 6 and not le:
			b.append('%02X' % ((i >> 24) & 0xFF))
		if p > 4 and not le:
			b.append('%02X' % ((i >> 16) & 0xFF))
		if p > 2 and not le:
			b.append('%02X' % ((i >>  8) & 0xFF))
		b.append('%02X' % (i & 0xFF))
		if p > 2 and le:
			b.append('%02X' % ((i >>  8) & 0xFF))
		if p > 4 and le:
			b.append('%02X' % ((i >> 16) & 0xFF))
		if p > 6 and le:
			b.append('%02X' % ((i >> 24) & 0xFF))
	return ' '.join(b)
