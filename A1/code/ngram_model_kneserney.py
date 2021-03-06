import nltk
import string
from nltk.util import ngrams
from math import log
from nltk.tokenize import TweetTokenizer

stopwords=['']
punctuation_list = [',','!','--','-','..',':)',';)','?',':D', '"', '(', ")", '[', ']']

corpus = open("../data/processed_data.txt", "r")
corpus = corpus.read()
corpus = corpus.lower()
corpus = corpus.translate(None, string.punctuation)

tweet_tokenizer = TweetTokenizer()
tokens = tweet_tokenizer.tokenize(corpus)

tokens = [w for w in tokens if not w in punctuation_list]

split_token =int(90 * len(tokens)/100)
train_corpus = tokens[:split_token]
test_corpus = tokens[split_token:]

freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)
vocab=len(set(train_corpus))

trigrams_as_bigrams=[]
trigram =[x for x in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]
trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigram])
cfreq_3gram = nltk.ConditionalFreqDist(trigrams_as_bigrams)
cprob_3gram=nltk.KneserNeyProbDist(nltk.FreqDist(trigram))

def trigram_prob(w1,w2,w3):
	return cprob_3gram.prob((w1,w2,w3))




def entropy(n, text):
        entropy = 0.0
        text = ["<s>"] + text + ["</s>"]
        for i in range(n - 1, len(text)):
            context = text[i - n + 1:i]
            token = text[i]
            entropy += logprob(token, context)
        return entropy / float(len(text) - (n - 1))


def logprob(word, context):
	if len(context)==2:
		prob = trigram_prob(context[0], context[1], word)
	if(prob == 0):
		return 0
	else:
		return -prob * log(prob , 2)

def perplexity(n, text):
	return pow(2.0, entropy(n, text))


entropy_value_3gram=entropy(3, test_corpus)
perp_value_3gram=perplexity(3, test_corpus)
print "Perplexity for trigram using Kneser Ney: ", perp_value_3gram

fp = open("../report.txt", "a")
fp.write("Perplexity for trigram using Kneser Ney:\t"+str(perp_value_3gram)+"\n\n")
fp.close()
