from helpers.trie import PrefixTrie
from processors.base_processor import BaseProcessor

class TrieProcessor(BaseProcessor):
  def __init__(self):
    # Initialize a new PrefixTrie instance and set current_trie_file to None
    super().__init__()
    self.__trie = PrefixTrie()
    self.current_trie_file = None

  @property
  def trie(self):
    # Read-only access to the underlying trie (encapsulation)
    return self.__trie

  def add_word(self, word, count=1):
    # Insert a word (converted to lowercase) into the trie
    self.__trie.insert(word.lower(), count)
    return f"Added '{word}' to trie"

  def delete_word(self, word):
    # Delete a word (converted to lowercase) from the trie
    # Return a message indicating success or failure
    if self.__trie.delete(word.lower()):
      return f"Deleted '{word}' from trie"
    return f"'{word}' is not a keyword in the trie"

  def find_word(self, word):
    # Search for a word (converted to lowercase) in the trie
    return self.__trie.search(word.lower())

  def display_trie(self):
    # Display a visual representation of the trie, or [] if empty
    if self.__trie.total_words == 0:
      print("[]")
    else:
      self.__trie.visualize()

  def get_all_words(self):
    # Retrieve all words stored in the trie
    return self.__trie.get_all_words()

  def find_matches(self, pattern):
    # Find all words in the trie that match the given pattern (converted to lowercase)
    return self.__trie.find_matches(pattern.lower())

  def clear_trie(self):
    # Clear the trie and reset it to empty state
    self.__trie = PrefixTrie()
    return "Trie cleared successfully"