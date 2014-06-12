import nltk;

origText = open('warofroses.txt', 'r');
stegText = open('warofposes.txt', 'w');

wholePaper = origText.read();

sepWords = nltk.word_tokenize(wholePaper);

from nltk.corpus import wordnet

for word in sepWords:
    wordnet.synsets(word)
