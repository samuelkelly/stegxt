import nltk;
import random;

origText = open('warofroses.txt', 'r');
stegText = open('warofposes.txt', 'w');

wholePaper = origText.read();

sepWords = nltk.word_tokenize(wholePaper);

from nltk.corpus import wordnet

for word in sepWords:
    synSet = wordnet.synsets(word);
    if(len(synSet) > 0):
        rIdx = random.randint(0, len(synSet) - 1);
        print synSet[rIdx].name.split('.')[0]
        stegText.write(synSet[rIdx].name.split('.')[0] + ' ');
    else:
        stegText.write(word + ' ');

print 'done'

origText.close();
stegText.close();
