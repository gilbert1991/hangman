class Word(object):
	def __init__(self, obs):
		self.str = str
		self.size = len(obs)
		self.data = Trie(self.size)

	def insert(self, words):
		for w in words:
			self.data.insert(w)

	def search(self, word):
		return self.data.search(word)

	# def remove(str):

class TrieNode(object):
	def __init__(self, val):
		self.val = val
		self.isLeaf = False
		self.children = {}

class Trie(object):

    def __init__(self, size):
        self.root = TrieNode(None)
        self.size = size

    def insert(self, word):
    	current = self.root

    	for c in word:
    		if c not in current.children:
    			current.children[c] = TrieNode(c)

        	current = current.children[c]
    	
    	current.isLeaf = True

    def search(self, word):
    	current = self.root

    	for c in word:
    		current = current.children.get(c)
    		if current is None: return False

    	return current.isLeaf

	# def startsWith(self, prefix):
	#     current = self.root
	#     for letter in prefix:
	#         current = current.children.get(letter)
	#         if current is None:
	#             return False
	#     return True

if __name__ == '__main__':
	word = Word("____")

	word.insert(["word", "work", "hand", "weak"])

	print word.search("word")
	print word.search("hand")
	print word.search("week")