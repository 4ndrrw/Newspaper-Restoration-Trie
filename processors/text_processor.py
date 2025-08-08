from processors.trie_processor import TrieProcessor
import re

class TextProcessor:
  def __init__(self, trie_processor):
    # Store the trie processor instance for word restoration
    self.trie = trie_processor
    # Keep a history of restoration attempts (original, restored)
    self.restoration_history = []

  def restore_word(self, word, mode='best'):
    # If the word does not contain a wildcard, return as is
    if '*' not in word:
      return word

    # Find possible matches for the word with wildcards
    matches = self.trie.find_matches(word)
    if not matches:
      # If no matches found, return the original word
      return word

    if mode == 'best':
      # Return the best match (first one) wrapped in <>
      return f"<{matches[0][0]}>"
    else:
      # Return all options as [option] after the word
      options = [f"[{match[0]}]" for match in matches]
      return f"{word} {' '.join(options)}"

  def restore_text(self, text, mode='best'):
    # Tokenize the text, preserving words, contractions, and punctuation
    tokens = re.findall(r"\w+'\w+|\w+|\W+", text)
    restored_tokens = []

    for token in tokens:
      if '*' in token:
        # Restore words with wildcards and record the restoration
        restored = self.restore_word(token, mode)
        self.restoration_history.append((token, restored))
        restored_tokens.append(restored)
      else:
        # Keep tokens without wildcards unchanged
        restored_tokens.append(token)

    # Reconstruct the text from the restored tokens
    return ''.join(restored_tokens)
