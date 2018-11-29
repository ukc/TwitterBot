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



def generate_tweet(tag_index1, query_value1, tag_index2, query_value2, templet, solr):
	answer_prefix1 = []
	answer_suffix1 = []
	answer_prefix2 = []
	answer_suffix2 = []
	answer_prefix1.append(query_value1)
	answer_suffix1.append(query_value1)
	answer_prefix2.append(query_value2)
	answer_suffix2.append(query_value2)
	

	j=0
	for i in range(tag_index1):
		found = 0
		results = search(solr, answer_prefix1[-1], query_value1, "second:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["first"]),tagset="universal") 
			if temp[0][1]==templet[tag_index1-(j+i)-1]:
				answer_prefix1.append(result["first"].encode("utf-8"))
				query = "second: "+result["first"]
				found = 1
				j = 0
				break
		if found == 0 :
			i=i+1
			j=2

	j=0
	for i in range(tag_index1+1,(tag_index1+tag_index2)/2):
		found = 0
		results = search(solr, answer_suffix1[-1], query_value1, "first:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["second"]),tagset="universal") 
			if temp[0][1]==templet[(j+i)]:
				answer_suffix1.append(result["second"].encode("utf-8"))
				query="first: "+result["second"]
				found=1
				j=0
				break
		if found == 0 :
			i=i+1
			j=0


	j=0
	for i in range((tag_index1+tag_index2)/2, tag_index2):
		found = 0
		results = search(solr, answer_prefix2[-1], query_value2, "second:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["first"]),tagset="universal") 
			if temp[0][1]==templet[tag_index2-(j+i)-1]:
				answer_prefix2.append(result["first"].encode("utf-8"))
				query = "second: "+result["first"]
				found = 1
				j = 0
				break
		if found == 0 :
			i=i+1
			j=2

	j=0
	for i in range(tag_index2+1,len(templet)):
		found = 0
		results = search(solr, answer_suffix2[-1], query_value2, "first:")	
		for result in results:
			temp =  nltk.pos_tag(nltk.word_tokenize(result["second"]),tagset="universal") 
			if temp[0][1]==templet[(j+i)]:
				answer_suffix2.append(result["second"].encode("utf-8"))
				query="first: "+result["second"]
				found=1
				j=0
				break
		if found == 0 :
			i=i+1
			j=0

	answer_prefix1.pop(0)	
	answer1 =  list(reversed(answer_prefix1)) + answer_suffix1
	answer_prefix2.pop(0)	
	answer2 =  list(reversed(answer_prefix2)) + answer_suffix2
	newtweet = ""
	answer = answer1 + answer2
	newtweet = ""
	for word in answer:
		newtweet += word + ' '
	
	print newtweet
	tweetfile = open("tweets.txt", "a+")
	tweetfile.write('query words: %s and %s\n%s\n\n' % (query_value1, query_value2, newtweet))




def search(solr, searching_word, query_value, option):	
	if searching_word in escapeRules:
		searching_word = escapeRules[searching_word]
	results = solr.search(option + searching_word, rows=50)
	if len(results) == 0:
		results = solr.search(option + query_value)
	return results





def find_tag_index(template, tag, start=0):
	 for i in range(start,len(template)):
		if template[i] == tag:
			return i




def main():
	
	if len(sys.argv) <= 1:
		print 'qwery word 1 not given. write query word'
		query_value1 = raw_input("query word 1 : ")		
	else:
 		query_value1 = sys.argv[1]
	
	if len(sys.argv) <= 2:
		print 'qwery word 2 not given. write query word'
		query_value2 = raw_input("query word 2 : ")		
	else:
 		query_value2 = sys.argv[2]

	query_value1 = query_value1.lower()
	query_value2 = query_value2.lower()
	solr = pysolr.Solr('http://localhost:8983/solr/tweetBigram_index', timeout=10)

	print "query word1", query_value1
	print "query word2", query_value2	
	pos_templet = "DET ADV NOUN VERB DET ADJ NOUN ADP DET NOUN VERB DET ADJ NOUN ADP DET NOUN"
	templet = nltk.word_tokenize(pos_templet)
	temp1 = nltk.pos_tag(nltk.word_tokenize(query_value1),tagset="universal")
	temp2 = nltk.pos_tag(nltk.word_tokenize(query_value2),tagset="universal")
	tag1 = temp1[0][1]
	tag2 = temp2[0][1]
	tag_index1 = find_tag_index(templet, tag1)

	if tag_index1 is not None:
			tag_index2 = find_tag_index(templet, tag2, tag_index1+1)
	else:
		tag_index2 = find_tag_index(templet, tag2)

	if tag_index1 is not None and tag_index2 is not None:
		generate_tweet(tag_index1, query_value1, tag_index2, query_value2, templet, solr)
	else:
		print "Required tweet cannot be generated"

if __name__ == '__main__':
	main()
