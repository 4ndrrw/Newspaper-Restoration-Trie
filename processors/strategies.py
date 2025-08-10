from abc import ABC, abstractmethod
import random

class RestoreStrategy(ABC):
  @abstractmethod
  def restore(self, pattern, trie_processor):
    # Restore a single wildcard word using the provided trie processor
    pass

class BestMatchStrategy(RestoreStrategy):
  def restore(self, pattern, trie_processor):
    # Return the best match (random among highest frequency)
    matches = trie_processor.find_matches(pattern)
    if not matches:
      return pattern
    max_freq = matches[0][1]
    top = [w for w, f in matches if f == max_freq]
    return random.choice(top)

class AllMatchesStrategy(RestoreStrategy):
  def restore(self, pattern, trie_processor):
    # Return all matches as ['opt1','opt2',...] format
    matches = trie_processor.find_matches(pattern)
    if not matches:
      return pattern
    items = [f"'{w}'" for w, _ in matches]
    return f"[{','.join(items)}]"