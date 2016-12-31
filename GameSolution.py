import re
import operator
import collections

class GameSolution():

	dic_ngram_freq = {}
	defult_freq = 0.0
	guessed_letters = []
	word_dict = {}

	def __init__(self):
		total = self.get_word_count('w2_.txt')
		self.load_ngram_freq('w2_.txt', total)
		return

	def init(self):
		self.guessed_letters = []

	def load_ngram_freq(self, fileName, total):
		# dic_ngram_freq = {}
		f = open(fileName, 'r')
		for line in f:
			splited = line.split()
			self.dic_ngram_freq[(splited[1], splited[2])] = float(splited[0]) / total
		# return dic_ngram_freq

	def get_word_count(self, fileName):
		# word_set = set()
		word1_set = set()
		word2_set = set()
		pair_count = 0
		total = 0
		f = open(fileName, 'r')	
		for line in f:
			pair_count += 1
			splited = line.split()
			total += int(splited[0])
			if not splited[1] in self.word_dict:
				self.word_dict[splited[1]] = 1
			else:
				self.word_dict[splited[1]] += 1
			if not splited[2] in self.word_dict:
				self.word_dict[splited[2]] = 1
			else:
				self.word_dict[splited[2]] += 1				
			word1_set.add(splited[1])
			word2_set.add(splited[2])
		self.defult_freq = 1.0 * 1 / pair_count
		# print 'total: ', total
		# print 'pair_count: ', pair_count
		# print 'len(word_set): ', len(word_set)
		# print 'len(word1_set): ', len(word1_set)
		# print 'len(word2_set): ', len(word2_set)
		# print 'len(word2_set): ', len(word2_set)
		# print 'defult_freq: ', self.defult_freq
		# print 'self.word_set', self.word_set
		return total


	def get_ngram_freq(self, word1, word2):
		# return 1.0
		if (word1, word2) in self.dic_ngram_freq:
			# print 'Found ngram freq for given pairs (%s, %s) = %.10f' % (word1, word2, self.dic_ngram_freq[(word1, word2)])
			return self.dic_ngram_freq[(word1, word2)]
		else:
			# print 'No ngram freq for given pairs (%s, %s), use default = %.10f' % (word1, word2, self.defult_freq)
			return self.defult_freq
		

	def get_top_words_freq(self, input_array):
		return [[('have', 0.2), ('hate', 0.2), ('hair', 0.3)],
				[('a', 0.2), ('access', 0.2)],
				[('good', 0.1), ('tooo', 0.3), ('bady', 0.3)],
				[('day', 0.1), ('daa', 0.2), ('dao', 0.3)]
				]

	def get_top_words_freq_naive(self, input_array):
		splited = input_array.split()
		# print splited
		words_freq = []
		for i in range(0, len(splited)):
			filtered = self.get_top_words_freq_naive_helper(splited[i])
			# print filtered
			words_freq.append(filtered)
		# print 'words_freq', words_freq
		return words_freq

	def get_top_words_freq_naive_helper(self, input):
		regex = '^' + input.replace('_', '[a-z]') + '$'		# suppose no A-Z
		# print 'regex', regex
		filtered = []
		reobj = re.compile(regex)
		for key in self.word_dict.keys():
			if(reobj.match(key)):
				filtered.append((key, self.word_dict[key]))
		sorted_filtered = sorted(filtered,key=operator.itemgetter(1))
		# print sorted_filtered
		if len(sorted_filtered) == 0:
			print 'len(sorted_filtered) == 0'
			return []
		elif len(sorted_filtered) > 5:
			return sorted_filtered[-5:]
		else:
			return sorted_filtered


	def get_sentences_prob(self, input_array):
		# words_freq = self.get_top_words_freq(input_array)
		words_freq = self.get_top_words_freq_naive(input_array)
		print 'words_freq', words_freq
		sentence = []
		prob = 1.0
		sentences_prob = []
		self.get_sentences_prob_helper(words_freq, 0, sentence, prob, sentences_prob)
		# print 'sentences_prob', len(sentences_prob), sentences_prob
		sorted_sentences_prob = sorted(sentences_prob, key=operator.itemgetter(1))
		# print 'sorted_sentences_prob', len(sorted_sentences_prob), sorted_sentences_prob
		return sorted_sentences_prob

	def get_sentences_prob_helper(self, words_freq, i, sentence, prob, sentences_prob):
		if i == len(words_freq):	# now save temp sentence and prob
			sentences_prob.append((list(sentence), prob))
			return 
		for j in range(0, len(words_freq[i])):
			prob_old = prob
			if len(sentence) != 0:
				prob *= self.get_ngram_freq(sentence[-1], words_freq[i][j][0]) *  words_freq[i][j][1]
			else:
				prob *= words_freq[i][j][1]
			sentence.append(words_freq[i][j][0])
			self.get_sentences_prob_helper(words_freq, i+1, sentence, prob, sentences_prob)
			
			prob = prob_old
			del sentence[-1]

	def get_guess_letter(self, input_array):
		sentences_prob = self.get_sentences_prob(input_array)
		i = len(sentences_prob) - 1
		sentence = ""
		while i >= 0 and i >= len(sentences_prob) - 5:
			sentence += "".join(sentences_prob[i][0])
			i -= 1
		print 'sentence', sentence
		letter_list = collections.Counter(sentence).most_common()
		for letter_count in letter_list:
			if letter_count[0][0] not in self.guessed_letters:
				self.guessed_letters.append(letter_count[0][0])
				print 'guess: ', letter_count[0][0]
				return letter_count[0][0]
		return ""

	
if __name__ == "__main__":
	gameSolution = GameSolution()
	gameSolution.get_top_words_freq_naive('_a__ _oo_')



