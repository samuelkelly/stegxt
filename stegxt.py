import nltk
import random
from nltk.corpus import wordnet

def synset_to_word(ss):
    return ss.name.split('.')[0]

orig_text = open('warofroses.txt', 'r')
steg_text = open('warofposes.txt', 'w')

words = nltk.word_tokenize(orig_text.read())

for word in words:
    synsets = wordnet.synsets(word)
    if len(synsets) > 0:
        rand_idx = random.randint(0, len(synsets) - 1)
        rand_synset = synsets[rand_idx]
        print synset_to_word(rand_synset)
        steg_text.write(synset_to_word(rand_synset) + ' ')
    else:
        steg_text.write(word + ' ')

print 'done'

orig_text.close()
steg_text.close()
