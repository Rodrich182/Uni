import math, collections


class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # Conteos unigrama para aplicar suavizado de Laplace.
    self.unigramCounts = collections.defaultdict(lambda: 0)
    # N: total de tokens (sin incluir <s> y </s>).
    self.totalTokens = 0
    # V: vocabulario observado en entrenamiento.
    self.vocabulary = set([])
    self.vocabularySize = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        
        if token == "<s>" or token == "</s>":
          continue
        self.unigramCounts[token] += 1
        self.totalTokens += 1
        self.vocabulary.add(token)
    self.vocabularySize = len(self.vocabulary)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    
    denominator = self.totalTokens + self.vocabularySize
    if denominator == 0:
      return float('-inf')

    for token in sentence:
      if token == "<s>" or token == "</s>":
        continue
      count = self.unigramCounts[token]
      # log P(w) con add-one smoothing.
      score += math.log(float(count + 1) / denominator)
    return score
