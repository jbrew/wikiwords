import nltk
import wikiwords
import random
from model import librarian
from model import dictionary
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


"""
Playing with context-free grammars in nltk

http://www.nltk.org/howto/generate.html

"""

def word_frequency_by_pos(pos_tagged):
	"Returns occurrence rates by part-of-speech"
	pos_dictionary = {}
	for tok, tag in pos_tagged:
		if tag in pos_dictionary:
			if tok in pos_dictionary[tag]:
				pos_dictionary[tag][tok] += 1
			else:
				pos_dictionary[tag][tok] = 1
		else:
			pos_dictionary[tag] = {tok: 1}
	return pos_dictionary

def grammar_from_tagged(pos_tagged):

	# grammar mapping symbols to their productions
	grammar = {}

	pos_dict = word_frequency_by_pos(pos_tagged)

	nouns = list(pos_dict['NN'].keys())
	adjectives = list(pos_dict['JJ'].keys())
	verbs = list(pos_dict['VBZ'].keys())
	#determiners = list(pos_dict['DT'].keys())
	#prepositions = list(pos_dict['IN'].keys())

	# non-terminal symbols
	grammar['S'] = {'NP VP': 1}
	grammar['NP'] = {'JJ NP': 1, 'N': 1, 'NP PP': 1}
	grammar['PP'] = {'P NP': 1}
	grammar['VP'] = {'VBG NP': 1, 'VBG JJ': 1}

	# terminal symbols
	grammar['N'] = {k: 1 for k in nouns}
	grammar['JJ'] = {k: 1 for k in adjectives}
	#grammar['Det'] = {'the': 1, '': 1}
	grammar['P'] = {'with': 1, 'of': 1, 'for': 1}
	grammar['VBG'] = {k: 1 for k in verbs}

	return grammar

def pos_grammar_from_tagged(pos_tagged):

	grammar = {}
	pos_dict = word_frequency_by_pos(pos_tagged)

	grammar['NP'] = {'Adj NP': 1, 'Noun': 1, 'Noun Verb NP': 1}#, 'NP PP': 1}
	#grammar['PP'] = {'P NP': 1}
	grammar['VP'] = {'Verb NP': 1, 'Verb Adj': 1}

	grammar['Noun'] = {'NN': 1}
	grammar['Adj'] = {'JJ': 1}
	#grammar['P'] = {'with': 1, 'of': 1, 'for': 1}
	grammar['Verb'] = {'VBG': 1}
	return grammar

def expand(symbol, grammar, depth=0, max_depth=5):
	if depth > max_depth:
		return ""
	else:
		if not symbol in grammar:
			return symbol
		else:
			options = list(grammar[symbol].keys())
			expansion = random.choice(options)
			tokens_to_expand = expansion.split()
			# if len(tokens_to_expand) > max_length:
			# 	return ""
			#else:
			return " ".join([expand(symbol, grammar, depth+1) for symbol in tokens_to_expand])		# recursive call




def word_to_pos_dict(tagged_words, threshold = 0.3):
	"For each word, returns the POS tags it receives at least [threshold] of the time"

	word_to_pos_dict = {}

	for token, tag in tagged_words:
		word = token.lower()
		if word in word_to_pos_dict:
			if tag in word_to_pos_dict[word]:
				word_to_pos_dict[word][tag] += 1
			else:
				word_to_pos_dict[word][tag] = 1
		else:
			word_to_pos_dict[word] = {tag: 1}

	normalized = {k: dictionary.normalize(d) for k, d in word_to_pos_dict.items()}
	#print(normalized['acronym'])
	oddballs_removed = {k: dictionary.clears_threshold(d, threshold) for k, d in normalized.items()}
	return {k: dictionary.normalize(d) for k, d in oddballs_removed.items()}


def pos_tagged_from_text(text):
	tokens = [word.strip() for word in nltk.word_tokenize(text) if not '.' in word and not '==' in word]
	return nltk.pos_tag(tokens)


### TESTS ###



def grammar_test():
	text = librarian.text_from_path('texts/Book.txt')
	tokens = [word.strip() for word in nltk.word_tokenize(text) if not '.' in word and not '==' in word]
	pos_tagged = nltk.pos_tag(tokens)
	grammar = pos_grammar_from_tagged(pos_tagged)
	print(expand('NP', grammar))



if __name__ == '__main__':
	grammar_test()
	#pos_dict_test()



