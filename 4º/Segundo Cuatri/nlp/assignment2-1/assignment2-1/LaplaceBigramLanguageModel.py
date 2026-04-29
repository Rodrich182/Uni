import math, collections


class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # count(prev, curr)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    # count(prev), usado como contexto del bigrama.
    self.contextCounts = collections.defaultdict(lambda: 0)
    # V sin tokens de frontera.
    self.vocabulary = set([])
    self.vocabularySize = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]

      for token in tokens:
        if token != "<s>" and token != "</s>":
          self.vocabulary.add(token)

      for i in range(1, len(tokens)):
        prev = tokens[i - 1]
        curr = tokens[i]
        # Estadísticas del modelo bigrama.
        self.bigramCounts[(prev, curr)] += 1
        self.contextCounts[prev] += 1

    self.vocabularySize = len(self.vocabulary)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    if self.vocabularySize == 0:
      return float('-inf')

    for i in range(1, len(sentence)):
      prev = sentence[i - 1]
      curr = sentence[i]
      # Laplace bigrama: (count(prev,curr)+1)/(count(prev)+V)
      numerator = self.bigramCounts[(prev, curr)] + 1
      denominator = self.contextCounts[prev] + self.vocabularySize
      score += math.log(float(numerator) / denominator)

    return score
