import file_handler as fh

class HangMan():
	def __init__(self, dict_dest):
		self.ai = AI(dict_dest)
		self.remain = 0
		self.guessed_l = set()

		self.letter_f = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', \
		'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

	def init_hm(self, text, remain):
		self.remain = remain

		self.guessed_l = set()
		for l in text: 
			if l.isalpha(): self.guessed_l.add(l)

		self.ai.init_ai(text)

	def update_hm(self, text, remain):
		self.remain = remain

		for l in text: 
			if l.isalpha(): self.guessed_l.add(l)

		self.ai.update_ai(text)

	def guess(self):
		if self.remain > 4 and self.simple_guess():
			letter = self.simple_guess()
			print "Simple Guess %c" % letter
		else:
			letter = self.ai.guess()
			print "AI Guess %s" % letter

		self.guessed_l.add(letter)
		self.ai.guessed_l.add(letter)

		return letter

	def simple_guess(self):
		for l in self.letter_f:
			if l not in self.guessed_l:
				return l

		return None

class AI():
	def __init__(self, dict_dest):
		(self.dictionary, self.bigram_f, self.word_f, self.default_freq) = fh.init_dict(dict_dest)

		self.guessed_l = set()
		self.ans = []
		self.candidates = []
		self.text = ""

		self.letter_f = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', \
		'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

	def init_ai(self, text):
		self.text = text

		self.ans = []
		self.guessed_l = set()
		self.candidates = []

		try:		
			self.ans = text.strip().split()
			
			for letter in text: 
				if letter.isalpha(): self.guessed_l.add(letter)

			for word in self.ans:
				if len(word) <= len(self.dictionary):
					self.candidates.append(fh.filter_dict(self.dictionary[len(word)], word))
				else:
					self.candidates.append(set())

		except:
			print "Error: Init AI."		

	def update_ai(self, text):		
		self.text = text

		# Update answers TODO
		self.ans = text.strip().split()

		# Update candidates for each word
		for idx in range(len(self.ans)):
			self.candidates[idx] = fh.filter_dict(self.candidates[idx], self.ans[idx])

	def guess(self):
		(path, prob) = self.veterbi()

		return self.predict(path, prob)

	def predict(self, path, prob):
		letter = None

		guess = {}

		# Calculate letter freq based on sentence freq
		for key in prob:
			sentence, p = path[key], prob[key]
			origin = " ".join(self.ans)

			for idx in range(len(sentence)):
				c = sentence[idx]

				# Calculate those not revealed positions only
				if c.isalpha() and c not in self.guessed_l and origin[idx] == '_':
					if c in guess: guess[c] += p
					else: guess[c] = p

		# All prediction has been guessed before 
		if not guess:
			for l in self.letter_f:
				if l not in self.guessed_l:
					return l


		letter = max(guess, key=guess.get) # TODO

		return letter


	def veterbi(self):
		prob = [{}]
		path = {}

		# Init first word
		if not self.candidates[0]: # Use ans if no candidates for ans in dict
			c = self.ans[0]
			prob[0][c] = 1
			path[c] = c
		else:
			for c in self.candidates[0]:
				prob[0][c] = self.word_f[c]
				path[c] = c

		# Subsequential words 
		for t in range(1, len(self.ans)):
			prob.append({})
			new_path = {}
			
			# Use ans if no candidates for ans in dict
			if not self.candidates[t]:
				pre_max = max(prob[t-1], key=prob[t-1].get)

				prob[t][self.ans[t]] = 1.0
				new_path[self.ans[t]] = "%s %s" % (path[pre_max], self.ans[t])

			else:
				sum_p = 0
				for c in self.candidates[t]:
					max_p, max_w = 0, ""
					for pre_c in prob[t-1]:
						# Use default freq if no bigram in dictionary
						trans_f = self.bigram_f[(pre_c, c)] if (pre_c, c) in self.bigram_f else self.default_freq

						prob[t][c] = prob[t-1][pre_c] * trans_f * self.word_f[c]
						sum_p += prob[t][c]

						if prob[t][c] > max_p:
							max_p = prob[t][c]
							max_w = pre_c
					
					# Store valid path only
					if max_w != "": new_path[c] = "%s %s" % (path[max_w], c)

				# Normalize probability at 't' in case of overflow
				fh.normalize(prob[t], sum_p)

			# Refresh path
			path = new_path

		# # sorted_path = sorted(prob[~0].items(), key=lambda (k,v):v, reverse=True)
		# # print path
		# # prediction = [path[p[0]] for p in prob]
	
		return (path, prob[~0])

if __name__ == '__main__':
	dict_dest = "/Users/Gilbert/Documents/hangman/w2_.txt"
	text = "_a_e a gctd da_"

	hangman = HangMan(dict_dest)
	hangman.init_hm("_hat are _ou doin_  ", 3)
	# hangman.update_hm(text, 3)

	print hangman.guess()


