import wikipedia
import wikiquote
from model import librarian
from model import dictionary
import os

def get_page_from_search_term(term):
	search_results = wikipedia.search(term)
	
	if len(search_results) == 0:
		return 'No search results found!'
	else:
		top_result = search_results[0]
		p = get_page_by_title(top_result)
		return p

def text_from_search_term(term):
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
	with open('resources/stopwords.txt') as f:
		return set([line.strip() for line in f.readlines()])


# get the words that occur in wikipedia articles about this topic but not others
def get_keywords(search_term):
	keywords_and_scores = keywords_with_scores(search_term)
	return [keyword for keyword, score in keywords_and_scores]

def keywords_with_scores(search_term):
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
	keyword_test()
	






