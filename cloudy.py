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
	return int(hashlib.md5(prehash).hexdigest(), 16)

def randhash(prehash):
	random.seed(prehash)
	return random.randrange(1000000)

class Cloud(object):
	def __init__(self, hashfn = inthash, seed = 0, cloud_prob=1/300., maxhash = math.pow(16, 33)):
		self.hashfn = hashfn
		self.seed = seed
		self.seedhash = self.hashfn(str(seed))
		self.cloud_prob = cloud_prob
		self.cloud_hashcap = maxhash*self.cloud_prob
		print self.cloud_hashcap

	def pointhash(self, x, y):
		return self.hashfn(str(int(x))+'x'+str(int(y)))

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
				newhash(hashval)
		hashno = abs(hashval-self.seedhash)

		print "A:", math.log(hashval*(math.exp(2.7)-1)+self.cloud_hashcap)
		print "B:", math.log(self.cloud_hashcap)
		print "C:", (math.log(hashval*(math.exp(2.7)-1)+self.cloud_hashcap)-math.log(self.cloud_hashcap))/.9

		return (math.log(hashno*(math.exp(2.7)-1)+self.cloud_hashcap)-math.log(self.cloud_hashcap))/.9

340265238700852410594329701508548580617