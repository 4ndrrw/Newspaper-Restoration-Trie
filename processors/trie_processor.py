from helpers.trie import PrefixTrie

class TrieProcessor:
  def __init__(self):
    # Initialize a new PrefixTrie instance and set current_trie_file to None
    self.trie = PrefixTrie()
    self.current_trie_file = None

  def add_word(self, word):
    # Insert a word (converted to lowercase) into the trie
    self.trie.insert(word.lower())
    return f"Added '{word}' to trie"

  def delete_word(self, word):
    # Delete a word (converted to lowercase) from the trie
    # Return a message indicating success or failure
    if self.trie.delete(word.lower()):
      return f"Deleted '{word}' from trie"
    return f"'{word}' is not a keyword in the trie"

  def find_word(self, word):
    # Search for a word (converted to lowercase) in the trie
    return self.trie.search(word.lower())

  def display_trie(self):
    # Display a visual representation of the trie, or [] if empty
    if self.trie.total_words == 0:
      print("[]")
    else:
      self.trie.visualize()

  def get_all_words(self):
    # Retrieve all words stored in the trie
    return self.trie.get_all_words()

  def find_matches(self, pattern):
    # Find all words in the trie that match the given pattern (converted to lowercase)
    return self.trie.find_matches(pattern.lower())

  def clear_trie(self):
    # Clear the trie and reset it to empty state
    self.trie = PrefixTrie()
    return "Trie cleared successfully"
