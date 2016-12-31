import hmm
import http_handler as hh
import file_handler as fh

def initGame():
	valid_set = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
	'o','p','q','r','s','t','u','v','w','x','y','z'}

	letter_f = [1/26.0] * 26
	# letter_url = "https://gist.githubusercontent.com/evilpacket/5973230/raw/045e0ecc34c6362728a9bce62d5cd2e41d29ad9a/letter_freq.json"
	# letter_dest = "/Users/Gilbert/Documents/hangman/freq.json"
	# letter_f = hh.loadFrequency(freq_dest, valid_set)

	# first_f = [0.11602, 0.04702, 0.03511, 0.026699999999999998, 0.02007, 0.03779, 0.0195, 0.07232, 0.06286, 0.00597, 0.0059, 0.02705, 0.04383, 0.02365, 0.06264, 0.02545, 0.0017299999999999998, 0.01653, 0.07755, 0.16671, 0.014870000000000001, 0.00649, 0.06753, 0.00017, 0.016200000000000003, 0.00034]
	first_f = [1/26.0] * 26;

	bigram_url = "https://gist.githubusercontent.com/lydell/259ab9f2ddaa1a64e6bd/raw/6e385151fd5de34e924a1e65f78d152c86afff76/bigrams-all.json"
	bigram_dest = "/Users/Gilbert/Documents/hangman/bigram.json"
	bi_f = fh.loadBigrams(bigram_dest)
	
	trigram_dest = "/Users/Gilbert/Downloads/english_trigrams.txt"
	tri_f = fh.loadTrigram(trigram_dest, valid_set)

	dict_url = "https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json"
	dict_dest = "/Users/Gilbert/Documents/hangman/dictionary.json"
	dictionary = fh.loadDictionary(dict_dest)
	
	return (letter_f, first_f, bi_f, tri_f)

def guessWord(obs, guessed_set):
	obs_num = 27
	state_num = 26

	states = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
	'o','p','q','r','s','t','u','v','w','x','y','z')

	remain_p = [[0 for c in range(len(obs))] for r in range(state_num)]
	for o_num in range(len(obs)):
		for s_num in range(state_num):
			if states[s_num] == obs[o_num] or states[s_num] not in guessed_set:
				remain_p[s_num][o_num] = 1 

	(letter_f, first_p, bi_p, tri_p) = initGame()
	
	emit_p = [[0 for c in range(obs_num)] for r in range(state_num)]
	for diagnol in range(state_num): 
		emit_p[diagnol][diagnol] = 1
		emit_p[diagnol][obs_num-1] = letter_f[diagnol]

	predictions = hmm.viterbi(obs, states, remain_p, first_p, bi_p, tri_p, emit_p)
	print predictions

	return optimize(predictions)

def optimize(predictions):
	result = []
	threshold = 0.8
	sum_p = sum([p[0] for p in predictions])

	prev_p = predictions[0][0] / sum_p
	for predict in predictions:
		if predict[0] == 0:
			break

		norm_p = predict[0] / sum_p
		if norm_p / prev_p >= threshold:
			result.append((norm_p, predict[1]))
		else:
			break

	return result


def interface(text):
	result = []
	guessed_set = set()

	for c in text:
		if c.isalpha(): guessed_set.add(c)

	words = text.split(" ")

	print guessed_set
	print words
	for w in words:
		result.append(optimize(guessWord(w, guessed_set)))

	return result

if __name__ == '__main__':
	"""
	Observations: 1*m (27 possible characters)
	States: 1*26
	Emission: 26*1 for '_' only
	Transition: 26*26 Bigram for now, consider using n-gram
	Start: 1 for valid character, 0 for invalid(guessed) character
	"""
	print interface("_a__ a good _a_")
	