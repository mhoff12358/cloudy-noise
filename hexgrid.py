import math, functools, itertools, cloudy

class HexGrid(object):
	def __init__(self, game, hexside = 15, xsize = 360, ysize = 180):
		self.game = game

		self.hexside = float(hexside)
		self.xsize = xsize
		self.ysize = ysize

		#Heights are stored [y][x]
		self.heights = list()
		for i in range(self.ysize):
			newcol = list()
			for j in range(self.xsize):
				if cloudy.checkcloud(i, j, 0):
					newcol.append(Height(1))
				else:
					newcol.append(Height(0))
				# newcol.append(Height(float(i+j)/(self.ysize+self.xsize)))
			self.heights.append(newcol)

	def retrieve_height(self, x, y):
		return self.heights[y][x]

	def retrieve_strip(self, lower_y):
		itertools.zip(self.heights[lower_y], self.heights[lower_y+1])


class Height(object):
	def __init__(self, start_height):
		self.actual_height = start_height