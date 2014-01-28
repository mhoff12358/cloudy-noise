import hashlib, math
hashcap = math.pow(16, 33)/100 #probability that a given hashvalue is a cloud point


def inthash(prehash):
	return int(hashlib.md5(prehash).hexdigest(), 16)

def pointhash(x, y):
	return inthash(str(x)+'x'+str(y))

def checkcloud(x, y, seed):
	return abs(pointhash(x, y)-inthash(seed)) < hashcap