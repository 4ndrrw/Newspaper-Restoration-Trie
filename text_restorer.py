import re

class TextRestorer:
  def __init__(self, trie):
    self.trie = trie  # Trie data structure for word lookup
    self.restoration_history = []  # Keep track of restoration actions
  
  def _is_wildcard_word(self, word):
    # Check if the word contains a wildcard character '*'
    return '*' in word
  
  def _get_word_variants(self, word):
    # Handle punctuation attached to wildcard words
    base_word = re.sub(r'[^a-zA-Z*]', '', word)  # Remove punctuation except '*'
    matches = self.trie.find_matches(base_word)  # Find possible matches in the trie
    
    if not matches:
      return [(word, 0)]  # Return original if no matches
    
    # Reattach punctuation to the matched words
    prefix = word[:word.find(base_word)]
    suffix = word[word.find(base_word) + len(base_word):]
    return [(prefix + match[0] + suffix, match[1]) for match in matches]
  
  def restore_word(self, word, mode='best'):
    # Restore a single word, replacing wildcards using the trie
    if not self._is_wildcard_word(word):
      return word
    
    variants = self._get_word_variants(word)
    
    if mode == 'best':
      # Choose the variant with the highest score
      best_match = max(variants, key=lambda x: x[1]) if variants else (word, 0)
      return f"<{best_match[0]}>" if best_match[1] > 0 else word
    else:  # 'all' mode
      # Show all possible variants
      options = [f"[{variant[0]}]" for variant in variants if variant[1] > 0]
      return f"{word} {' '.join(options)}" if options else word
  
  def restore_text(self, text, mode='best'):
    # Restore all wildcard words in a text
    # Split while preserving contractions and punctuation
    tokens = re.findall(r"\w+'\w+|\w+|\W+", text)
    restored_tokens = []
    
    for token in tokens:
      if self._is_wildcard_word(token):
        restored = self.restore_word(token, mode)
        self.restoration_history.append((token, restored))  # Log restoration
        restored_tokens.append(restored)
      else:
        restored_tokens.append(token)
    
    # Reconstruct text with original spacing
    return ''.join(restored_tokens)
  
  def batch_restore_files(self, input_files, output_dir, mode='best'):
    # Restore text in multiple files and save the results
    results = []
    for file in input_files:
      with open(file, 'r') as f:
        content = f.read()
      restored = self.restore_text(content, mode)
      
      output_path = os.path.join(output_dir, f"restored_{os.path.basename(file)}")
      with open(output_path, 'w') as f:
        f.write(restored)
      
      results.append((file, output_path))
    return results