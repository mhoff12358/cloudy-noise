import math, functools, itertools, cloudy

class HexGrid(object):
	def __init__(self, game, hexside = 15, xsize = 180, ysize = 90):
		self.game = game

		self.hexside = float(hexside)
		self.xsize = xsize
		self.ysize = ysize

		self.cloud = cloudy.Cloud()

		#Heights are stored [y][x]
		self.heights = list()
		for i in range(self.ysize):
			newcol = list()
			for j in range(self.xsize):
				if self.cloud.checkcloud(x=2*i-j%2, y=2*j):
					newcol.append(Height(self.cloud.cloudbase(x=2*i-j%2, y=2*j)))
					# newcol.append(Height(1))
				else:
					newcol.append(Height(0))
			self.heights.append(newcol)

	def retrieve_height(self, x, y):
		return self.heights[y][x]

	def retrieve_strip(self, lower_y):
		itertools.zip(self.heights[lower_y], self.heights[lower_y+1])


class Height(object):
	def __init__(self, start_height):
		self.actual_height = start_height