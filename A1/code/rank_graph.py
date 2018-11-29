# -*- coding: utf-8 -*-
import nltk
import string
import matplotlib.pyplot as plt
from nltk.util import ngrams
from operator import itemgetter
from collections import OrderedDict


stopwords = ['', '(', ')', '{', '}', '\\', '--', ':']
noOfProcessedLines = 0
tokens=list()

with open('../data/processed_data.txt') as inpFile:
    for line in inpFile:
        noOfProcessedLines += 1
        if (noOfProcessedLines % 10000 == 0):
            print noOfProcessedLines, " lines processed.."
        line = line.rstrip()
        if line == '':
            continue
        # tokens.append('<s>')
        for word in nltk.word_tokenize(line):
            if word not in stopwords :#and d.check(word)==True:
                tokens.append(word)

      
def n_grams():
    unigram=[w.strip(string.punctuation).lower() for w in tokens]
    unigram=[w for w in unigram if not w in stopwords]
    bigram =[a for a in ngrams(unigram,2)]
    trigram =[a for a in ngrams(unigram,3)]
    return unigram, bigram, trigram
    
unigram, bigram, trigram = n_grams()

def rank_graph(n_gram):
    frequency=nltk.FreqDist(n_gram)
    sorted_freq=OrderedDict(reversed(sorted(frequency.items(), key = itemgetter(1))))
    term_index={}
    freq_ngram=[]
    for i, key in enumerate(sorted_freq):
        term_index[i]=key
        freq_ngram.append(sorted_freq[key])
    plt.scatter(list(term_index.keys()), freq_ngram, color="orange", marker="*")
    index=0;
    for i,key in enumerate(sorted_freq):
        print key
	index+=1
	if(index==10):
	    break;
    plt.title('freq_dist')
    plt.savefig('../freq_dist.png')
    print 'Top 10 bigrams'

    return term_index, freq_ngram 
    
term_index, freq_ngram=rank_graph(bigram)
