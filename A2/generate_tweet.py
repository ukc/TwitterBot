import pysolr
import random
import sys

TWEET_LENGTH = 10

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
		searching_word = query_value
	results = solr.search(option + searching_word)
	if len(results) == 0:
		results = solr.search(option + query_value)
	return results


def main():
	
	if len(sys.argv) <= 1:
		print 'qwery word not given. write query word'
		query_value = raw_input("query word : ")		
	else:
 		query_value = sys.argv[1]
	solr = pysolr.Solr('http://localhost:8983/solr/tweetBigram_index', timeout=10)

	print "query word", query_value
	answer_prefix = []
	answer_suffix = []
	answer_prefix.append(query_value)
	answer_suffix.append(query_value)
	for i in range(TWEET_LENGTH+1) or len(answer_prefix) + len(answer_suffix) <= TWEET_LENGTH:
		if i%2 == 0:
			results = search(solr, answer_prefix[-1], query_value, "second:")
			rand = random.randint(0, len(results))
			for j,result in enumerate(results):
				if j == rand:
					answer_prefix.append(result['first'].encode("utf-8"))
					break

		else:
			results = search(solr, answer_suffix[-1],query_value, "first:")
			rand = random.randint(0, len(results))
			for j,result in enumerate(results):
				if j == rand:
					answer_suffix.append(result['second'].encode("utf-8"))
					break
		
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
