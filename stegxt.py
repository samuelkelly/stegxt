import nltk
import random
from nltk.corpus import wordnet
from nltk.corpus import brown

def synset_to_word(ss):
    return ss.name.split('.')[0]

def replace(sentence, index, replword):
    new_sentence = sentence[:]
    new_sentence[index] = replword
    return new_sentence
	
def ngrams(sentence, n, i):
    list_of_phrases = []
    for j in range(0, n):
        list_of_phrases.append(sentence[j + i - n + 1:j + i + 1])
	
    return filter(lambda phrase: phrase != [], list_of_phrases)
	
def score(sentence, i):
	word_score = 0
	for j in range(2, 6):
		sentence_ngrams = ngrams(sentence, j, i)
		temp_score = 0
		for k in range(0, len(sentence_ngrams)):
			temp_score += frequency(sentence_ngrams[k])
		word_score += log(temp_score)
	return word_score
	
def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))

def frequency(ngram):
    return len([s for s in brown.sents() if contains_sublist(s, ngram)])

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
