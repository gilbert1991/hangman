import re

def init_dict(dict_dest):
	(dictionary, bigram_f, word_f) = load_dict(dict_dest)
	default_freq = 1.0 / len(bigram_f)	
	return (dictionary, bigram_f, word_f, default_freq)

def load_dict(dict_dest):
	dictionary, bigram_f, word_f = {}, {}, {}

	with open(dict_dest, 'rb') as file:
		content = file.readlines()

	bigram_count = 0
	for line in content:
		bg = line.split()

		# Process alphabet only
		if bg[1].isalpha() and bg[2].isalpha():
			bigram_count += int(bg[0])
			insert_bigram(bigram_f, bg)

			insert_dict(dictionary, bg[1])
			insert_dict(dictionary, bg[2])

			insert_word(word_f, bg[1], bg[0])
			insert_word(word_f, bg[2], bg[0])

	normalize(bigram_f, bigram_count)
	normalize(word_f, 2*bigram_count) # each freq counted twice

	return (dictionary, bigram_f, word_f)

def insert_bigram(bigram_f, entry):
	bigram_f[(entry[1], entry[2])] = float(entry[0])

def insert_dict(dictionary, word):
	length = len(word)

	if length in dictionary:
		dictionary.get(length).add(word)
	else:
		dictionary[length] = {word}

def insert_word(word_f, word, freq):
	if word in word_f:
		word_f[word] += float(freq)
	else:
		word_f[word] = float(freq)

def filter_dict(candidates, target):
	regex = '^' + target.replace('_', '[a-z]') + '$'
	obj = re.compile(regex)

	new_set = set()
	for c in candidates:
		if obj.match(c): new_set.add(c)

	return new_set

def normalize(dictionary, count):
	if count != 0:
		for k in dictionary: dictionary[k] /= float(count)

def process_text(text):
	return len(text)