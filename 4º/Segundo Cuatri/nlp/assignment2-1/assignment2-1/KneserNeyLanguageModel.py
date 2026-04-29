import math, collections


class KneserNeyLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # Descuento fijo usado en el modelo.
    self.d = 2
    # count(prev,curr) y count(prev)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.contextCounts = collections.defaultdict(lambda: 0)
    # Estadísticas unigram para fallback.
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalTokens = 0
    self.vocabulary = set([])
    self.vocabularySize = 0
    # nNext(prev): cuántos tipos distintos siguen a prev.
    self.nNext = collections.defaultdict(lambda: 0)
    # nPrev(curr): cuántos tipos distintos preceden a curr.
    self.nPrev = collections.defaultdict(lambda: 0)
    # Número total de tipos de bigrama observados.
    self.numBigramTypes = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    nextSets = collections.defaultdict(set)
    prevSets = collections.defaultdict(set)

    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]

      for token in tokens:
        # <s> no se cuenta en N; </s> sí se cuenta como token pero no entra en V.
        if token == "<s>":
          continue
        self.unigramCounts[token] += 1
        self.totalTokens += 1
        if token != "</s>":
          self.vocabulary.add(token)

      for i in range(1, len(tokens)):
        prev = tokens[i - 1]
        curr = tokens[i]
        # Conteos base + sets para obtener nNext y nPrev.
        self.bigramCounts[(prev, curr)] += 1
        self.contextCounts[prev] += 1
        nextSets[prev].add(curr)
        prevSets[curr].add(prev)

    for prev, nextWords in nextSets.items():
      self.nNext[prev] = len(nextWords)

    for curr, prevWords in prevSets.items():
      self.nPrev[curr] = len(prevWords)

    self.numBigramTypes = len(self.bigramCounts)
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
      bigramCount = self.bigramCounts[(prev, curr)]
      contextCount = self.contextCounts[prev]

      # Parte descontada del bigrama observado.
      discounted = max(bigramCount - self.d, 0)
      continuation = 0.0
      if self.numBigramTypes > 0:
        # Parte de continuación basada en diversidad de contextos.
        continuation = float(self.d * self.nNext[prev] * self.nPrev[curr]) / self.numBigramTypes

      numerator = discounted + continuation
      if numerator > 0.0 and contextCount > 0:
        probability = float(numerator) / contextCount
      else:
        # Fallback unigrama Laplace cuando no hay masa suficiente en el contexto.
        probability = float(self.unigramCounts[curr] + 1) / unigramDenominator

      if probability <= 0.0:
        return float('-inf')
      score += math.log(probability)

    return score
