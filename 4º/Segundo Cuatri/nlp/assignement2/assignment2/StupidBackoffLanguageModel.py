import math, collections


class StupidBackoffLanguageModel:
  BOUNDARY_TOKENS = {"<s>", "</s>"}

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.alpha = 0.4
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
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
          self.total += 1
          self.vocabulary.add(token)
      for i in range(1, len(tokens)):
        self.bigramCounts[(tokens[i - 1], tokens[i])] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    if len(sentence) <= 1:
      return 0.0
    if self.total == 0:
      return float("-inf")

    score = 0.0
    vocab_size = len(self.vocabulary)
    unigram_denominator = self.total + vocab_size
    for i in range(1, len(sentence)):
      prev_token = sentence[i - 1]
      token = sentence[i]
      bigram_count = self.bigramCounts[(prev_token, token)]
      prev_count = self.unigramCounts[prev_token]

      if bigram_count > 0 and prev_count > 0:
        prob = float(bigram_count) / prev_count
      else:
        # Fallback follows the assignment guideline: alpha * Laplace unigram.
        prob = self.alpha * float(self.unigramCounts[token] + 1) / unigram_denominator
      score += math.log(prob)
    return score
