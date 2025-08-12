import re
from processors.strategies import BestMatchStrategy, AllMatchesStrategy, ContextBestStrategy
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
  
  def restore_text_with_context(self, text, lm, threshold=0.6):
    """
    Restore a text using the ContextBestStrategy with a language model.
    Produces:
      - restored text (best choices wrapped in <...>)
      - a list of review rows for CSV: [(original, choice, confidence, left, right, candidates_csv), ...]
    """
    tokens = re.findall(r"[a-zA-Z0-9*']+|[^\w\s]|\n", text)
    restored_tokens = []
    review_rows = []
    ctx_strategy = ContextBestStrategy()

    def prev_word(idx):
      j = idx - 1
      while j >= 0:
        if re.match(r"[A-Za-z0-9']+$", tokens[j]):
          return tokens[j].lower()
        elif tokens[j] == '\n':
          return '<s>'
        j -= 1
      return '<s>'

    def next_word(idx):
      j = idx + 1
      while j < len(tokens):
        if re.match(r"[A-Za-z0-9']+$", tokens[j]):
          return tokens[j].lower()
        elif tokens[j] == '\n':
          return '</s>'
        j += 1
      return None

    for i, token in enumerate(tokens):
      if '*' in token:
        # Score candidates using the language model and surrounding context
        left = prev_word(i)
        right = next_word(i)
        choice, conf = ctx_strategy.restore(token, self.trie, lm=lm, left_word=left, right_word=right)

        # Apply threshold: only replace if confidence >= threshold; otherwise keep original token
        if conf >= threshold:
          restored_tokens.append(f"<{choice}>")
        else:
          restored_tokens.append(token)

        # Collect review information for CSV (always recorded, even if not replaced)
        matches = self.trie.find_matches(token)
        alts = [w for w, _ in matches]
        review_rows.append((token, choice, f"{conf:.3f}", left, (right or ''), ",".join(alts)))
      else:
        # Keep tokens without wildcards unchanged
        restored_tokens.append(token)

    # Reconstruct the text, preserving spacing/newlines and handling punctuation
    out = ''
    for i, tok in enumerate(restored_tokens):
      if tok == '\n':
        out += tok
      elif i > 0 and restored_tokens[i - 1] != '\n' and not re.match(r"[.,!?;:\)\]\}]", tok):
        out += ' ' + tok
      else:
        out += tok

    return out, review_rows