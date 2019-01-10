#!/usr/bin/env python


class rpnCalculator:
	vec = []
	
	def __init__(self, vec):
		self.ident = vec
		
	def pushValue(self, val):
		self.vec.insert(0,val)
		
	def popValue(self):
		b = self.vec.pop(0)
		print "%d" % (b) 
		
	def addsub(self):
		self.vec.insert(0,self.vec.pop(0)+self.vec.pop(0))
		
		
obj1 = rpnCalculator([1, 2, 3, 4, 5])

obj1.popValue

		
		
		
		
