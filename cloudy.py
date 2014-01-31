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

def inthash(prehash):
	return int(hashlib.sha1(prehash).hexdigest(), 16)

def randhash(prehash):
	random.seed(prehash)
	return random.randrange(1000000)

class Cloud(object):
	def __init__(self, hashfn = inthash, seed = 0, cloud_prob=1/100., maxhash = math.pow(16, 40)):
		self.hashfn = hashfn
		self.maxhash = maxhash
		self.seed = seed
		self.seedhash = self.hashfn(str(seed))
		self.cloud_prob = cloud_prob
		self.cloud_hashcap = self.maxhash*self.cloud_prob

	def pointhash(self, x, y, mod=""):
		return self.hashfn(str(int(x))+'x'+str(int(y))+mod)

	def checkcloud(self, hashval = None, x = None, y = None):
		if hashval is None:
			if x is None and y is None:
				raise Exception
			else:
				hashval = self.pointhash(x, y)
				# newhash(hashval)

		return abs(hashval-self.seedhash) < self.cloud_hashcap

	def cloudbase(self, hashval = None, x = None, y = None):
		if hashval is None:
			if x is None and y is None:
				raise Exception
			else:
				hashval = self.pointhash(x, y)
		hashno = abs(hashval-self.seedhash)

		return math.log((hashno/self.cloud_hashcap*(1-1/math.e))+(1/math.e))+1

	def cloudrad(self, hashval = None, x = None, y = None):
		if hashval is None:
			if x is None and y is None:
				raise Exception
			else:
				hashval = self.pointhash(x, y, "rad")

		# print (hashval/self.maxhash)
		return 24.*hashval/self.maxhash