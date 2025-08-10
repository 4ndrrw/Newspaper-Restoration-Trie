import re

def default_confusables():
  # Basic OCR confusables map (symmetric pairs expanded)
  base = {
    '0': ['O', 'o'],
    'O': ['0', 'o'],
    'o': ['0', 'O'],
    '1': ['l', 'I'],
    'l': ['1', 'I'],
    'I': ['1', 'l'],
    'rn': ['m'],
    'm': ['rn'],
  }
  return base

def is_confusable(a, b, conf):
  # Treat as equal if exactly same (case-insensitive) or mapped confusables
  if a == b:
    return True
  if a.lower() == b.lower():
    return True
  if len(a) == 1 and len(b) == 1 and a in conf and b in conf[a]:
    return True
  return False

class TrieFuzzySearcher:
  def __init__(self, trie_processor, confusables=None):
    # Keep reference to the trie processor
    self.trie_proc = trie_processor
    self.conf = confusables or default_confusables()

  def search_word(self, word, max_dist=1):
    """
    Return list of (candidate, distance) whose edit distance <= max_dist.
    Based on DP rows carried along the trie (Ukkonen-style pruning).
    """
    word = word.lower()
    root = self.trie_proc.trie.root
    results = []
    init_row = list(range(len(word) + 1))

    def recurse(node, prefix, prev_row):
      for ch, child in node.children.items():
        curr_row = [prev_row[0] + 1]  # deletion cost
        for i in range(1, len(word) + 1):
          cost_sub = 0 if is_confusable(ch, word[i-1], self.conf) else 1
          insert_cost = curr_row[i-1] + 1
          delete_cost = prev_row[i] + 1
          sub_cost = prev_row[i-1] + cost_sub
          curr_row.append(min(insert_cost, delete_cost, sub_cost))
        if curr_row[-1] <= max_dist and child.is_end:
          results.append((prefix + ch, curr_row[-1]))
        if min(curr_row) <= max_dist:
          recurse(child, prefix + ch, curr_row)

    recurse(root, '', init_row)
    results.sort(key=lambda x: (x[1], x[0]))
    return results

  def suggest_for_text(self, text, max_dist=1):
    """
    For each word token not found in the trie (and without '*'),
    suggest near matches; return a list of (token, suggestions).
    """
    tokens = re.findall(r"[A-Za-z0-9']+|\n|[^\w\s]", text)
    suggestions = []
    for t in tokens:
      if '*' in t:
        continue
      if not re.match(r"[A-Za-z0-9']+$", t):
        continue
      if self.trie_proc.find_word(t.lower()):
        continue
      suggs = self.search_word(t, max_dist=max_dist)
      if suggs:
        suggestions.append((t, [w for w, d in suggs[:5]]))
    return suggestions