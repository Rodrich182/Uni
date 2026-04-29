import math, collections


class KneserNeyLanguageModel:
  BOUNDARY_TOKENS = {"<s>", "</s>"}

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.d = 0.75
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.continuationCounts = collections.defaultdict(lambda: 0)
    self.followCounts = collections.defaultdict(lambda: 0)
    self.uniqueBigramCount = 0
    self.vocabulary = set()
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    unique_predecessors = collections.defaultdict(set)
    unique_successors = collections.defaultdict(set)
    unique_bigrams = set()

    for sentence in corpus.corpus:
      tokens = [datum.word for datum in sentence.data]
      for token in tokens:
        self.unigramCounts[token] += 1
        if token not in self.BOUNDARY_TOKENS:
          self.vocabulary.add(token)
          self.total += 1

      for i in range(1, len(tokens)):
        prev_token = tokens[i - 1]
        token = tokens[i]
        self.bigramCounts[(prev_token, token)] += 1
        unique_bigrams.add((prev_token, token))
        unique_predecessors[token].add(prev_token)
        unique_successors[prev_token].add(token)

    self.uniqueBigramCount = len(unique_bigrams)
    for token, predecessors in unique_predecessors.items():
      self.continuationCounts[token] = len(predecessors)
    for prev_token, successors in unique_successors.items():
      self.followCounts[prev_token] = len(successors)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    if len(sentence) <= 1:
      return 0.0

    score = 0.0
    vocab_size = max(1, len(self.vocabulary))
    continuation_denominator = max(1, self.uniqueBigramCount)
    unigram_denominator = max(1, self.total + vocab_size)

    for i in range(1, len(sentence)):
      prev_token = sentence[i - 1]
      token = sentence[i]
      prev_count = self.unigramCounts[prev_token]
      bigram_count = self.bigramCounts[(prev_token, token)]
      n_next = self.followCounts[prev_token]
      n_prev = self.continuationCounts[token]

      numerator = max(bigram_count - self.d, 0.0)
      numerator += self.d * n_next * float(n_prev) / continuation_denominator

      if numerator > 0.0 and prev_count > 0:
        prob = numerator / prev_count
      else:
        # Fallback follows the assignment guideline: Laplace unigram.
        prob = float(self.unigramCounts[token] + 1) / unigram_denominator
      score += math.log(prob)

    return score
