#!/usr/bin/env python

class BitSet:
	def __init__(self, pivot=8):
		self.pivot = pivot
		self.mask = (1 << pivot) - 1
		self.bits = {}

	def get(self, i):
		k = i >> self.pivot
		if k in self.bits:
			m = 1 << (i & self.mask)
			if self.bits[k] & m:
				return True
		return False

	def getAny(self, i1, i2):
		k1 = i1 >> self.pivot
		k2 = i2 >> self.pivot
		if k1 == k2:
			if k1 in self.bits:
				i1 &= self.mask
				i2 &= self.mask
				m = ((1 << (i2 - i1 + 1)) - 1) << i1
				if self.bits[k1] & m:
					return True
			return False
		else:
			if k1 in self.bits:
				i1 &= self.mask
				m = ((1 << (self.mask - i1 + 1)) - 1) << i1
				if self.bits[k1] & m:
					return True
			if k2 in self.bits:
				i2 &= self.mask
				m = ((1 << (i2 + 1)) - 1)
				if self.bits[k2] & m:
					return True
			for k in range(k1 + 1, k2):
				if k in self.bits and self.bits[k]:
					return True
			return False

	def set(self, i):
		k = i >> self.pivot
		m = 1 << (i & self.mask)
		if k in self.bits:
			self.bits[k] |= m
		else:
			self.bits[k] = m
		return self

	def clear(self, i):
		k = i >> self.pivot
		if k in self.bits:
			m = 1 << (i & self.mask)
			if self.bits[k] & m:
				self.bits[k] ^= m
		return self

	def update(self, b):
		for k in b.bits:
			if k in self.bits:
				self.bits[k] |= b.bits[k]
			else:
				self.bits[k] = b.bits[k]
		return self

	def popcount(self):
		count = 0
		for k in self.bits:
			count += bin(self.bits[k]).count('1')
		return count

	def popcountBetween(self, i1, i2):
		k1 = i1 >> self.pivot
		k2 = i2 >> self.pivot
		if k1 == k2:
			if k1 in self.bits:
				i1 &= self.mask
				i2 &= self.mask
				m = ((1 << (i2 - i1 + 1)) - 1) << i1
				return bin(self.bits[k1] & m).count('1')
			return 0
		else:
			count = 0
			if k1 in self.bits:
				i1 &= self.mask
				m = ((1 << (self.mask - i1 + 1)) - 1) << i1
				count += bin(self.bits[k1] & m).count('1')
			if k2 in self.bits:
				i2 &= self.mask
				m = ((1 << (i2 + 1)) - 1)
				count += bin(self.bits[k2] & m).count('1')
			for k in range(k1 + 1, k2):
				if k in self.bits:
					count += bin(self.bits[k]).count('1')
			return count

def bitset_test():
	def check(t):
		print("PASS" if t else "FAIL")
	b = BitSet()
	b.set(10)
	b.set(20)
	b.set(30)
	check(b.get(10))
	check(b.get(20))
	check(b.get(30))
	check(not b.get(9))
	check(not b.get(11))
	check(not b.get(19))
	check(not b.get(21))
	check(not b.get(29))
	check(not b.get(31))
	check(b.getAny(10, 20))
	check(b.getAny(10, 19))
	check(b.getAny(11, 20))
	check(not b.getAny(11, 19))
	check(b.getAny(10, 30))
	check(b.getAny(10, 29))
	check(b.getAny(11, 30))
	check(b.getAny(11, 29))
	check(b.popcount() == 3)
	check(b.popcountBetween(10, 20) == 2)
	check(b.popcountBetween(10, 19) == 1)
	check(b.popcountBetween(11, 20) == 1)
	check(b.popcountBetween(11, 19) == 0)
	check(b.popcountBetween(10, 30) == 3)
	check(b.popcountBetween(10, 29) == 2)
	check(b.popcountBetween(11, 30) == 2)
	check(b.popcountBetween(11, 29) == 1)
	b = BitSet()
	b.set(1000)
	b.set(2000)
	b.set(3000)
	check(b.get(1000))
	check(b.get(2000))
	check(b.get(3000))
	check(not b.get(999))
	check(not b.get(1001))
	check(not b.get(1999))
	check(not b.get(2001))
	check(not b.get(2999))
	check(not b.get(3001))
	check(b.getAny(1000, 2000))
	check(b.getAny(1000, 1999))
	check(b.getAny(1001, 2000))
	check(not b.getAny(1001, 1999))
	check(b.getAny(1000, 3000))
	check(b.getAny(1000, 2999))
	check(b.getAny(1001, 3000))
	check(b.getAny(1001, 2999))
	check(b.popcount() == 3)
	check(b.popcountBetween(1000, 2000) == 2)
	check(b.popcountBetween(1000, 1999) == 1)
	check(b.popcountBetween(1001, 2000) == 1)
	check(b.popcountBetween(1001, 1999) == 0)
	check(b.popcountBetween(1000, 3000) == 3)
	check(b.popcountBetween(1000, 2999) == 2)
	check(b.popcountBetween(1001, 3000) == 2)
	check(b.popcountBetween(1001, 2999) == 1)

if __name__ == '__main__':
	bitset_test()
