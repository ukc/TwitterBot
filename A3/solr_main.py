import pysolr
import simplejson as json
import requests
from nltk.util import ngrams
from tokenizer import tokenizer
import timeit

start = timeit.default_timer()

T = tokenizer.TweetTokenizer(preserve_handles=False, preserve_hashes=False, preserve_case=False, preserve_url=False,regularize=True)



def update_solr_field(payload):
    base_url = 'http://localhost:8983/'
    solr_url = 'solr/test/'
    update_url = 'update?commit=true'
    full_url = base_url + solr_url + update_url
    headers = {'content-type': "application/json"}

    response = requests.post(full_url, data=json.dumps(payload), headers=headers)

    return response


def update_bigram_solr_field(payload):
    base_url = 'http://localhost:8983/'
    solr_url = 'solr/bigrams/'
    update_url = 'update?commit=true'
    full_url = base_url + solr_url + update_url
    headers = {'content-type': "application/json"}

    response = requests.post(full_url, data=json.dumps(payload), headers=headers)

    return response

try:
    solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
    count=0;
    unidata = [ ]
    bidata = []
    unigrams = dict()
    bigrams = dict()

    with open("corpusData") as corpusFile:
        for tweet in corpusFile:
            tokens=T.tokenize(tweet)
            bgrams=list(ngrams(tokens,2))
            for word in tokens:
                if( unigrams.has_key(word) ):
                    unigrams[word]+=1
                else:
                    unigrams[word]=1
            for words in bgrams:
                key=words[0]+"@#,"+words[1]
                if(bigrams.has_key(key)):
                    bigrams[key]+=1
                else:
                    bigrams[key]=1

            count+=1

            if count%10000 ==0:
                for key, value in unigrams.iteritems():
                    unidata.append( {"id":key,"token":key,"count":{"inc":value}} )
                for key, value in bigrams.iteritems():
                    bi=key.split("@#,")
                    first=bi[0]
                    second=bi[1]
                    bidata.append( {"id":key,"first":first,"second":second,"count":{"inc":value}} )
                update_solr_field(unidata)
                update_bigram_solr_field(bidata)

                unidata=[]
                bidata=[]
                unigrams=dict()
                bigrams=dict()

                print "{0} tweets processed...".format(count)

except Exception as e:
    print(e)

stop = timeit.default_timer()
print 'Runtime : '
print stop - start
