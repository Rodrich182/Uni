# Descarga datos (solo una vez)
import nltk
nltk.download('book', quiet=True)

# Imports
from nltk.book import *
from collections import Counter

print("text3:", len(text3), "tokens")
print("text5:", len(text5), "tokens")

# Q1: Segunda 7-letras más frecuente en text5
seven = [w for w in text5 if len(w) == 7]
fd = Counter(seven)
top = sorted(fd.items(), key=lambda x: x[1], reverse=True)
second_freq = top[1][1]
print("\nQ1:", second_freq)  # 82

# Q2: Lexical diversity text3
lex_div = len(set(text3)) / len(text3)
print("Q2:", round(lex_div, 3))  # 0.062
