import nltk
import random
import math
from nltk.corpus import wordnet
import re
import requests

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
                for start in range(max(0, center - n + 1), 
                                   min(center + 1, len(sentence) - n + 1))]

def score(sentence, i):
    word_score = 0
    for n in range(2, 6):
        sentence_ngrams = ngrams(sentence, n, i)
        t = total_frequency(sentence_ngrams)
        if t == 0:
            break
        word_score += math.log(max(1, t))
    return word_score

def oldscore(sentence, i):
    word_score = 0
    for j in range(2, 6):
        sentence_ngrams = ngrams(sentence, j, i)
        temp_score = 0
        for k in range(0, len(sentence_ngrams)):
            temp_score += frequency(sentence_ngrams[k])
        if (temp_score <= 0):
            break
        word_score += math.log(temp_score)
    return word_score

def total_frequency(ngrams):
    url = "https://books.google.com/ngrams/graph?content=" + \
          "%2C".join(["+".join(ngram) for ngram in ngrams]) + \
          "&case_insensitive=on&year_start=1999&year_end=2000&corpus=15&smoothing=0"
    html = requests.get(url).text
    m = re.findall('(\d\.(\d)+e\-\d\d)\], "parent": ""', html)
    return sum([float(match[0]) * 11190986329.0 for match in m])

def frequency(ngram):
    if ngram == []:
        return 0
    url = "https://books.google.com/ngrams/graph?content=" + \
          "+".join(ngram) + \
          "&case_insensitive=on&year_start=1999&year_end=2000&corpus=15&smoothing=3"
    html = requests.get(url).text
    r = re.compile('.*(\d\.(\d)+e\-\d\d)\], "parent": "".*', re.DOTALL)
    m = r.match(html)
    if m:
        return float(m.group(1)) * 11190986329.0
    else:
        return 0

def best_synonym(sentence, i):
    (best_syn, best_score) = best(lambda syn: score(replace(sentence, i, syn), i),
                                  synonyms(sentence[i]))
    if best_syn == None:
        return sentence[i]
    else:
        return (best_syn, best_score)

def viable_synonyms(sentence, i):
	syn_list = synonyms_with_scores(sentence, i)
	max_count = 0
	possible_syns = [];
	for syn in syn_list:
		if syn[1] > max_count:
			max_count = syn[1]
	if max_count == 0:
		print "could not connect to Google"
		return
	for syn in syn_list:
		syn[1] /= max_count
		if syn[1] > .85: # this is the threshold check. it should probably be global or something?
			possible_syns.append(syn[0])
	return possible_syns

def synonyms(word):
    syns = []
    for synset in wordnet.synsets(word):
        syns += synset.lemma_names
    return list(set(syns)) # remove duplicates

def synonyms_with_scores(sentence, i):
    return [[syn, score(replace(sentence, i, syn), i)]
            for syn in synonyms(sentence[i])]

def best(fn, lst):
    if lst == []:
        return None
    else:
        winner = lst[0]
        max_score = fn(winner)
        for obj in lst[1:]:
            score = fn(obj)
            if score > max_score:
                winner = obj
                max_score = score
        return (winner, max_score)

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

# def contains_sublist(lst, sublst):
#     n = len(sublst)
#     return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))
#
# def oldfrequency(ngram):
#     """The frequency of any ngram in the corpus."""
#     if ngram == []:
#         return 0
#     else:
#         return len([s for s in brown.sents() if contains_sublist(s, ngram)])
