import math, functools, itertools, cloudy

class HexGrid(object):
	def __init__(self, game, hexside = 15, xsize = 240, ysize = 120):
		self.game = game

		self.hexside = float(hexside)
		self.xsize = xsize
		self.ysize = ysize

		self.cloud = cloudy.Cloud()

		#Heights are stored [y][x]
		self.heights = list()
		for y in range(self.ysize):
			newcol = list()
			for x in range(self.xsize):
				newheight = Height(0)
				newcol.append(newheight)
			self.heights.append(newcol)

		for y in range(self.ysize):
			for x in range(self.xsize):
				if self.cloud.checkcloud(x=x, y=y):
					base = self.cloud.cloudbase(x=x, y=y)
					rad = self.cloud.cloudrad(x=x, y=y)
					for px in range(max(int(x-rad), 0), min(int(x+rad+1), self.xsize)):
						for py in range(max(int(rad-y), 0), min(int(rad+y+1), self.ysize)):
							dist = math.sqrt(math.pow(x-px,2)+math.pow(y-py,2))
							if dist < rad:
								self.retrieve_height(px, py).apply_raise(math.pow((rad-dist)/rad, 2)*base)
		total = 0
		for x in range(self.xsize):
			for y in range(self.ysize):
				total += self.retrieve_height(x, y).actual_height/(120*240)
		print total

	def retrieve_height(self, x, y):
		return self.heights[y][x]


class Height(object):
	def __init__(self, start_height):
		self.actual_height = start_height

	def apply_raise(self, raise_percent):
		self.actual_height = self.actual_height+((1-self.actual_height)*raise_percent)