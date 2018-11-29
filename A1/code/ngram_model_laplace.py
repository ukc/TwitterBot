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

split_tokens =int(90 * len(tokens)/100)
train_corpus = tokens[:split_tokens]
test_corpus = tokens[split_tokens:]

freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)
vocab=len(set(train_corpus))

def unigram_prob_with_add1smoothing(word):
	val = float( freq_1gram[word] + 1)/(len_brown + vocab)
	return val

cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens, pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>"))
cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)

def bigram_prob_with_add1smoothing(word1, word2):
	cprob_2gram_add1=float((((float)(1+cfreq_2gram[word1][word2])/(len(cfreq_2gram)+sum(cfreq_2gram[word1].values())))))
	return cprob_2gram_add1


trigrams_as_bigrams=[]
trigram =[x for x in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]
trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigram])

cfreq_3gram = nltk.ConditionalFreqDist(trigrams_as_bigrams)
cprob_3gram = nltk.ConditionalProbDist(cfreq_3gram, nltk.MLEProbDist)

def trigram_prob_with_add1smoothing(w1, w2, w3):
	cprob_3gram_add1=float((((float)(1+cfreq_3gram[(w1,w2)][w3])/(len(cfreq_3gram)+sum(cfreq_3gram[(w1,w2)].values())))))
	return cprob_3gram_add1


def entropy(n, text):
        entropy = 0.0
        text = ["<s>"] + text + ["</s>"]
        for i in range(n - 1, len(text)):
            context = text[i - n + 1:i]
            token = text[i]
            entropy += logprob(token, context)
        return entropy / float(len(text) - (n - 1))


def logprob(word, context):
    if len(context)==0:
        prob = unigram_prob_with_add1smoothing(word)
    elif len(context)==1:
        prob = bigram_prob_with_add1smoothing(context[0], word)
    else:
        prob = trigram_prob_with_add1smoothing(context[0], context[1], word)
    if(prob == 0):
        return 0
    else:
        return -prob * log(prob , 2)


def perplexity(n, text):
      return pow(2.0, entropy(n, text))

entropy_value_2gram = entropy(2, test_corpus)
entropy_value_3gram = entropy(3, test_corpus)
perp_value_2gram = perplexity(2, test_corpus)
perp_value_3gram = perplexity(3, test_corpus)
print "Perplexity for bigram using Laplace: \t", perp_value_2gram
print "Perplexity for trigram using Laplace:\t", perp_value_3gram

fp = open("../report.txt", "w")
fp.write("Perplexity for bigram using Laplace: \t"+str(perp_value_2gram)+"\n")
fp.write("Perplexity for trigram using Laplace:\t"+str(perp_value_3gram)+"\n\n")
fp.close()
