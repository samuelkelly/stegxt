import nltk
import random
import math
from nltk.corpus import wordnet
from nltk.corpus import brown

def synset_to_word(ss):
    return ss.name.split('.')[0]

def replace(sentence, index, replword):
    new_sentence = sentence[:]
    new_sentence[index] = replword
    return new_sentence
	
def ngrams(sentence, n, center):
    if n > len(sentence):
        return [[]]
    elif n == len(sentence):
        return [sentence[:]]
    else:
        return [sentence[start:start+n] 
                for start in range(max(0, center - n + 1), min(center + 1, len(sentence) - n + 1))]

def score(sentence, i):
    return sum( [math.log(max(1, frequency(ng))) # 0 occurences contributes 0 to score
                 for n in range(2,6)
                 for ng in ngrams(sentence, n, i)] )

def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))

def frequency(ngram):
    """The frequency of any ngram in the corpus."""
    if ngram == []:
        return 0
    else:
        return len([s for s in brown.sents() if contains_sublist(s, ngram)])

def best_synonym(sentence, i):
    max_score = 0
    for synonym in list_syn(sentence[i]):
        s = score(replace(sentence, i, synonym), i)
        if s > max_score:
            max_score = s
            best_syn = synonym
    if max_score == 0:
        return sentence[i]
    else:
        return best_syn

if __name__ == "__main__":
    orig_text = open('warofroses.txt', 'r');
    steg_text = open('warofposes.txt', 'w');

    words = nltk.word_tokenize(orig_text.read())

    for word in words:
        synsets = wordnet.synsets(word)
        if len(synsets) > 0:
            rand_idx = random.randint(0, len(synsets) - 1)
            rand_synset = synsets[rand_idx]
            #print synset_to_word(rand_synset)
            steg_text.write(synset_to_word(rand_synset) + ' ')
        else:
            steg_text.write(word + ' ')

    print 'done'

    orig_text.close()
    steg_text.close()
