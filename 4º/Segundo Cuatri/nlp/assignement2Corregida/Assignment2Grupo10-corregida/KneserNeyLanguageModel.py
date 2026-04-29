import math, collections


class KneserNeyLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.d = 2
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.contextCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalTokens = 0
    self.nextSets = collections.defaultdict(set)
    self.prevSets = collections.defaultdict(set)
    self.nNext = collections.defaultdict(lambda: 0)
    self.nPrev = collections.defaultdict(lambda: 0)
    self.numBigramTypes = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]

      for token in tokens:
        self.unigramCounts[token] += 1
        if token == "<s>" :
          continue   
        if token != "<s>" :
          self.unigramCounts[token] += 1
          self.totalTokens += 1
        

      for i in range(1, len(tokens)):
        prev = tokens[i - 1]
        curr = tokens[i]
        self.bigramCounts[(prev, curr)] += 1
        self.contextCounts[prev] += 1
        self.nextSets[prev].add(curr)
        self.prevSets[curr].add(prev)

    for prev, nextWords in self.nextSets.items():
      self.nNext[prev] = len(nextWords)

    for curr, prevWords in self.prevSets.items():
      self.nPrev[curr] = len(prevWords)

    self.numBigramTypes = len(self.bigramCounts)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    vocabularySize = len(self.unigramCounts)
    unigramDenominator = self.totalTokens + vocabularySize
    if self.numBigramTypes == 0 or unigramDenominator == 0:
      return float('-inf')

    for i in range(1, len(sentence)):
      prev = sentence[i - 1]
      curr = sentence[i]
      bigramCount = self.bigramCounts[(prev, curr)]
      contextCount = self.contextCounts[prev]
      numerator = max(bigramCount - self.d, 0.0)
      numerator += float(self.d * self.nNext[prev] * self.nPrev[curr]) / self.numBigramTypes

      if numerator > 0.0 and contextCount > 0:
        probability = float(numerator) / contextCount
      else:
        probability = float(self.unigramCounts[curr] + 1) / unigramDenominator

      if probability <= 0.0:
        return float('-inf')
      score += math.log(probability)

    return score
