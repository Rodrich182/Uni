import math, collections


class LaplaceUnigramLanguageModel:
  BOUNDARY_TOKENS = {"<s>", "</s>"}

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.vocabulary = set()
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.unigramCounts[token] += 1
        if token not in self.BOUNDARY_TOKENS:
          self.total += 1
          self.vocabulary.add(token)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    vocab_size = len(self.vocabulary)
    denominator = self.total + vocab_size
    for token in sentence:
      if token in self.BOUNDARY_TOKENS:
        continue
      score += math.log(self.unigramCounts[token] + 1)
      score -= math.log(denominator)
    return score
