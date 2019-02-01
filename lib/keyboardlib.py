#!/usr/bin/env python

def dict_merge(*dicts):
	result = {}
	for d in dicts:
		result.update(d)
	return result

keystroke_us_ascii = {
	0x0001: 'Ctrl-A',
	0x0002: 'Ctrl-B',
	0x0003: 'Ctrl-C',
	0x0004: 'Ctrl-D',
	0x0005: 'Ctrl-E',
	0x0006: 'Ctrl-F',
	0x0007: 'Ctrl-G',
	0x0008: 'Ctrl-H',
	0x0009: 'Ctrl-I',
	0x000A: 'Ctrl-J',
	0x000B: 'Ctrl-K',
	0x000C: 'Ctrl-L',
	0x000D: 'Ctrl-M',
	0x000E: 'Ctrl-N',
	0x000F: 'Ctrl-O',
	0x0010: 'Ctrl-P',
	0x0011: 'Ctrl-Q',
	0x0012: 'Ctrl-R',
	0x0013: 'Ctrl-S',
	0x0014: 'Ctrl-T',
	0x0015: 'Ctrl-U',
	0x0016: 'Ctrl-V',
	0x0017: 'Ctrl-W',
	0x0018: 'Ctrl-X',
	0x0019: 'Ctrl-Y',
	0x001A: 'Ctrl-Z',
	0x001B: 'Ctrl-[',
	0x001C: 'Ctrl-\\',
	0x001D: 'Ctrl-]',
	0x001E: 'Ctrl-6',
	0x001F: 'Ctrl--',
	0x0020: 'Space',
	0x0021: 'Shift-1',
	0x0022: 'Shift-\'',
	0x0023: 'Shift-3',
	0x0024: 'Shift-4',
	0x0025: 'Shift-5',
	0x0026: 'Shift-7',
	0x0027: '\'',
	0x0028: 'Shift-9',
	0x0029: 'Shift-0',
	0x002A: 'Shift-8',
	0x002B: 'Shift-=',
	0x002C: ',',
	0x002D: '-',
	0x002E: '.',
	0x002F: '/',
	0x0030: '0',
	0x0031: '1',
	0x0032: '2',
	0x0033: '3',
	0x0034: '4',
	0x0035: '5',
	0x0036: '6',
	0x0037: '7',
	0x0038: '8',
	0x0039: '9',
	0x003A: 'Shift-;',
	0x003B: ';',
	0x003C: 'Shift-,',
	0x003D: '=',
	0x003E: 'Shift-.',
	0x003F: 'Shift-/',
	0x0040: 'Shift-2',
	0x0041: 'Shift-A',
	0x0042: 'Shift-B',
	0x0043: 'Shift-C',
	0x0044: 'Shift-D',
	0x0045: 'Shift-E',
	0x0046: 'Shift-F',
	0x0047: 'Shift-G',
	0x0048: 'Shift-H',
	0x0049: 'Shift-I',
	0x004A: 'Shift-J',
	0x004B: 'Shift-K',
	0x004C: 'Shift-L',
	0x004D: 'Shift-M',
	0x004E: 'Shift-N',
	0x004F: 'Shift-O',
	0x0050: 'Shift-P',
	0x0051: 'Shift-Q',
	0x0052: 'Shift-R',
	0x0053: 'Shift-S',
	0x0054: 'Shift-T',
	0x0055: 'Shift-U',
	0x0056: 'Shift-V',
	0x0057: 'Shift-W',
	0x0058: 'Shift-X',
	0x0059: 'Shift-Y',
	0x005A: 'Shift-Z',
	0x005B: '[',
	0x005C: '\\',
	0x005D: ']',
	0x005E: 'Shift-6',
	0x005F: 'Shift--',
	0x0060: '`',
	0x0061: 'A',
	0x0062: 'B',
	0x0063: 'C',
	0x0064: 'D',
	0x0065: 'E',
	0x0066: 'F',
	0x0067: 'G',
	0x0068: 'H',
	0x0069: 'I',
	0x006A: 'J',
	0x006B: 'K',
	0x006C: 'L',
	0x006D: 'M',
	0x006E: 'N',
	0x006F: 'O',
	0x0070: 'P',
	0x0071: 'Q',
	0x0072: 'R',
	0x0073: 'S',
	0x0074: 'T',
	0x0075: 'U',
	0x0076: 'V',
	0x0077: 'W',
	0x0078: 'X',
	0x0079: 'Y',
	0x007A: 'Z',
	0x007B: 'Shift-[',
	0x007C: 'Shift-\\',
	0x007D: 'Shift-]',
	0x007E: 'Shift-`',
	0x007F: 'Del',
}

keystroke_mac_us = dict_merge(keystroke_us_ascii, {
	0x00A0: 'Option-Space',
	0x00A1: 'Option-1',
	0x00A2: 'Option-4',
	0x00A3: 'Option-3',
	0x00A5: 'Option-Y',
	0x00A7: 'Option-6',
	0x00A8: 'Option-Shift-U',
	0x00A9: 'Option-G',
	0x00AA: 'Option-9',
	0x00AB: 'Option-\\',
	0x00AC: 'Option-L',
	0x00AE: 'Option-R',
	0x00AF: 'Option-Shift-,',
	0x00B0: 'Option-Shift-8',
	0x00B1: 'Option-Shift-=',
	0x00B4: 'Option-Shift-E',
	0x00B5: 'Option-M',
	0x00B6: 'Option-7',
	0x00B7: 'Option-Shift-9',
	0x00B8: 'Option-Shift-Z',
	0x00BA: 'Option-0',
	0x00BB: 'Option-Shift-\\',
	0x00BF: 'Option-Shift-/',
	0x00C0: 'Option-`, Shift-A',
	0x00C1: 'Option-E, Shift-A',
	0x00C2: 'Option-I, Shift-A',
	0x00C3: 'Option-N, Shift-A',
	0x00C4: 'Option-U, Shift-A',
	0x00C5: 'Option-Shift-A',
	0x00C6: 'Option-Shift-\'',
	0x00C7: 'Option-Shift-C',
	0x00C8: 'Option-`, Shift-E',
	0x00C9: 'Option-E, Shift-E',
	0x00CA: 'Option-I, Shift-E',
	0x00CB: 'Option-U, Shift-E',
	0x00CC: 'Option-`, Shift-I',
	0x00CD: 'Option-E, Shift-I',
	0x00CE: 'Option-I, Shift-I',
	0x00CF: 'Option-U, Shift-I',
	0x00D1: 'Option-N, Shift-N',
	0x00D2: 'Option-`, Shift-O',
	0x00D3: 'Option-E, Shift-O',
	0x00D4: 'Option-I, Shift-O',
	0x00D5: 'Option-N, Shift-O',
	0x00D6: 'Option-U, Shift-O',
	0x00D8: 'Option-Shift-O',
	0x00D9: 'Option-`, Shift-U',
	0x00DA: 'Option-E, Shift-U',
	0x00DB: 'Option-I, Shift-U',
	0x00DC: 'Option-U, Shift-U',
	0x00DF: 'Option-S',
	0x00E0: 'Option-`, A',
	0x00E1: 'Option-E, A',
	0x00E2: 'Option-I, A',
	0x00E3: 'Option-N, A',
	0x00E4: 'Option-U, A',
	0x00E5: 'Option-A',
	0x00E6: 'Option-\'',
	0x00E7: 'Option-C',
	0x00E8: 'Option-`, E',
	0x00E9: 'Option-E, E',
	0x00EA: 'Option-I, E',
	0x00EB: 'Option-U, E',
	0x00EC: 'Option-`, I',
	0x00ED: 'Option-E, I',
	0x00EE: 'Option-I, I',
	0x00EF: 'Option-U, I',
	0x00F1: 'Option-N, N',
	0x00F2: 'Option-`, O',
	0x00F3: 'Option-E, O',
	0x00F4: 'Option-I, O',
	0x00F5: 'Option-N, O',
	0x00F6: 'Option-U, O',
	0x00F7: 'Option-/',
	0x00F8: 'Option-O',
	0x00F9: 'Option-`, U',
	0x00FA: 'Option-E, U',
	0x00FB: 'Option-I, U',
	0x00FC: 'Option-U, U',
	0x00FF: 'Option-U, Y',
	0x0131: 'Option-Shift-B',
	0x0152: 'Option-Shift-Q',
	0x0153: 'Option-Q',
	0x0178: 'Option-U, Shift-Y',
	0x0192: 'Option-F',
	0x02C6: 'Option-Shift-I',
	0x02C7: 'Option-Shift-T',
	0x02D8: 'Option-Shift-.',
	0x02D9: 'Option-H',
	0x02DA: 'Option-K',
	0x02DB: 'Option-Shift-X',
	0x02DC: 'Option-Shift-N',
	0x02DD: 'Option-Shift-G',
	0x03A9: 'Option-Z',
	0x03C0: 'Option-P',
	0x2013: 'Option--',
	0x2014: 'Option-Shift--',
	0x2018: 'Option-]',
	0x2019: 'Option-Shift-]',
	0x201A: 'Option-Shift-0',
	0x201C: 'Option-[',
	0x201D: 'Option-Shift-[',
	0x201E: 'Option-Shift-W',
	0x2020: 'Option-T',
	0x2021: 'Option-Shift-7',
	0x2022: 'Option-8',
	0x2026: 'Option-;',
	0x2030: 'Option-Shift-R',
	0x2039: 'Option-Shift-3',
	0x203A: 'Option-Shift-4',
	0x2044: 'Option-Shift-1',
	0x20AC: 'Option-Shift-2',
	0x2122: 'Option-2',
	0x2202: 'Option-D',
	0x2206: 'Option-J',
	0x220F: 'Option-Shift-P',
	0x2211: 'Option-W',
	0x221A: 'Option-V',
	0x221E: 'Option-5',
	0x222B: 'Option-B',
	0x2248: 'Option-X',
	0x2260: 'Option-=',
	0x2264: 'Option-,',
	0x2265: 'Option-.',
	0x25CA: 'Option-Shift-V',
	0xF8FF: 'Option-Shift-K',
	0xFB01: 'Option-Shift-5',
	0xFB02: 'Option-Shift-6',
})

keystroke_mac_us_ext = dict_merge(keystroke_us_ascii, {
	0x00A0: 'Option-Space',
	0x00A1: 'Option-1',
	0x00A2: 'Option-4',
	0x00A3: 'Option-3',
	0x00A5: 'Option-Y',
	0x00A7: 'Option-5',
	0x00A8: 'Option-U, Space',
	0x00A9: 'Option-G',
	0x00AA: 'Option-9',
	0x00AB: 'Option-\\',
	0x00AE: 'Option-R',
	0x00AF: 'Option-A, Space',
	0x00B0: 'Option-Shift-8',
	0x00B1: 'Option-Shift-=',
	0x00B4: 'Option-E, Space',
	0x00B6: 'Option-7',
	0x00B7: 'Option-Shift-9',
	0x00B8: 'Option-C, Space',
	0x00BA: 'Option-0',
	0x00BB: 'Option-Shift-\\',
	0x00BF: 'Option-Shift-/',
	0x00C0: 'Option-`, Shift-A',
	0x00C1: 'Option-E, Shift-A',
	0x00C2: 'Option-6, Shift-A',
	0x00C3: 'Option-N, Shift-A',
	0x00C4: 'Option-U, Shift-A',
	0x00C5: 'Option-K, Shift-A',
	0x00C6: 'Option-Shift-\'',
	0x00C7: 'Option-C, Shift-C',
	0x00C8: 'Option-`, Shift-E',
	0x00C9: 'Option-E, Shift-E',
	0x00CA: 'Option-6, Shift-E',
	0x00CB: 'Option-U, Shift-E',
	0x00CC: 'Option-`, Shift-I',
	0x00CD: 'Option-E, Shift-I',
	0x00CE: 'Option-6, Shift-I',
	0x00CF: 'Option-U, Shift-I',
	0x00D0: 'Option-Shift-D',
	0x00D1: 'Option-N, Shift-N',
	0x00D2: 'Option-`, Shift-O',
	0x00D3: 'Option-E, Shift-O',
	0x00D4: 'Option-6, Shift-O',
	0x00D5: 'Option-N, Shift-O',
	0x00D6: 'Option-U, Shift-O',
	0x00D8: 'Option-Shift-O',
	0x00D9: 'Option-`, Shift-U',
	0x00DA: 'Option-E, Shift-U',
	0x00DB: 'Option-6, Shift-U',
	0x00DC: 'Option-U, Shift-U',
	0x00DD: 'Option-E, Shift-Y',
	0x00DE: 'Option-Shift-T',
	0x00DF: 'Option-S',
	0x00E0: 'Option-`, A',
	0x00E1: 'Option-E, A',
	0x00E2: 'Option-6, A',
	0x00E3: 'Option-N, A',
	0x00E4: 'Option-U, A',
	0x00E5: 'Option-K, A',
	0x00E6: 'Option-\'',
	0x00E7: 'Option-C, C',
	0x00E8: 'Option-`, E',
	0x00E9: 'Option-E, E',
	0x00EA: 'Option-6, E',
	0x00EB: 'Option-U, E',
	0x00EC: 'Option-`, I',
	0x00ED: 'Option-E, I',
	0x00EE: 'Option-6, I',
	0x00EF: 'Option-U, I',
	0x00F0: 'Option-D',
	0x00F1: 'Option-N, N',
	0x00F2: 'Option-`, O',
	0x00F3: 'Option-E, O',
	0x00F4: 'Option-6, O',
	0x00F5: 'Option-N, O',
	0x00F6: 'Option-U, O',
	0x00F7: 'Option-/',
	0x00F8: 'Option-O',
	0x00F9: 'Option-`, U',
	0x00FA: 'Option-E, U',
	0x00FB: 'Option-6, U',
	0x00FC: 'Option-U, U',
	0x00FD: 'Option-E, Y',
	0x00FE: 'Option-T',
	0x00FF: 'Option-U, Y',
	0x0100: 'Option-A, Shift-A',
	0x0101: 'Option-A, A',
	0x0102: 'Option-B, Shift-A',
	0x0103: 'Option-B, A',
	0x0104: 'Option-M, Shift-A',
	0x0105: 'Option-M, A',
	0x0106: 'Option-E, Shift-C',
	0x0107: 'Option-E, C',
	0x0108: 'Option-6, Shift-C',
	0x0109: 'Option-6, C',
	0x010A: 'Option-W, Shift-C',
	0x010B: 'Option-W, C',
	0x010C: 'Option-V, Shift-C',
	0x010D: 'Option-V, C',
	0x010E: 'Option-V, Shift-D',
	0x010F: 'Option-V, D',
	0x0110: 'Option-L, Shift-D',
	0x0111: 'Option-L, D',
	0x0112: 'Option-A, Shift-E',
	0x0113: 'Option-A, E',
	0x0114: 'Option-B, Shift-E',
	0x0115: 'Option-B, E',
	0x0116: 'Option-W, Shift-E',
	0x0117: 'Option-W, E',
	0x0118: 'Option-M, Shift-E',
	0x0119: 'Option-M, E',
	0x011A: 'Option-V, Shift-E',
	0x011B: 'Option-V, E',
	0x011C: 'Option-6, Shift-G',
	0x011D: 'Option-6, G',
	0x011E: 'Option-B, Shift-G',
	0x011F: 'Option-B, G',
	0x0120: 'Option-W, Shift-G',
	0x0121: 'Option-W, G',
	0x0122: 'Option-C, Shift-G',
	0x0123: 'Option-C, G',
	0x0124: 'Option-6, Shift-H',
	0x0125: 'Option-6, H',
	0x0126: 'Option-L, Shift-H',
	0x0127: 'Option-L, H',
	0x0128: 'Option-N, Shift-I',
	0x0129: 'Option-N, I',
	0x012A: 'Option-A, Shift-I',
	0x012B: 'Option-A, I',
	0x012C: 'Option-B, Shift-I',
	0x012D: 'Option-B, I',
	0x012E: 'Option-M, Shift-I',
	0x012F: 'Option-M, I',
	0x0130: 'Option-W, Shift-I',
	0x0131: 'Option-W, I',
	0x0134: 'Option-6, Shift-J',
	0x0135: 'Option-6, J',
	0x0136: 'Option-C, Shift-K',
	0x0137: 'Option-C, K',
	0x0138: 'Option-Shift-;, K',
	0x0139: 'Option-E, Shift-L',
	0x013A: 'Option-E, L',
	0x013B: 'Option-C, Shift-L',
	0x013C: 'Option-C, L',
	0x013D: 'Option-V, Shift-L',
	0x013E: 'Option-V, L',
	0x0141: 'Option-L, Shift-L',
	0x0142: 'Option-L, L',
	0x0143: 'Option-E, Shift-N',
	0x0144: 'Option-E, N',
	0x0145: 'Option-C, Shift-N',
	0x0146: 'Option-C, N',
	0x0147: 'Option-V, Shift-N',
	0x0148: 'Option-V, N',
	0x014A: 'Option-Shift-;, Shift-N',
	0x014B: 'Option-Shift-;, N',
	0x014C: 'Option-A, Shift-O',
	0x014D: 'Option-A, O',
	0x014E: 'Option-B, Shift-O',
	0x014F: 'Option-B, O',
	0x0150: 'Option-J, Shift-O',
	0x0151: 'Option-J, O',
	0x0152: 'Option-Shift-Q',
	0x0153: 'Option-Q',
	0x0154: 'Option-E, Shift-R',
	0x0155: 'Option-E, R',
	0x0156: 'Option-C, Shift-R',
	0x0157: 'Option-C, R',
	0x0158: 'Option-V, Shift-R',
	0x0159: 'Option-V, R',
	0x015A: 'Option-E, Shift-S',
	0x015B: 'Option-E, S',
	0x015C: 'Option-6, Shift-S',
	0x015D: 'Option-6, S',
	0x015E: 'Option-C, Shift-S',
	0x015F: 'Option-C, S',
	0x0160: 'Option-V, Shift-S',
	0x0161: 'Option-V, S',
	0x0162: 'Option-C, Shift-T',
	0x0163: 'Option-C, T',
	0x0164: 'Option-V, Shift-T',
	0x0165: 'Option-V, T',
	0x0166: 'Option-L, Shift-T',
	0x0167: 'Option-L, T',
	0x0168: 'Option-N, Shift-U',
	0x0169: 'Option-N, U',
	0x016A: 'Option-A, Shift-U',
	0x016B: 'Option-A, U',
	0x016C: 'Option-B, Shift-U',
	0x016D: 'Option-B, U',
	0x016E: 'Option-K, Shift-U',
	0x016F: 'Option-K, U',
	0x0170: 'Option-J, Shift-U',
	0x0171: 'Option-J, U',
	0x0172: 'Option-M, Shift-U',
	0x0173: 'Option-M, U',
	0x0174: 'Option-6, Shift-W',
	0x0175: 'Option-6, W',
	0x0176: 'Option-6, Shift-Y',
	0x0177: 'Option-6, Y',
	0x0178: 'Option-U, Shift-Y',
	0x0179: 'Option-E, Shift-Z',
	0x017A: 'Option-E, Z',
	0x017B: 'Option-W, Shift-Z',
	0x017C: 'Option-W, Z',
	0x017D: 'Option-V, Shift-Z',
	0x017E: 'Option-V, Z',
	0x017F: 'Option-Shift-;, S',
	0x0180: 'Option-L, B',
	0x0181: 'Option-Shift-., Shift-B',
	0x0184: 'Option-Shift-;, Shift-6',
	0x0185: 'Option-Shift-;, 6',
	0x0186: 'Option-Shift-;, Shift-C',
	0x0187: 'Option-Shift-., Shift-C',
	0x0188: 'Option-Shift-., C',
	0x0189: 'Option-Shift-., Shift-X',
	0x018A: 'Option-Shift-., Shift-D',
	0x018E: 'Option-Shift-;, Shift-E',
	0x018F: 'Option-Shift-;, Shift-A',
	0x0190: 'Option-Shift-;, Shift-3',
	0x0191: 'Option-Shift-., Shift-F',
	0x0192: 'Option-F',
	0x0193: 'Option-Shift-., Shift-G',
	0x0194: 'Option-Shift-;, Shift-G',
	0x0195: 'Option-Shift-;, H',
	0x0196: 'Option-Shift-., Shift-I',
	0x0197: 'Option-L, Shift-I',
	0x0198: 'Option-Shift-., Shift-K',
	0x0199: 'Option-Shift-., K',
	0x019C: 'Option-Shift-;, Shift-M',
	0x019D: 'Option-Shift-., Shift-N',
	0x019E: 'Option-Shift-;, J',
	0x019F: 'Option-L, Shift-O',
	0x01A0: 'Option-I, Shift-O',
	0x01A1: 'Option-I, O',
	0x01A2: 'Option-Shift-;, Shift-Q',
	0x01A3: 'Option-Shift-;, Q',
	0x01A4: 'Option-Shift-., Shift-P',
	0x01A5: 'Option-Shift-., P',
	0x01A6: 'Option-Shift-;, Shift-R',
	0x01A7: 'Option-Shift-;, Shift-2',
	0x01A8: 'Option-Shift-;, 2',
	0x01A9: 'Option-Shift-., Shift-S',
	0x01AC: 'Option-Shift-., Shift-T',
	0x01AD: 'Option-Shift-., T',
	0x01AE: 'Option-Shift-., Shift-R',
	0x01AF: 'Option-I, Shift-U',
	0x01B0: 'Option-I, U',
	0x01B1: 'Option-Shift-;, Shift-U',
	0x01B2: 'Option-Shift-., Shift-U',
	0x01B3: 'Option-Shift-., Shift-Y',
	0x01B4: 'Option-Shift-., Y',
	0x01B5: 'Option-L, Shift-Z',
	0x01B6: 'Option-L, Z',
	0x01B7: 'Option-Shift-;, Shift-Z',
	0x01BC: 'Option-Shift-;, Shift-5',
	0x01BD: 'Option-Shift-;, 5',
	0x01BF: 'Option-Shift-;, W',
	0x01CD: 'Option-V, Shift-A',
	0x01CE: 'Option-V, A',
	0x01CF: 'Option-V, Shift-I',
	0x01D0: 'Option-V, I',
	0x01D1: 'Option-V, Shift-O',
	0x01D2: 'Option-V, O',
	0x01D3: 'Option-V, Shift-U',
	0x01D4: 'Option-V, U',
	0x01D5: 'Option-A, Shift-V',
	0x01D6: 'Option-A, V',
	0x01D7: 'Option-E, Shift-V',
	0x01D8: 'Option-E, V',
	0x01D9: 'Option-V, Shift-V',
	0x01DA: 'Option-V, V',
	0x01DB: 'Option-`, Shift-V',
	0x01DC: 'Option-`, V',
	0x01DD: 'Option-Shift-;, E',
	0x01E2: 'Option-A, Option-Shift-\'',
	0x01E3: 'Option-A, Option-\'',
	0x01E4: 'Option-L, Shift-G',
	0x01E5: 'Option-L, G',
	0x01E6: 'Option-V, Shift-G',
	0x01E7: 'Option-V, G',
	0x01E8: 'Option-V, Shift-K',
	0x01E9: 'Option-V, K',
	0x01EA: 'Option-M, Shift-O',
	0x01EB: 'Option-M, O',
	0x01F0: 'Option-V, J',
	0x01F4: 'Option-E, Shift-G',
	0x01F5: 'Option-E, G',
	0x01F6: 'Option-Shift-;, Shift-H',
	0x01F7: 'Option-Shift-;, Shift-W',
	0x01F8: 'Option-`, Shift-N',
	0x01F9: 'Option-`, N',
	0x01FA: 'Option-E, ',
	0x01FB: 'Option-E, ',
	0x01FC: 'Option-E, Option-Shift-\'',
	0x01FD: 'Option-E, Option-\'',
	0x01FE: 'Option-E, Option-Shift-O',
	0x01FF: 'Option-E, Option-O',
	0x0200: 'Option-Shift-Y, Shift-A',
	0x0201: 'Option-Shift-Y, A',
	0x0202: 'Option-Shift-S, Shift-A',
	0x0203: 'Option-Shift-S, A',
	0x0204: 'Option-Shift-Y, Shift-E',
	0x0205: 'Option-Shift-Y, E',
	0x0206: 'Option-Shift-S, Shift-E',
	0x0207: 'Option-Shift-S, E',
	0x0208: 'Option-Shift-Y, Shift-I',
	0x0209: 'Option-Shift-Y, I',
	0x020A: 'Option-Shift-S, Shift-I',
	0x020B: 'Option-Shift-S, I',
	0x020C: 'Option-Shift-Y, Shift-O',
	0x020D: 'Option-Shift-Y, O',
	0x020E: 'Option-Shift-S, Shift-O',
	0x020F: 'Option-Shift-S, O',
	0x0210: 'Option-Shift-Y, Shift-R',
	0x0211: 'Option-Shift-Y, R',
	0x0212: 'Option-Shift-S, Shift-R',
	0x0213: 'Option-Shift-S, R',
	0x0214: 'Option-Shift-Y, Shift-U',
	0x0215: 'Option-Shift-Y, U',
	0x0216: 'Option-Shift-S, Shift-U',
	0x0217: 'Option-Shift-S, U',
	0x0218: 'Option-P, Shift-S',
	0x0219: 'Option-P, S',
	0x021A: 'Option-P, Shift-T',
	0x021B: 'Option-P, T',
	0x021C: 'Option-Shift-;, Shift-Y',
	0x021D: 'Option-Shift-;, Y',
	0x021E: 'Option-V, Shift-H',
	0x021F: 'Option-V, H',
	0x0220: 'Option-Shift-;, Shift-J',
	0x0222: 'Option-Shift-;, Shift-8',
	0x0223: 'Option-Shift-;, 8',
	0x0224: 'Option-Shift-., Shift-Z',
	0x0225: 'Option-Shift-., Z',
	0x0226: 'Option-W, Shift-A',
	0x0227: 'Option-W, A',
	0x0228: 'Option-C, Shift-E',
	0x0229: 'Option-C, E',
	0x022E: 'Option-W, Shift-O',
	0x022F: 'Option-W, O',
	0x0232: 'Option-A, Shift-Y',
	0x0233: 'Option-A, Y',
	0x0253: 'Option-Shift-., B',
	0x0254: 'Option-Shift-;, C',
	0x0256: 'Option-Shift-., X',
	0x0257: 'Option-Shift-., D',
	0x0259: 'Option-Shift-;, A',
	0x025B: 'Option-Shift-;, 3',
	0x0260: 'Option-Shift-., G',
	0x0263: 'Option-Shift-;, G',
	0x0266: 'Option-Shift-., H',
	0x0268: 'Option-L, I',
	0x0269: 'Option-Shift-., I',
	0x026F: 'Option-Shift-;, M',
	0x0272: 'Option-Shift-., N',
	0x0275: 'Option-L, O',
	0x0280: 'Option-Shift-;, R',
	0x0283: 'Option-Shift-., S',
	0x0288: 'Option-Shift-., R',
	0x0289: 'Option-L, U',
	0x028A: 'Option-Shift-;, U',
	0x028B: 'Option-Shift-., U',
	0x028C: 'Option-Shift-;, V',
	0x0292: 'Option-Shift-;, Z',
	0x0294: 'Option-Shift-., Space',
	0x02A0: 'Option-Shift-., Q',
	0x02B9: 'Option-Shift-;, \'',
	0x02BA: 'Option-Shift-;, Shift-\'',
	0x02BB: 'Option-Shift-;, Option-]',
	0x02BC: 'Option-I, Space',
	0x02BD: 'Option-Shift-;, Option-[',
	0x02C0: 'Option-Z, Space',
	0x02C6: 'Option-6, Space',
	0x02C7: 'Option-V, Space',
	0x02CD: 'Option-H, Space',
	0x02D8: 'Option-B, Space',
	0x02D9: 'Option-W, Space',
	0x02DA: 'Option-K, Space',
	0x02DB: 'Option-M, Space',
	0x02DC: 'Option-N, Space',
	0x02DD: 'Option-J, Space',
	0x0300: 'Option-Shift-`',
	0x0301: 'Option-Shift-E',
	0x0302: 'Option-Shift-6',
	0x0303: 'Option-Shift-N',
	0x0304: 'Option-Shift-A',
	0x0306: 'Option-Shift-B',
	0x0307: 'Option-Shift-W',
	0x0308: 'Option-Shift-U',
	0x0309: 'Option-Shift-Z',
	0x030A: 'Option-Shift-K',
	0x030B: 'Option-Shift-J',
	0x030C: 'Option-Shift-V',
	0x031B: 'Option-Shift-I',
	0x0323: 'Option-Shift-X',
	0x0326: 'Option-Shift-P',
	0x0327: 'Option-Shift-C',
	0x0328: 'Option-Shift-M',
	0x0331: 'Option-Shift-H',
	0x0335: 'Option-Shift-L',
	0x1E02: 'Option-W, Shift-B',
	0x1E03: 'Option-W, B',
	0x1E04: 'Option-X, Shift-B',
	0x1E05: 'Option-X, B',
	0x1E06: 'Option-H, Shift-B',
	0x1E07: 'Option-H, B',
	0x1E0A: 'Option-W, Shift-D',
	0x1E0B: 'Option-W, D',
	0x1E0C: 'Option-X, Shift-D',
	0x1E0D: 'Option-X, D',
	0x1E0E: 'Option-H, Shift-D',
	0x1E0F: 'Option-H, D',
	0x1E10: 'Option-C, Shift-D',
	0x1E11: 'Option-C, D',
	0x1E12: 'Option-Shift-G, Shift-D',
	0x1E13: 'Option-Shift-G, D',
	0x1E18: 'Option-Shift-G, Shift-E',
	0x1E19: 'Option-Shift-G, E',
	0x1E1A: 'Option-Shift-F, Shift-E',
	0x1E1B: 'Option-Shift-F, E',
	0x1E1E: 'Option-W, Shift-F',
	0x1E1F: 'Option-W, F',
	0x1E20: 'Option-A, Shift-G',
	0x1E21: 'Option-A, G',
	0x1E22: 'Option-W, Shift-H',
	0x1E23: 'Option-W, H',
	0x1E24: 'Option-X, Shift-H',
	0x1E25: 'Option-X, H',
	0x1E26: 'Option-U, Shift-H',
	0x1E27: 'Option-U, H',
	0x1E28: 'Option-C, Shift-H',
	0x1E29: 'Option-C, H',
	0x1E2A: 'Option-B, Shift-H',
	0x1E2B: 'Option-B, H',
	0x1E2C: 'Option-Shift-F, Shift-I',
	0x1E2D: 'Option-Shift-F, I',
	0x1E30: 'Option-E, Shift-K',
	0x1E31: 'Option-E, K',
	0x1E32: 'Option-X, Shift-K',
	0x1E33: 'Option-X, K',
	0x1E34: 'Option-H, Shift-K',
	0x1E35: 'Option-H, K',
	0x1E36: 'Option-X, Shift-L',
	0x1E37: 'Option-X, L',
	0x1E3A: 'Option-H, Shift-L',
	0x1E3B: 'Option-H, L',
	0x1E3C: 'Option-Shift-G, Shift-L',
	0x1E3D: 'Option-Shift-G, L',
	0x1E3E: 'Option-E, Shift-M',
	0x1E3F: 'Option-E, M',
	0x1E40: 'Option-W, Shift-M',
	0x1E41: 'Option-W, M',
	0x1E42: 'Option-X, Shift-M',
	0x1E43: 'Option-X, M',
	0x1E44: 'Option-W, Shift-N',
	0x1E45: 'Option-W, N',
	0x1E46: 'Option-X, Shift-N',
	0x1E47: 'Option-X, N',
	0x1E48: 'Option-H, Shift-N',
	0x1E49: 'Option-H, N',
	0x1E4A: 'Option-Shift-G, Shift-N',
	0x1E4B: 'Option-Shift-G, N',
	0x1E54: 'Option-E, Shift-P',
	0x1E55: 'Option-E, P',
	0x1E56: 'Option-W, Shift-P',
	0x1E57: 'Option-W, P',
	0x1E58: 'Option-W, Shift-R',
	0x1E59: 'Option-W, R',
	0x1E5A: 'Option-X, Shift-R',
	0x1E5B: 'Option-X, R',
	0x1E5E: 'Option-H, Shift-R',
	0x1E5F: 'Option-H, R',
	0x1E60: 'Option-W, Shift-S',
	0x1E61: 'Option-W, S',
	0x1E62: 'Option-X, Shift-S',
	0x1E63: 'Option-X, S',
	0x1E6A: 'Option-W, Shift-T',
	0x1E6B: 'Option-W, T',
	0x1E6C: 'Option-X, Shift-T',
	0x1E6D: 'Option-X, T',
	0x1E6E: 'Option-H, Shift-T',
	0x1E6F: 'Option-H, T',
	0x1E70: 'Option-Shift-G, Shift-T',
	0x1E71: 'Option-Shift-G, T',
	0x1E74: 'Option-Shift-F, Shift-U',
	0x1E75: 'Option-Shift-F, U',
	0x1E76: 'Option-Shift-G, Shift-U',
	0x1E77: 'Option-Shift-G, U',
	0x1E7C: 'Option-N, Shift-V',
	0x1E7D: 'Option-N, V',
	0x1E7E: 'Option-X, Shift-V',
	0x1E7F: 'Option-X, V',
	0x1E80: 'Option-`, Shift-W',
	0x1E81: 'Option-`, W',
	0x1E82: 'Option-E, Shift-W',
	0x1E83: 'Option-E, W',
	0x1E84: 'Option-U, Shift-W',
	0x1E85: 'Option-U, W',
	0x1E86: 'Option-W, Shift-W',
	0x1E87: 'Option-W, W',
	0x1E88: 'Option-X, Shift-W',
	0x1E89: 'Option-X, W',
	0x1E8A: 'Option-W, Shift-X',
	0x1E8B: 'Option-W, X',
	0x1E8C: 'Option-U, Shift-X',
	0x1E8D: 'Option-U, X',
	0x1E8E: 'Option-W, Shift-Y',
	0x1E8F: 'Option-W, Y',
	0x1E90: 'Option-6, Shift-Z',
	0x1E91: 'Option-6, Z',
	0x1E92: 'Option-X, Shift-Z',
	0x1E93: 'Option-X, Z',
	0x1E94: 'Option-H, Shift-Z',
	0x1E95: 'Option-H, Z',
	0x1E96: 'Option-H, H',
	0x1E97: 'Option-U, T',
	0x1E98: 'Option-K, W',
	0x1E99: 'Option-K, Y',
	0x1EA0: 'Option-X, Shift-A',
	0x1EA1: 'Option-X, A',
	0x1EA2: 'Option-Z, Shift-A',
	0x1EA3: 'Option-Z, A',
	0x1EB8: 'Option-X, Shift-E',
	0x1EB9: 'Option-X, E',
	0x1EBA: 'Option-Z, Shift-E',
	0x1EBB: 'Option-Z, E',
	0x1EBC: 'Option-N, Shift-E',
	0x1EBD: 'Option-N, E',
	0x1EC8: 'Option-Z, Shift-I',
	0x1EC9: 'Option-Z, I',
	0x1ECA: 'Option-X, Shift-I',
	0x1ECB: 'Option-X, I',
	0x1ECC: 'Option-X, Shift-O',
	0x1ECD: 'Option-X, O',
	0x1ECE: 'Option-Z, Shift-O',
	0x1ECF: 'Option-Z, O',
	0x1EE4: 'Option-X, Shift-U',
	0x1EE5: 'Option-X, U',
	0x1EE6: 'Option-Z, Shift-U',
	0x1EE7: 'Option-Z, U',
	0x1EF2: 'Option-`, Shift-Y',
	0x1EF3: 'Option-`, Y',
	0x1EF4: 'Option-X, Shift-Y',
	0x1EF5: 'Option-X, Y',
	0x1EF6: 'Option-Z, Shift-Y',
	0x1EF7: 'Option-Z, Y',
	0x1EF8: 'Option-N, Shift-Y',
	0x1EF9: 'Option-N, Y',
	0x2013: 'Option--',
	0x2014: 'Option-Shift--',
	0x2018: 'Option-]',
	0x2019: 'Option-Shift-]',
	0x201A: 'Option-Shift-0',
	0x201C: 'Option-[',
	0x201D: 'Option-Shift-[',
	0x201E: 'Option-Shift-,',
	0x2020: 'Option-Shift-5',
	0x2021: 'Option-Shift-7',
	0x2022: 'Option-8',
	0x2026: 'Option-;',
	0x2030: 'Option-Shift-R',
	0x2038: 'Option-Shift-G, Space',
	0x2039: 'Option-Shift-3',
	0x203A: 'Option-Shift-4',
	0x2044: 'Option-Shift-1',
	0x204A: 'Option-Shift-;, 7',
	0x20AC: 'Option-Shift-2',
	0x2116: 'Option-Shift-;, Space',
	0x2122: 'Option-2',
	0x2260: 'Option-=',
	0x2264: 'Option-,',
	0x2265: 'Option-.',
})

keystroke_superlatin = dict_merge(keystroke_us_ascii, {
	0x00A0: 'Alt-Space',
	0x00A1: 'Alt-Shift-1',
	0x00A2: 'Alt-Shift-4',
	0x00A3: 'Alt-Shift-3',
	0x00A4: 'Alt-Shift-X',
	0x00A5: 'Alt-Y',
	0x00A6: 'Alt-Shift-\\',
	0x00A7: 'Alt-W',
	0x00A8: 'Alt-4, Space',
	0x00A9: 'Alt-C',
	0x00AA: 'Alt-Shift-Q',
	0x00AB: 'Alt-Shift-[',
	0x00AC: 'Alt-V',
	0x00AD: 'Alt-Shift-0',
	0x00AE: 'Alt-R',
	0x00AF: 'Alt-0, Space',
	0x00B0: 'Alt-Shift-6',
	0x00B1: 'Alt-Shift-=',
	0x00B2: 'Alt-6, 2',
	0x00B3: 'Alt-6, 3',
	0x00B4: 'Alt-1, Space',
	0x00B5: 'Alt-U',
	0x00B6: 'Alt-Q',
	0x00B7: 'Alt-Shift-9',
	0x00B8: 'Alt-,, Space',
	0x00B9: 'Alt-6, 1',
	0x00BA: 'Alt-Shift-W',
	0x00BB: 'Alt-Shift-]',
	0x00BC: 'Alt-/, 2',
	0x00BD: 'Alt-/, 5',
	0x00BE: 'Alt-/, 8',
	0x00BF: 'Alt-Shift-/',
	0x00C0: 'Alt-`, Shift-A',
	0x00C1: 'Alt-1, Shift-A',
	0x00C2: 'Alt-6, Shift-A',
	0x00C3: 'Alt-9, Shift-A',
	0x00C4: 'Alt-4, Shift-A',
	0x00C5: 'Alt-5, Shift-A',
	0x00C6: 'Alt-Shift-A',
	0x00C7: 'Alt-,, Shift-C',
	0x00C8: 'Alt-`, Shift-E',
	0x00C9: 'Alt-1, Shift-E',
	0x00CA: 'Alt-6, Shift-E',
	0x00CB: 'Alt-4, Shift-E',
	0x00CC: 'Alt-`, Shift-I',
	0x00CD: 'Alt-1, Shift-I',
	0x00CE: 'Alt-6, Shift-I',
	0x00CF: 'Alt-4, Shift-I',
	0x00D0: 'Alt-Shift-D',
	0x00D1: 'Alt-9, Shift-N',
	0x00D2: 'Alt-`, Shift-O',
	0x00D3: 'Alt-1, Shift-O',
	0x00D4: 'Alt-6, Shift-O',
	0x00D5: 'Alt-9, Shift-O',
	0x00D6: 'Alt-4, Shift-O',
	0x00D7: 'Alt-X',
	0x00D8: 'Alt-/, Shift-O',
	0x00D9: 'Alt-`, Shift-U',
	0x00DA: 'Alt-1, Shift-U',
	0x00DB: 'Alt-6, Shift-U',
	0x00DC: 'Alt-4, Shift-U',
	0x00DD: 'Alt-1, Shift-Y',
	0x00DE: 'Alt-Shift-T',
	0x00DF: 'Alt-S',
	0x00E0: 'Alt-`, A',
	0x00E1: 'Alt-1, A',
	0x00E2: 'Alt-6, A',
	0x00E3: 'Alt-9, A',
	0x00E4: 'Alt-4, A',
	0x00E5: 'Alt-5, A',
	0x00E6: 'Alt-A',
	0x00E7: 'Alt-,, C',
	0x00E8: 'Alt-`, E',
	0x00E9: 'Alt-1, E',
	0x00EA: 'Alt-6, E',
	0x00EB: 'Alt-4, E',
	0x00EC: 'Alt-`, I',
	0x00ED: 'Alt-1, I',
	0x00EE: 'Alt-6, I',
	0x00EF: 'Alt-4, I',
	0x00F0: 'Alt-D',
	0x00F1: 'Alt-9, N',
	0x00F2: 'Alt-`, O',
	0x00F3: 'Alt-1, O',
	0x00F4: 'Alt-6, O',
	0x00F5: 'Alt-9, O',
	0x00F6: 'Alt-4, O',
	0x00F7: 'Alt-\\',
	0x00F8: 'Alt-/, O',
	0x00F9: 'Alt-`, U',
	0x00FA: 'Alt-1, U',
	0x00FB: 'Alt-6, U',
	0x00FC: 'Alt-4, U',
	0x00FD: 'Alt-1, Y',
	0x00FE: 'Alt-T',
	0x00FF: 'Alt-4, Y',
	0x0100: 'Alt-0, Shift-A',
	0x0101: 'Alt-0, A',
	0x0102: 'Alt-8, Shift-A',
	0x0103: 'Alt-8, A',
	0x0104: 'Alt-., Shift-A',
	0x0105: 'Alt-., A',
	0x0106: 'Alt-1, Shift-C',
	0x0107: 'Alt-1, C',
	0x0108: 'Alt-6, Shift-C',
	0x0109: 'Alt-6, C',
	0x010A: 'Alt-3, Shift-C',
	0x010B: 'Alt-3, C',
	0x010C: 'Alt-7, Shift-C',
	0x010D: 'Alt-7, C',
	0x010E: 'Alt-7, Shift-D',
	0x010F: 'Alt-7, D',
	0x0110: 'Alt-/, Shift-D',
	0x0111: 'Alt-/, D',
	0x0112: 'Alt-0, Shift-E',
	0x0113: 'Alt-0, E',
	0x0114: 'Alt-8, Shift-E',
	0x0115: 'Alt-8, E',
	0x0116: 'Alt-3, Shift-E',
	0x0117: 'Alt-3, E',
	0x0118: 'Alt-., Shift-E',
	0x0119: 'Alt-., E',
	0x011A: 'Alt-7, Shift-E',
	0x011B: 'Alt-7, E',
	0x011C: 'Alt-6, Shift-G',
	0x011D: 'Alt-6, G',
	0x011E: 'Alt-8, Shift-G',
	0x011F: 'Alt-8, G',
	0x0120: 'Alt-3, Shift-G',
	0x0121: 'Alt-3, G',
	0x0122: 'Alt-,, Shift-G',
	0x0123: 'Alt-,, G',
	0x0124: 'Alt-6, Shift-H',
	0x0125: 'Alt-6, H',
	0x0126: 'Alt-/, Shift-H',
	0x0127: 'Alt-/, H',
	0x0128: 'Alt-9, Shift-I',
	0x0129: 'Alt-9, I',
	0x012A: 'Alt-0, Shift-I',
	0x012B: 'Alt-0, I',
	0x012C: 'Alt-8, Shift-I',
	0x012D: 'Alt-8, I',
	0x012E: 'Alt-., Shift-I',
	0x012F: 'Alt-., I',
	0x0130: 'Alt-3, Shift-I',
	0x0131: 'Alt-3, I',
	0x0131: 'Alt-I',
	0x0132: 'Alt-4, Shift-J',
	0x0133: 'Alt-4, J',
	0x0134: 'Alt-6, Shift-J',
	0x0135: 'Alt-6, J',
	0x0136: 'Alt-,, Shift-K',
	0x0137: 'Alt-,, K',
	0x0138: 'Alt-K',
	0x0139: 'Alt-1, Shift-L',
	0x013A: 'Alt-1, L',
	0x013B: 'Alt-,, Shift-L',
	0x013C: 'Alt-,, L',
	0x013D: 'Alt-7, Shift-L',
	0x013E: 'Alt-7, L',
	0x013F: 'Alt-3, Shift-L',
	0x0140: 'Alt-3, L',
	0x0141: 'Alt-/, Shift-L',
	0x0142: 'Alt-/, L',
	0x0143: 'Alt-1, Shift-N',
	0x0144: 'Alt-1, N',
	0x0145: 'Alt-,, Shift-N',
	0x0146: 'Alt-,, N',
	0x0147: 'Alt-7, Shift-N',
	0x0148: 'Alt-7, N',
	0x0149: 'Alt-N',
	0x014A: 'Alt-Shift-G',
	0x014B: 'Alt-G',
	0x014C: 'Alt-0, Shift-O',
	0x014D: 'Alt-0, O',
	0x014E: 'Alt-8, Shift-O',
	0x014F: 'Alt-8, O',
	0x0150: 'Alt-2, Shift-O',
	0x0151: 'Alt-2, O',
	0x0152: 'Alt-Shift-O',
	0x0153: 'Alt-O',
	0x0154: 'Alt-1, Shift-R',
	0x0155: 'Alt-1, R',
	0x0156: 'Alt-,, Shift-R',
	0x0157: 'Alt-,, R',
	0x0158: 'Alt-7, Shift-R',
	0x0159: 'Alt-7, R',
	0x015A: 'Alt-1, Shift-S',
	0x015B: 'Alt-1, S',
	0x015C: 'Alt-6, Shift-S',
	0x015D: 'Alt-6, S',
	0x015E: 'Alt-,, Shift-S',
	0x015F: 'Alt-,, S',
	0x0160: 'Alt-7, Shift-S',
	0x0161: 'Alt-7, S',
	0x0162: 'Alt-,, Shift-T',
	0x0163: 'Alt-,, T',
	0x0164: 'Alt-7, Shift-T',
	0x0165: 'Alt-7, T',
	0x0166: 'Alt-/, Shift-T',
	0x0167: 'Alt-/, T',
	0x0168: 'Alt-9, Shift-U',
	0x0169: 'Alt-9, U',
	0x016A: 'Alt-0, Shift-U',
	0x016B: 'Alt-0, U',
	0x016C: 'Alt-8, Shift-U',
	0x016D: 'Alt-8, U',
	0x016E: 'Alt-5, Shift-U',
	0x016F: 'Alt-5, U',
	0x0170: 'Alt-2, Shift-U',
	0x0171: 'Alt-2, U',
	0x0172: 'Alt-., Shift-U',
	0x0173: 'Alt-., U',
	0x0174: 'Alt-6, Shift-W',
	0x0175: 'Alt-6, W',
	0x0176: 'Alt-6, Shift-Y',
	0x0177: 'Alt-6, Y',
	0x0178: 'Alt-4, Shift-Y',
	0x0179: 'Alt-1, Shift-Z',
	0x017A: 'Alt-1, Z',
	0x017B: 'Alt-3, Shift-Z',
	0x017C: 'Alt-3, Z',
	0x017D: 'Alt-7, Shift-Z',
	0x017E: 'Alt-7, Z',
	0x017F: 'Alt-Shift-Z',
	0x0180: 'Alt-/, B',
	0x0192: 'Alt-F',
	0x0197: 'Alt-/, Shift-I',
	0x01A0: 'Alt-,, Shift-O',
	0x01A1: 'Alt-,, O',
	0x01AF: 'Alt-,, Shift-U',
	0x01B0: 'Alt-,, U',
	0x01B5: 'Alt-/, Shift-Z',
	0x01B6: 'Alt-/, Z',
	0x01CD: 'Alt-7, Shift-A',
	0x01CE: 'Alt-7, A',
	0x01CF: 'Alt-7, Shift-I',
	0x01D0: 'Alt-7, I',
	0x01D1: 'Alt-7, Shift-O',
	0x01D2: 'Alt-7, O',
	0x01D3: 'Alt-7, Shift-U',
	0x01D4: 'Alt-7, U',
	0x01DD: 'Alt-E',
	0x01E4: 'Alt-/, Shift-G',
	0x01E5: 'Alt-/, G',
	0x01E6: 'Alt-7, Shift-G',
	0x01E7: 'Alt-7, G',
	0x01E8: 'Alt-7, Shift-K',
	0x01E9: 'Alt-7, K',
	0x01EA: 'Alt-., Shift-O',
	0x01EB: 'Alt-., O',
	0x01F0: 'Alt-7, J',
	0x01F4: 'Alt-1, Shift-G',
	0x01F5: 'Alt-1, G',
	0x01F8: 'Alt-`, Shift-N',
	0x01F9: 'Alt-`, N',
	0x0218: 'Alt-., Shift-S',
	0x0219: 'Alt-., S',
	0x021A: 'Alt-., Shift-T',
	0x021B: 'Alt-., T',
	0x021E: 'Alt-7, Shift-H',
	0x021F: 'Alt-7, H',
	0x0226: 'Alt-3, Shift-A',
	0x0227: 'Alt-3, A',
	0x0228: 'Alt-,, Shift-E',
	0x0229: 'Alt-,, E',
	0x022E: 'Alt-3, Shift-O',
	0x022F: 'Alt-3, O',
	0x0232: 'Alt-0, Shift-Y',
	0x0233: 'Alt-0, Y',
	0x0237: 'Alt-3, J',
	0x0237: 'Alt-J',
	0x023A: 'Alt-/, Shift-A',
	0x023B: 'Alt-/, Shift-C',
	0x023C: 'Alt-/, C',
	0x0243: 'Alt-/, Shift-B',
	0x0246: 'Alt-/, Shift-E',
	0x0247: 'Alt-/, E',
	0x0248: 'Alt-/, Shift-J',
	0x0249: 'Alt-/, J',
	0x024C: 'Alt-/, Shift-R',
	0x024D: 'Alt-/, R',
	0x024E: 'Alt-/, Shift-Y',
	0x024F: 'Alt-/, Y',
	0x0268: 'Alt-/, I',
	0x02C6: 'Alt-6, Space',
	0x02C7: 'Alt-7, Space',
	0x02CB: 'Alt-`, Space',
	0x02D8: 'Alt-8, Space',
	0x02D9: 'Alt-3, Space',
	0x02DA: 'Alt-5, Space',
	0x02DB: 'Alt-., Space',
	0x02DC: 'Alt-9, Space',
	0x02DD: 'Alt-2, Space',
	0x0300: 'Alt-`, Alt-Space',
	0x0301: 'Alt-1, Alt-Space',
	0x0302: 'Alt-6, Alt-Space',
	0x0303: 'Alt-9, Alt-Space',
	0x0304: 'Alt-0, Alt-Space',
	0x0306: 'Alt-8, Alt-Space',
	0x0307: 'Alt-3, Alt-Space',
	0x0308: 'Alt-4, Alt-Space',
	0x030A: 'Alt-5, Alt-Space',
	0x030B: 'Alt-2, Alt-Space',
	0x030C: 'Alt-7, Alt-Space',
	0x0327: 'Alt-,, Alt-Space',
	0x0328: 'Alt-., Alt-Space',
	0x03A9: 'Alt-Shift-U',
	0x03C0: 'Alt-P',
	0x1D7D: 'Alt-/, P',
	0x1E02: 'Alt-3, Shift-B',
	0x1E03: 'Alt-3, B',
	0x1E0A: 'Alt-3, Shift-D',
	0x1E0B: 'Alt-3, D',
	0x1E10: 'Alt-,, Shift-D',
	0x1E11: 'Alt-,, D',
	0x1E1E: 'Alt-3, Shift-F',
	0x1E1F: 'Alt-3, F',
	0x1E20: 'Alt-0, Shift-G',
	0x1E21: 'Alt-0, G',
	0x1E22: 'Alt-3, Shift-H',
	0x1E23: 'Alt-3, H',
	0x1E26: 'Alt-4, Shift-H',
	0x1E27: 'Alt-4, H',
	0x1E28: 'Alt-,, Shift-H',
	0x1E29: 'Alt-,, H',
	0x1E30: 'Alt-1, Shift-K',
	0x1E31: 'Alt-1, K',
	0x1E3E: 'Alt-1, Shift-M',
	0x1E3F: 'Alt-1, M',
	0x1E40: 'Alt-3, Shift-M',
	0x1E41: 'Alt-3, M',
	0x1E44: 'Alt-3, Shift-N',
	0x1E45: 'Alt-3, N',
	0x1E54: 'Alt-1, Shift-P',
	0x1E55: 'Alt-1, P',
	0x1E56: 'Alt-3, Shift-P',
	0x1E57: 'Alt-3, P',
	0x1E58: 'Alt-3, Shift-R',
	0x1E59: 'Alt-3, R',
	0x1E60: 'Alt-3, Shift-S',
	0x1E61: 'Alt-3, S',
	0x1E6A: 'Alt-3, Shift-T',
	0x1E6B: 'Alt-3, T',
	0x1E7C: 'Alt-9, Shift-V',
	0x1E7D: 'Alt-9, V',
	0x1E80: 'Alt-`, Shift-W',
	0x1E81: 'Alt-`, W',
	0x1E82: 'Alt-1, Shift-W',
	0x1E83: 'Alt-1, W',
	0x1E84: 'Alt-4, Shift-W',
	0x1E85: 'Alt-4, W',
	0x1E86: 'Alt-3, Shift-W',
	0x1E87: 'Alt-3, W',
	0x1E8A: 'Alt-3, Shift-X',
	0x1E8B: 'Alt-3, X',
	0x1E8C: 'Alt-4, Shift-X',
	0x1E8D: 'Alt-4, X',
	0x1E8E: 'Alt-3, Shift-Y',
	0x1E8F: 'Alt-3, Y',
	0x1E90: 'Alt-6, Shift-Z',
	0x1E91: 'Alt-6, Z',
	0x1E97: 'Alt-4, T',
	0x1E98: 'Alt-5, W',
	0x1E99: 'Alt-5, Y',
	0x1E9E: 'Alt-Shift-S',
	0x1EBC: 'Alt-9, Shift-E',
	0x1EBD: 'Alt-9, E',
	0x1EF2: 'Alt-`, Shift-Y',
	0x1EF3: 'Alt-`, Y',
	0x1EF8: 'Alt-9, Shift-Y',
	0x1EF9: 'Alt-9, Y',
	0x2013: 'Alt--',
	0x2014: 'Alt-Shift--',
	0x2018: 'Alt-;',
	0x2019: 'Alt-\'',
	0x201A: 'Alt-L',
	0x201C: 'Alt-Shift-;',
	0x201D: 'Alt-Shift-\'',
	0x201E: 'Alt-Shift-L',
	0x2020: 'Alt-H',
	0x2021: 'Alt-Shift-H',
	0x2022: 'Alt-Shift-8',
	0x2026: 'Alt-Z',
	0x2030: 'Alt-Shift-5',
	0x2039: 'Alt-[',
	0x203A: 'Alt-]',
	0x203D: 'Alt-Shift-Y',
	0x2044: 'Alt-/, Space',
	0x2070: 'Alt-6, 0',
	0x2074: 'Alt-6, 4',
	0x2075: 'Alt-6, 5',
	0x2076: 'Alt-6, 6',
	0x2077: 'Alt-6, 7',
	0x2078: 'Alt-6, 8',
	0x2079: 'Alt-6, 9',
	0x2080: 'Alt-7, 0',
	0x2081: 'Alt-7, 1',
	0x2082: 'Alt-7, 2',
	0x2083: 'Alt-7, 3',
	0x2084: 'Alt-7, 4',
	0x2085: 'Alt-7, 5',
	0x2086: 'Alt-7, 6',
	0x2087: 'Alt-7, 7',
	0x2088: 'Alt-7, 8',
	0x2089: 'Alt-7, 9',
	0x20AC: 'Alt-Shift-2',
	0x2116: 'Alt-Shift-N',
	0x2117: 'Alt-Shift-C',
	0x2122: 'Alt-M',
	0x2153: 'Alt-/, 3',
	0x2154: 'Alt-/, 7',
	0x215B: 'Alt-/, 1',
	0x215C: 'Alt-/, 4',
	0x215D: 'Alt-/, 6',
	0x215E: 'Alt-/, 9',
	0x215F: 'Alt-/, 0',
	0x2202: 'Alt-B',
	0x2206: 'Alt-Shift-B',
	0x2207: 'Alt-Shift-V',
	0x220F: 'Alt-Shift-P',
	0x2211: 'Alt-Shift-E',
	0x221A: 'Alt-Shift-R',
	0x221E: 'Alt-Shift-7',
	0x222B: 'Alt-Shift-J',
	0x2248: 'Alt-Shift-`',
	0x2260: 'Alt-=',
	0x2264: 'Alt-Shift-,',
	0x2265: 'Alt-Shift-.',
	0x2318: 'Alt-Shift-M',
	0x25CA: 'Alt-Shift-K',
	0x2C63: 'Alt-/, Shift-P',
	0x2C65: 'Alt-/, A',
	0xA740: 'Alt-/, Shift-K',
	0xA741: 'Alt-/, K',
	0xFB01: 'Alt-Shift-I',
	0xFB02: 'Alt-Shift-F',
})