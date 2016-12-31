import json

def readJsonFile(dest):
	with open(dest, 'rb') as f:
		return json.load(f)

def readTxtFile(dest):
	with open(dest, 'rb') as f:
		print f.readlines()

def loadFrequency(dest):
	freq_data = readJsonFile(dest)

	size = 26
	probability = [0 for r in range(size)]
	sum_p = 0.0

	for data in freq_data:
		bg, freq = data, freq_data[data]
		if bg.isalpha():
			probability[ord(bg[0])-ord('a')] = freq
			sum_p += freq

	for idx in range(size):
		probability[idx] /= sum_p

	return probability

def loadBigrams(dest):
	bigram_data = readJsonFile(dest)

	size = 26
	probability = [[0 for r in range(size)] for c in range(size)]
	sum_p = 0.0

	for data in bigram_data:
		bg, freq = data[0], data[1]
		if bg.isalpha():
			probability[ord(bg[0])-ord('a')][ord(bg[1])-ord('a')] = freq
			sum_p += freq

	for r in range(size):
		for c in range(size):
			probability[r][c] /= sum_p

	return probability

def loadTrigram(dest, valid_set):
	trigram = {}
	sum_p = 0.0

	for s in valid_set:
		trigram[s] = set()

	with open(dest, 'rb') as f:
		contents = f.readlines()
		
	for line in contents:
		(tri, freq) = line.rstrip("\n").split(" ")
		if tri.isalpha(): sum_p += int(freq)

	for line in contents:
		(tri, freq) = line.rstrip("\n").split(" ")
		tri = tri.lower()
		if tri.isalpha():
			k, v = tri[0:2], int(freq)/sum_p
			trigram[tri[2]].add((k, v))

	return trigram

def loadDictionary(dest):
	return set(key.lower() for key in readJsonFile(dest))

if __name__ == '__main__':
	valid_set = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
	'o','p','q','r','s','t','u','v','w','x','y','z'}
	dest = "/Users/Gilbert/Downloads/english_trigrams.txt"
	tri = loadTrigram(dest, valid_set)
	for tup in tri['p']:
		print tup