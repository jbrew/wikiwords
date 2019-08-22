import wikipedia
import wikiquote
from model import librarian
from model import dictionary
import os



def get_page_from_search_term(term):
	"""
	returns the top search result if there are any
	otherwise, returns the string 'No search results found!'
	"""
	search_results = wikipedia.search(term)
	
	if len(search_results) == 0:
		return 'No search results found!'
	else:
		top_result = search_results[0]
		p = get_page_by_title(top_result)
		return p

def text_from_search_term(term):
	"""
	returns the text of the page up to the header for the References section
	"""
	page = get_page_from_search_term(term)
	return page.content.split('== References ==')[0]


def get_page_by_title(title):
	try:
		p = wikipedia.page(title)
	except wikipedia.exceptions.DisambiguationError as err:
		p = wikipedia.page(err.options[0])
	return p


def print_to_file(page, savepath):
	with open(savepath, 'w') as f:
		
		f.write(page.content.split('== References ==')[0]) # everything before the references section
		#f.write('\n==== LINKS ====\n')
		#f.write('\n'.join(page.links))

def get_stopwords():
	"""
	loads a list of very common "stopwords" to ignore in listing keywords
	"""
	with open('resources/stopwords.txt') as f:
		return set([line.strip() for line in f.readlines()])


def get_keywords(search_term):
	"""
	get the scored keywords for the search term's page,
	then just return the top words without their scores
	"""
	keywords_and_scores = keywords_with_scores(search_term)
	return [keyword for keyword, score in keywords_and_scores]

def keywords_with_scores(search_term):
	"""
	for a given search term, computes the tf-idf score for words in the associated article
	relative to an existing library of wikipedia articles

	returns a list of (keyword, score) tuples
	"""

	# convert to title case
	lookup_name = search_term[0].upper() + search_term[1:].lower() + '.txt'

	if lookup_name in os.listdir('texts'):
		savename = lookup_name
	else:
		page = get_page_from_search_term(search_term)
		print('finding keywords for',page.title)
		savename = page.title + '.txt'

	savepath = 'texts/' + savename

	if not os.path.exists(savepath):
		print_to_file(page, savepath)

	tf_dict = librarian.term_frequency_dict_by_name('texts', savename)
	
	tf_dicts = librarian.term_frequency_dicts_from_directory('texts')
	df_dict = librarian.document_frequency_dict_from_tf_dicts(tf_dicts)
	
	keywords = librarian.keywords(tf_dict, df_dict, tf_dicts)
	stopwords = get_stopwords()

	return [(kword, score) for kword, score in keywords if not kword in stopwords]


def get_keywords_from_file_and_directory(filepath, dirpath):
	"""
	compute the tf-idf keywords for terms in a given file, relative
	to all files in a given directory (not necessarily containing the file, though it can)
	"""

	with open(filepath) as f:
		filetext = f.read()
	tf_dict = librarian.term_dict(filetext)
	tf_dicts = librarian.term_frequency_dicts_from_directory(dirpath)
	df_dict = librarian.document_frequency_dict_from_tf_dicts(tf_dicts)
	keywords = librarian.keywords(tf_dict, df_dict, tf_dicts)
	stopwords = get_stopwords()
	keywords = [kword for kword, score in keywords if not kword in stopwords]
	return keywords

def search(requested):
	return wikiquote.search(requested)

def quotes_from_page(page, n=1000):
	return wikiquote.quotes(page, max_quotes=n)

### TESTS ###

def keyword_test():
	print(get_keywords('toast'))
	print(get_keywords('high jump'))


if __name__ == '__main__':
	while True:
		next_term = input('Enter next term:\n')
		if next_term in ['n','no','N','NO','q','x','z']:
			break
		else:
			print(get_keywords(next_term))






