import math, collections


class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.alpha = 0.4
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.contextCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalTokens = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]

      for token in tokens:
        if token == "<s>" or token == "</s>":
          continue
        self.unigramCounts[token] += 1
        self.totalTokens += 1

      for i in range(1, len(tokens)):
        prev = tokens[i - 1]
        curr = tokens[i]
        self.bigramCounts[(prev, curr)] += 1
        self.contextCounts[prev] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    vocabularySize = len(self.unigramCounts)
    unigramDenominator = self.totalTokens + vocabularySize
    if unigramDenominator == 0:
      return float('-inf')

    for i in range(1, len(sentence)):
      prev = sentence[i - 1]
      curr = sentence[i]
      bigramCount = self.bigramCounts[(prev, curr)]

      if bigramCount > 0:
        probability = float(bigramCount) / self.contextCounts[prev]
      else:
        probability = self.alpha * float(self.unigramCounts[curr] + 1) / unigramDenominator

      if probability <= 0.0:
        return float('-inf')
      score += math.log(probability)

    return score
