import nltk
from nltk.corpus import brown

print(nltk.corpus.gutenberg.fileids())

movie_dick = nltk.corpus.gutenberg.words('austen-persuasion.txt')
print(len(movie_dick))

target = "nonsensical"
for cat in brown.categories():
    c = sum(1 for w in brown.words(categories=cat) if w.lower() == target)
    if c == 1:
        print(cat)