import random

class RandomWordChallenge:
	def __init__(self, trie_processor):
		self.trie_processor = trie_processor

	def play_round(self):
		"""Play a single round of the random word challenge with difficulty selection."""
		print("Select difficulty: [1] Easy  [2] Medium  [3] Hard")
		print("  	Easy:   5-6 letter words, 1 letter hidden")
		print("  	Medium: 7-8 letter words, 3 letters hidden")
		print("  	Hard:   9+ letter words, 5 letters hidden\n")
		level = input("Enter 1, 2, or 3: ").strip()
		if level not in {'1', '2', '3'}:
			print("Invalid choice. Defaulting to Easy.")
			level = '1'
		word = self._get_random_word(level)
		if not word:
			print("No eligible words for this difficulty. Please add more words!")
			return
		masked = self._mask_word(word, level)
		print(f"Guess the word: {masked}")
		guess = input("Your guess: ").strip().lower()
		if guess == word:
			print("Correct! Well done!")
		else:
			print(f"Incorrect. The word was: {word}")

	def _get_random_word(self, level):
		# Easy: 5-6 letters, Medium: 7-8, Hard: 9+
		if level == '1':
			words = [w for w, _ in self.trie_processor.get_all_words() if 5 <= len(w) <= 6]
		elif level == '2':
			words = [w for w, _ in self.trie_processor.get_all_words() if 7 <= len(w) <= 8]
		else:
			words = [w for w, _ in self.trie_processor.get_all_words() if len(w) >= 9]
		if not words:
			return None
		return random.choice(words)

	def _mask_word(self, word, level):
		n = len(word)
		if level == '1':
			num_to_hide = 1
		elif level == '2':
			num_to_hide = 3 if n >= 7 else 2
		else:
			num_to_hide = 5 if n >= 9 else 4
		indices = random.sample(range(n), min(num_to_hide, n))
		return ''.join('*' if i in indices else c for i, c in enumerate(word))
