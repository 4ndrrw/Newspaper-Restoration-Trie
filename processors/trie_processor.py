from helpers.trie import PrefixTrie

class TrieProcessor:
    def __init__(self):
        self.trie = PrefixTrie()
        self.current_trie_file = None

    def add_word(self, word):
        self.trie.insert(word.lower())
        return f"Added '{word}' to trie"

    def delete_word(self, word):
        if self.trie.delete(word.lower()):
            return f"Deleted '{word}' from trie"
        return f"'{word}' not found in trie"

    def find_word(self, word):
        return self.trie.search(word.lower())

    def display_trie(self):
        return self.trie.visualize()

    def get_all_words(self):
        return self.trie.get_all_words()

    def find_matches(self, pattern):
        return self.trie.find_matches(pattern.lower())