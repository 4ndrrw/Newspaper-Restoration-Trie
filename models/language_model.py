import re
from collections import defaultdict, Counter
import math

class NGramLanguageModel:
  def __init__(self, k=1.0):
    # Add-k smoothing constant
    self.k = k
    self.unigrams = Counter()
    self.bigrams = defaultdict(Counter)
    self.V = 0

  def _tokenize(self, text):
    # Simple tokenizer: words + sentence boundaries
    lines = text.split('\n')
    seq = []
    for line in lines:
      if not line.strip():
        continue
      tokens = re.findall(r"[A-Za-z0-9']+", line.lower())
      if tokens:
        seq.append('<s>')
        seq.extend(tokens)
        seq.append('</s>')
    return seq

  def fit_from_file(self, corpus_filename):
    with open(corpus_filename, 'r', encoding='utf-8') as f:
      text = f.read()
    tokens = self._tokenize(text)
    for i, w in enumerate(tokens):
      self.unigrams[w] += 1
      if i > 0:
        prev = tokens[i-1]
        self.bigrams[prev][w] += 1
    self.V = len(self.unigrams)

  def prob_bigram(self, prev, word):
    num = self.bigrams[prev][word] + self.k
    den = sum(self.bigrams[prev].values()) + self.k * max(1, self.V)
    return num / den

  def logprob_context(self, left_word, word, right_word=None):
    lp = 0.0
    lp += math.log(self.prob_bigram(left_word, word))
    if right_word is not None:
      lp += math.log(self.prob_bigram(word, right_word))
    return lp

  def choose_best(self, candidates, left_word, right_word=None):
    if not candidates:
      return None, 0.0, {}
    scores = {}
    max_score = None
    for c in candidates:
      s = self.logprob_context(left_word, c, right_word)
      scores[c] = s
      if max_score is None or s > max_score:
        max_score = s
    exps = {w: math.exp(s - max_score) for w, s in scores.items()}
    Z = sum(exps.values())
    probs = {w: exps[w] / Z for w in exps}
    best = max(scores.items(), key=lambda kv: kv[1])[0]
    confidence = probs[best]
    return best, confidence, scores