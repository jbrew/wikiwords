import wikiwords
import random
from model import command_line
import os
import cfg
from model import markov
from model import dictionary
from model import librarian

uppercase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
lowercase = set('abcdefghijklmnopqrstuzwxyz')


"""
This is command line program for filling in Backronyms.

"""

def fill_from_context_free_grammar(request, text, attempts=10000):

	pos_tagged = cfg.pos_tagged_from_text(text)
	grammar = cfg.pos_grammar_from_tagged(pos_tagged)
	pos_dict = cfg.word_frequency_by_pos(pos_tagged)
	pos_sequences = [cfg.expand('NP', grammar) for i in range(attempts)]
	
	correct_length_sequences = [sequence for sequence in pos_sequences if len(sequence.split())==len(request)]
	
	candidates = []

	for sequence in correct_length_sequences:
		scaffold = [None for i in range(len(request))]
		tags = sequence.split()
		for i, tag in enumerate(tags):
			words_with_tag = pos_dict[tag]
			words_with_initial = [word for word in words_with_tag if word[0] == request[i]]
			if len(words_with_initial) > 0:
				scaffold[i] = random.choice(words_with_initial)
		
		if not None in scaffold:
			candidates.append(scaffold)


	keywords = dict(wikiwords.keywords_with_scores(request.lower())[:150])
	markov_dict = markov.forward_dict(text)

	keyword_scores = [(candidate, score_by_keywords(candidate, keywords)) for candidate in candidates]
	markov_scores = [(candidate, score_by_markov(candidate, markov_dict)) for candidate in candidates]

	keyword_weight = 1
	markov_weight = 0

	candidates_scored_by_mixture = [(candidate, keyword_scores[i][1]*keyword_weight + markov_scores[i][1]*markov_weight) for i, candidate in enumerate(candidates)]

	return sorted(candidates_scored_by_mixture[:20], key=lambda x: x[1], reverse=True)



def score_by_keywords(candidate_sequence, keywords):
	"""
	candidate_sequence: a list of words
	keywords: a dictionary mapping keywords to scores
	"""
	return sum([keywords[word] for word in candidate_sequence if word in keywords])


def score_by_markov(candidate_sequence, markov_dict):
	cost = markov.transition_cost(" ".join(candidate_sequence), markov_dict)
	return 1/cost






def fill_from_text(request, text):
	"""
	Given a requested acronym, fill with sequences of words from the text.
	"""

	words = text.lower().split()
	initials = ''.join([word[0] for word in words])

	if len(request) == 0:
		return []
	else:
		for sequence_length in range(len(request), 0, -1):
			sequence = request[:sequence_length]
			if sequence in initials:
				start = initials.index(sequence)
				end = start + sequence_length
				word_sequence = [words[start:end]]
				word_sequence.extend(fill_from_text(request[sequence_length:], text))
				return word_sequence
		return 'Could not find'


def filter_by_letter(words, letter):
	return [word for word in words if word[0] == letter]

def fill_with_keywords_and_bridges(request, keywords, markov_dict):
	
	"""
	request: 		a string of uppercase and lowercase letters and underscores
					indicating which positions to fill with keywords (uppercase), fill with 
					bridge words (lowercase) or leave alone (underscores)
	keywords:		a list of topical keywords
	markov_dict:	a dictionary mapping contexts to continuations
	"""

	scaffold = []

	for letter in request:
		if letter in uppercase:
			candidates = filter_by_letter(keywords, letter.lower())
			if len(candidates) > 0:
				scaffold.append(random.choice(candidates))
			else:
				scaffold.append(None)
		else:
			scaffold.append(None)

	for i, entry in enumerate(scaffold):

		if entry == None:
			candidates = [k for k in markov_dict.keys() if len(k) > 0 and len(k.split()) == 1 and k[0] == request[i]]
			bridges = markov.scored_bridges(scaffold[i-1], candidates, scaffold[i+1], markov_dict)
			top_bridges = dictionary.sort_ascending(bridges)[:10]
			scaffold[i] = random.choice(top_bridges)[0]

	return scaffold


### LOOPS ###


# keep getting backronyms until user breaks loop
def keywords_loop(request):
	text = wikiwords.text_from_search_term(request.lower())
	keywords = wikiwords.get_keywords(request.lower())[:150]
	print('first ten keywords:',keywords[:10])
	
	markov_dict = markov.forward_dict(text)
	
	while True:
		backronym = fill_with_keywords_and_bridges(request, keywords, markov_dict)
		capitalized = [word[0].upper() + word[1:] for word in backronym]
		print(" ".join(capitalized))

		if input('Find another backronym?\n') in ['no','n','NO', 'N']:
			break

# keep filling backronyms from text until user breaks loop
def text_loop(request):
	while True:
		options = os.listdir('texts')
		random.shuffle(options)
		fpath = 'texts/' + command_line.choose_from_list(options[:10])
		with open(fpath) as f:
			text = f.read()
		print(fill_from_text(request, text))

		if input('Another?\n') in ['no','n','NO', 'N']:
			break




if __name__ == '__main__':


	while True:
		print()
		options = os.listdir('texts')
		random.shuffle(options)
		fname = command_line.choose_from_list(options[:10])
		print(fname)
		fpath = 'texts/' + fname
		request = fname.split('.txt')[0].lower()
		print(request)
		text = librarian.text_from_path(fpath)

		candidates_and_scores = fill_from_context_free_grammar(request, text)
		for c, s in candidates_and_scores:
			print(" ".join(c), s)




	

	





