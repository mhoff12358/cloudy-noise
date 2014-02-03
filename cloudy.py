import hashlib, math, random
hashcap = math.pow(16, 33)/300 #probability that a given hashvalue is a cloud point

minhashval = None
maxhashval = -1

def newhash(val):
	global minhashval, maxhashval
	newval = False
	if minhashval is None:
		minhashval = val
		newval = True
	if val < minhashval:
		minhashval = val
		newval = True
	if val > maxhashval:
		maxhashval = val
		newval = True
	if newval:
		print minhashval, maxhashval

class HashFn(object):
	def __init__(self, hashfn, maxhash):
		self.hashfn = hashfn
		self.maxhash = maxhash

	def compute(self, val):
		return self.hashfn(val)

inthash = HashFn(lambda x: int(hashlib.sha1(x).hexdigest(), 16), math.pow(16, 40))
randhash = HashFn(lambda x: (random.seed(prehash), random.randrange(100000))[1], 100000)

def hashpoint(mod=""):
	def wrap(f):
		def newf(self, hashval = None, x = None, y = None, *args, **kwargs):
			if hashval is None:
				if x is None or y is None:
					raise Exception
				else:
					hashval = self.pointhash(x, y, mod)
			return f(self, hashval=hashval, *args, **kwargs)
		return newf
	return wrap

class CloudGrid(object):
	def __init__(self, game, size = (240, 120), hashfn = inthash, seed = 0, cloud_prob=1/100., max_radius=24.):
		self.game = game

		self.hashfn = hashfn
		self.seed = seed
		self.seedhash = self.hashfn.compute(str(seed))
		self.cloud_prob = cloud_prob
		self.cloud_hashcap = self.hashfn.maxhash*self.cloud_prob
		self.max_radius = max_radius

		self.height_add_fn = lambda x, y: x+(1-x)*y
		self.distance_fn = lambda dist, rad: math.pow((rad-dist)/rad, 2)

		self.heights = []
		self.size = size

		#############
		#Stuff used to internal tracking/stats, not actual output data
		self.centers = []
		self.hist = []
		for i in range(self.game.view.width/5):
			self.hist.append(0)
		#############

		self.compute_cloud()

	def pointhash(self, x, y, mod=""):
		return self.hashfn.compute(str(int(x))+'x'+str(int(y))+mod)

	@hashpoint()
	def check_point(self, hashval = None, x = None, y = None):
		return abs(hashval-self.seedhash) < self.cloud_hashcap

	@hashpoint()
	def point_height(self, hashval = None, x = None, y = None):
		return math.log((abs(hashval-self.seedhash)/self.cloud_hashcap*(1-1/math.e))+(1/math.e))+1

	@hashpoint("rad")
	def point_rad(self, hashval = None, x = None, y = None):
		return self.max_radius*hashval/self.hashfn.maxhash

	def height_finalize_fn(self, height):
		############
		self.hist[int(height*len(self.hist))] += 1
		############
		return height

	def compute_cloud(self):
		self.heights = []
		for x in range(self.size[0]):
			newrow = []
			for y in range(self.size[1]):
				newrow.append(0.0)
			self.heights.append(newrow)

		self.centers = []
		for x in range(self.size[0]):
			newrow = []
			for y in range(self.size[1]):
				newrow.append(False)
			self.centers.append(newrow)
			
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				if self.check_point(x=x, y=y):
					self.centers[x][y] = True
					base = self.point_height(x=x, y=y)
					rad = self.point_rad(x=x, y=y)
					for px in range(max(int(x-rad), 0), min(int(x+rad+1), self.size[0])):
						for py in range(max(int(rad-y), 0), min(int(rad+y+1), self.size[1])):
							dist = math.sqrt(math.pow(x-px,2)+math.pow(y-py,2))
							if dist < rad:
								self.heights[px][py] = self.height_add_fn(self.heights[px][py], self.distance_fn(dist, rad)*base)

		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.heights[x][y] = self.height_finalize_fn(self.heights[x][y])

	def retrieve_center(self, x, y):
		return self.centers[x][y]

	def retrieve_height(self, x, y):
		return self.heights[x][y]