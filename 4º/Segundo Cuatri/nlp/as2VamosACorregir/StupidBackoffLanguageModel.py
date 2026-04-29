import math


class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # Factor de backoff del enunciado.
    self.alpha = 0.4
    # Conteos bigrama/contexto para usar la probabilidad condicional cuando existe el bigrama.
    self.bigramCounts = {}
    self.contextCounts = {}
    # Conteos unigrama para el caso de backoff.
    self.unigramCounts = {}
    self.totalTokens = 0
    self.vocabulary = set()
    self.vocabularySize = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]

      for token in tokens:
        # <s> no se cuenta en N; </s> sí se cuenta como token pero no entra en V.
        self.unigramCounts[token] = self.unigramCounts.get(token, 0) + 1
        if token == "<s>":
          continue      
        if token != "</s>":
          self.totalTokens += 1
          self.vocabulary.add(token)

      for i in range(1, len(tokens)):
        prev = tokens[i - 1]
        curr = tokens[i]
        self.bigramCounts[(prev, curr)] = self.bigramCounts.get((prev, curr), 0) + 1
        self.contextCounts[prev] = self.contextCounts.get(prev, 0) + 1

    self.vocabularySize = len(self.vocabulary)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    unigramDenominator = self.totalTokens + self.vocabularySize
    if unigramDenominator == 0:
      return float('-inf')

    for i in range(1, len(sentence)):
      prev = sentence[i - 1]
      curr = sentence[i]
      bigramCount = self.bigramCounts.get((prev, curr), 0)

      if bigramCount > 0:
        # Si vimos el bigrama en entrenamiento, usamos MLE de bigrama.
        probability = float(bigramCount) / self.contextCounts.get(prev, 0)
      else:
        # Si no existe, hacemos backoff a unigrama Laplace escalado por alpha.
        probability = self.alpha * float(self.unigramCounts.get(curr, 0) + 1) / unigramDenominator

      if probability <= 0.0:
        return float('-inf')
      score += math.log(probability)

    return score
