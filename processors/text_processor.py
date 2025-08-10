import re
from processors.strategies import BestMatchStrategy, AllMatchesStrategy
from processors.base_processor import BaseProcessor

class TextProcessor(BaseProcessor):
  def __init__(self, trie_processor):
    # Store the trie processor instance for word restoration
    super().__init__()
    self.trie = trie_processor
    # Register strategies for polymorphic restore behavior
    self._strategies = {
      'best': BestMatchStrategy(),
      'all': AllMatchesStrategy()
    }

  def restore_word(self, word, mode='best'):
    # If the word does not contain a wildcard, return as is
    if '*' not in word:
      return word

    # Pick strategy and restore word
    strat = self._strategies.get(mode, self._strategies['best'])
    result = strat.restore(word, self.trie)
    # Record restoration event
    self.record((word, result))
    return result

  def restore_text(self, text, mode='best'):
    # Tokenize words including wildcards, apostrophes, digits, punctuation, and newlines
    tokens = re.findall(r"[a-zA-Z0-9*']+|[^\w\s]|\n", text)
    restored_tokens = []

    for token in tokens:
      if '*' in token:
        # Restore words with wildcards
        restored = self.restore_word(token, mode)
        if mode == 'best':
          # Wrap the best match with < >
          restored_tokens.append(f"<{restored}>")
        else:
          # Keep the ['opt1','opt2'] output
          restored_tokens.append(restored)
      else:
        # Keep tokens without wildcards unchanged
        restored_tokens.append(token)

    # Reconstruct the text with spacing and preserved newlines/punctuation
    restored_text = ""
    for i, token in enumerate(restored_tokens):
      if token == '\n':
        restored_text += token
      elif i > 0 and restored_tokens[i - 1] != '\n' and not re.match(r"[.,!?;:\)\]\}]", token):
        restored_text += " " + token
      else:
        restored_text += token
    return restored_text
