from abc import ABC, abstractmethod
import random

class RestoreStrategy(ABC):
  @abstractmethod
  def restore(self, pattern, trie_processor, **kwargs):
    # Restore a single wildcard word using the provided trie processor
    pass

class BestMatchStrategy(RestoreStrategy):
  def restore(self, pattern, trie_processor, **kwargs):
    # Return the best match (random among highest frequency)
    matches = trie_processor.find_matches(pattern)
    if not matches:
      return pattern
    max_freq = matches[0][1]
    top = [w for w, f in matches if f == max_freq]
    return random.choice(top)

class AllMatchesStrategy(RestoreStrategy):
  def restore(self, pattern, trie_processor, **kwargs):
    # Return all matches as ['opt1','opt2',...] format
    matches = trie_processor.find_matches(pattern)
    if not matches:
      return pattern
    items = [f"'{w}'" for w, _ in matches]
    return f"[{','.join(items)}]"

class ContextBestStrategy(RestoreStrategy):
  def restore(self, pattern, trie_processor, **kwargs):
    """
    Context-aware best choice using a bigram LM.
    kwargs:
      lm: NGramLanguageModel (required)
      left_word: str or '<s>'
      right_word: str or None
    """
    lm = kwargs.get('lm')
    left_word = (kwargs.get('left_word') or '<s>').lower()
    right_word = kwargs.get('right_word')
    if right_word is not None:
      right_word = right_word.lower()

    if lm is None:
      # Fallback to plain best if LM not provided
      return BestMatchStrategy().restore(pattern, trie_processor)

    matches = trie_processor.find_matches(pattern)
    if not matches:
      return pattern

    candidates = [w for w, _ in matches]
    best, confidence, _ = lm.choose_best(candidates, left_word, right_word)
    return best, confidence
