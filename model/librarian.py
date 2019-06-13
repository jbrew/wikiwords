import csv
import os
import math
from . import dictionary
from . import texthandler
from itertools import islice
import string

punctuation = ['.', ',', '!', '?', '(', ')', '$', ':', ';', '{', '}', '[', ']', '•', '|']


def text_from_path(path):
	with open(path) as f:
		return f.read()

def text_from_directory(dirpath):
	text = ''
	for fname in os.listdir(dirpath)[1:]:
		fpath = '%s/%s' % (dirpath, fname)
		text += text_from_path(fpath)
	return text


def clean_all(lines):
	return [remove_punctuation(line.strip()) for line in lines]

def filter_characters(lines, characters):
	char_set = set(characters)
	return [line for line in lines if none_in(line, char_set)]

def in_size_range(lines, min_length=20, max_length=20):
	"""
	return lines whose size is within the given range
	"""
	return [line for line in lines if len(line) > min_length and len(line) < max_length]


def none_in(line, character_set):
	for c in line:
		if c in character_set:
			return False
	return True

def term_frequency_dict_by_name(dirpath, name):
	all_files = get_data_from_directory(dirpath, headers=['name','text'])
	for rowname, rowtext in all_files:
		if rowname == name:
			return term_dict(rowtext)
	return None

def term_frequency_dicts_from_directory(dirpath):
	all_files = get_data_from_directory(dirpath, headers=['name','text'])
	all_text = all_text_from_column(all_files, 'text')
	tds = [term_dict(text) for name, text in all_files]
	return tds


def document_frequency_dict_from_tf_dicts(tf_dicts):
	big_td = dictionary.union(tf_dicts)	# one term dictionary for all documents
	doc_frequency_dict = df_dict(big_td, tf_dicts, threshold=1)

	return doc_frequency_dict


def lines_from_lyrics_directory(dirpath):
	text_files = get_data_from_directory(dirpath, headers=['name','text'])
	lines = [remove_punctuation(line.strip().lower()) for line in get_all_lines(text_files) if len(line.strip()) > 0]
	lines = sanitize(lines)
	return lines

def sanitize(lines):
	"""
 	remove bad words using this list:
	https://github.com/dariusk/wordfilter/blob/master/lib/badwords.json
	"""
	with open('resources/badwords.txt') as f:
		badwords = set([line.strip() for line in f.readlines()]) | set([line.strip() + 's' for line in f.readlines()])

	lines = [line for line in lines if is_clean(line, badwords)]
	return lines


def get_all_lines(text_files):
	lines = []
	for name, text in text_files:
		lines.extend(text.split('\n'))
	return lines

def is_clean(line, badwords):
	words = line.split()
	for w in words:
		if w in badwords:
			return False
	return True




### LINES AND SENTENCES ###


def lines_from_file(fpath):
	with open(fpath) as f:
		lines = f.readlines()
		return sanitize(lines)

def lines_from_directory(dirpath):
	lines = []
	for fname in os.listdir(dirpath)[1:]:
		fpath = '%s/%s' % (dirpath, fname)
		lines.extend(lines_from_file(fpath))
	return lines

def sentences_from_file(filepath):
	with open(filepath) as f:
		text = f.read()
		return texthandler.split_into_sentences(text)

def fragments_from_file(filepath):
	with open(filepath) as f:
		text = f.read()
		return texthandler.split_into_sentences(text.replace(',','.'))

def sentences_from_directory(dirpath):
	sentences = []
	for fname in os.listdir(dirpath)[1:]:
		print(fname)
		fpath = '%s/%s' % (dirpath, fname)
		with open(fpath) as f:
			text = f.read()
			sentences.extend(texthandler.split_into_sentences(text))
	return sentences

def sentences_from_TED_file(fpath):
	with open(fpath) as f:
		text = f.read()
		sentences = [s.replace('\n',' ') for s in text.split('.\n')]
		return sentences

def sentences_from_TED_directory(dirpath):
	sentences = []
	for fname in os.listdir(dirpath)[1:]:
		fpath = '%s/%s' % (dirpath, fname)
		sentences.extend(sentences_from_TED_file(fpath))
	return sentences




def get_data(path, n=100000):
	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		rows = [row for row in islice(csv_reader,0,n)]
		return rows

def get_data_from_tab_delimited(path, n=100000, headers=None):
	with open(path) as f:
		next(f)
		reader=csv.reader(f,delimiter='\t')
		rows = [row for row in islice(reader,0,n)]
	if headers:
		rows.insert(0, headers)	# prepend to list
	return rows

# directory of only text files (NOTE: In future, consider scraping to CSV instead)
def get_data_from_directory(dirpath, headers=['','']):
	rows = [headers]
	for filename in os.listdir(dirpath):
		if os.path.isdir(filename):
			return "directory must only contain text files"
		if not dirpath[-1] == '/':
			dirpath += '/'
		filepath = dirpath+filename
		with open(filepath) as f:
			try:
				text = f.read()
				rows.append([filename, text])
			except:
				pass
	return rows


# remove any dictionaries with suspiciously similar profiles
def eliminate_duplicates(tds, threshold=.9):
	if len(tds) == 0:
		return []
	else:		
		head = tds[0]
		remainder = tds[1:]
		if list_contains_duplicate(head, remainder, threshold):
			return eliminate_duplicates(remainder, threshold)
		else:
			return [head] + eliminate_duplicates(remainder, threshold)

# given a dictionary and a list of dictionaries, returns whether any is a duplicate
def list_contains_duplicate(d, dlist, threshold=.9):
	for head in dlist:
		if dictionary.similarity(d, head) > threshold:
			return True
	return False



def all_text_from_column(rows, col_name):

	if col_name in rows[0]:
		n = rows[0].index(col_name)
		return '\n'.join([row[n] for row in rows[1:]])
	else:
		return ''


def remove_punctuation(text):
	exclude = set(string.punctuation)
	return ''.join(ch for ch in text if ch not in exclude)


# a dictionary of all terms in the document of length 1
def term_dict(doc):
	term_dict = {}
	words = [remove_punctuation(w.strip().lower()) for w in doc.split()]
	for word in words:
		if word in term_dict:
			term_dict[word] += 1
		else:
			term_dict[word] = 1
	return term_dict

# a list of dictionaries of terms in the document of length n
def term_dicts(corpus):
	return [term_dict(d) for d in corpus]

# returns lower and upper bounds containing 95 percent of occurrence rates of the term
def tf_bounds(term, tds, n=2):
	distribution = frequency_distribution(term, tds)
	m = mean(distribution)
	sd = stdev(distribution)
	return m - n*sd, m + n*sd

# returns terms in a dictionary that occur in at least two (or n) dictionaries from a list of dictionaries
def non_unique_terms(term_dict, dict_list, n=1):
	return {k: v for k, v in term_dict.items() if doc_frequency(k, dict_list) >= n}


# how many documents in the corpus include the term
def doc_frequency(term, term_dicts):
	return len([1 for td in term_dicts if term in td])

# returns a dictionary of document frequencies (df) for all terms in the dictionary list
# only includes terms with a df of at least n
def df_dict(term_dict, dict_list, threshold=1):
	to_return = {}
	for k, v in term_dict.items():
		df = doc_frequency(k, dict_list)
		if df >= threshold:
			to_return[k] = df
	return to_return



#### SEARCH ####

# takes a list of docs and a corresponding (equal length) list of term dicts
def docs_containing_term(term, docs, term_dicts):
	return [docs[i] for i, td in enumerate(term_dicts) if term in td]


### LOAD RESOURCES ###

def stopwords():
	with open('resources/stopwords.txt') as f:
		return set(f.read().split('\n'))



### STATISTICAL METHODS ####

# standard deviation
def stdev(values):
	N = len(values)
	mean = sum(values) / N
	sum_squared_differences = sum([(x-mean)**2 for x in values])
	return math.sqrt(sum_squared_differences / (N-1))

def mean(values):
	return sum(values) / len(values)




#### SAVING DICTIONARIES ####

def save_ngrams_from_field(docs, field, n, dirname='NO DIR', dup_threshold=.8):
	text = all_text_from_column(docs,field)
	tds = term_dicts(text,n)		# one term dictionary per document
	unique_tds = eliminate_duplicates(tds, threshold=dup_threshold)
	big_td = dictionary.union(unique_tds)	# one term dictionary for all documents

	to_save = df_dict(big_td, unique_tds, threshold=2)
	print(len(to_save))
	dirpath = 'stats/%s/' % dirname
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	filename = '%s_%sg_df.txt' % (field.lower(), n)
	savepath = dirpath + filename
	dictionary.to_tab_delimited(to_save, savepath)

def process_directory(dirname, dup_threshold=.8):
	dirpath = 'data/%s' % dirname
	savepath = 'stats/%s/' % dirname

	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	if not os.path.exists(savepath):
		os.mkdir(savepath)

	rows = get_data_from_directory(dirpath, headers=['Filename','Songtext'])

	for n in range(1, 6):
		save_ngrams_from_field(rows, 'Songtext', n, dirname=dirname, dup_threshold=dup_threshold)




# arranges documents into groups of a given size
def group_into_documents(small_docs, group_size):

	num_docs = len(small_docs)

	new_docs = ['' for x in range(num_docs//group_size)]

	for doc_index in range(len(new_docs)):
		for i in range(group_size):
			full_index = doc_index*group_size+i
			new_docs[doc_index] += small_docs[full_index] + '\n'
	return new_docs

# returns a list of keywords for the doc in the context of the corpus
def keywords(tf_dict, df_dict, tf_dicts):

	total_docs = len(tf_dicts)

	tfidfs = {k: tfidf(k, tf_dict, df_dict, total_docs) for k in tf_dict.keys()}

	return dictionary.sort_descending(tfidfs)

def tfidf(k, tf_dict, df_dict, total_docs):
	tf = tf_dict[k]
	df = df_dict[k]
	idf = -1 * math.log(df/total_docs)
	return tf*idf

