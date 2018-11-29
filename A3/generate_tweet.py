import pysolr
import random
import sys
import nltk

escapeRules = {'+': r'\+',
               '-': r'\-',
               '&': r'\&',
               '|': r'\|',
               '!': r'\!',
               '(': r'\(',
               ')': r'\)',
               '{': r'\{',
               '}': r'\}',
               '[': r'\[',
               ']': r'\]',
               '^': r'\^',
               '~': r'\~',
               '*': r'\*',
               '?': r'\?',
               ':': r'\:',
               '"': r'\"',
               ';': r'\;',
               ' ': r'\ ',
	       	   '/': r'\/',
	       	   '.': r'\.'}


def search(solr, searching_word, query_value, option):	
	if searching_word in escapeRules:
		searching_word = escapeRules[searching_word]
	results = solr.search(option + searching_word, rows=50)
	if len(results) == 0:
		results = solr.search(option + query_value)
	return results


def main():
	
	if len(sys.argv) <= 1:
		print 'qwery word not given. write query word'
		query_value = raw_input("query word : ")		
	else:
 		query_value = sys.argv[1]
	query_value = query_value.lower()
	solr = pysolr.Solr('http://localhost:8983/solr/tweetBigram_index', timeout=10)

	print "query word", query_value
	answer_prefix = []
	answer_suffix = []
	pos_templet = "DET ADV NOUN VERB DET ADJ NOUN ADP DET NOUN"
	templet = nltk.word_tokenize(pos_templet)
	temp = nltk.pos_tag(nltk.word_tokenize(query_value),tagset="universal")
	tag = temp[0][1]
	tag_index = templet.index(tag)
	answer_prefix.append(query_value)
	answer_suffix.append(query_value)

	j=0
	for i in range(tag_index):
		found = 0
		results = search(solr, answer_prefix[-1], query_value, "second:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["first"]),tagset="universal") 
			if temp[0][1]==templet[tag_index-(j+i)-1]:
				answer_prefix.append(result["first"].encode("utf-8"))
				query = "second: "+result["first"]
				found = 1
				j = 0
		    	break
		if found == 0 :
			i=i+1
			j=2
	
	j=0
	for i in range(tag_index+1,len(templet)):
		found = 0
		results = search(solr, answer_suffix[-1], query_value, "first:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["second"]),tagset="universal") 
			if temp[0][1]==templet[(j+i)]:
				answer_suffix.append(result["second"].encode("utf-8"))
				query="first: "+result["second"]
				found=1
				j=0
				break
		if found == 0 :
			i=i+1
			j=0


	answer_prefix.pop(0)	
	answer =  list(reversed(answer_prefix)) + answer_suffix
	newtweet = ""
	for word in answer:
		newtweet += word + ' '
	
	print newtweet
	tweetfile = open("tweets.txt", "a+")
	tweetfile.write('query word: %s\n%s\n\n' % (query_value, newtweet))

if __name__ == '__main__':
	main()
