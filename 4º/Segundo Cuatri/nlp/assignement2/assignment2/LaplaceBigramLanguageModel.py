import math, collections


class LaplaceBigramLanguageModel:
  BOUNDARY_TOKENS = {"<s>", "</s>"}

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.vocabulary = set()
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]
      for token in tokens:
        self.unigramCounts[token] += 1
        if token not in self.BOUNDARY_TOKENS:
          self.vocabulary.add(token)
      for i in range(1, len(tokens)):
        self.bigramCounts[(tokens[i - 1], tokens[i])] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    if len(sentence) <= 1:
      return 0.0

    score = 0.0
    vocab_size = len(self.vocabulary)
    for i in range(1, len(sentence)):
      prev_token = sentence[i - 1]
      token = sentence[i]
      numerator = self.bigramCounts[(prev_token, token)] + 1
      denominator = self.unigramCounts[prev_token] + vocab_size
      score += math.log(numerator)
      score -= math.log(denominator)
    return score
