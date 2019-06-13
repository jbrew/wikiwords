import wikiwords
import random
import command_line
import os
from model import markov
from model import dictionary
from model import librarian

uppercase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
lowercase = set('abcdefghijklmnopqrstuzwxyz')


"""
This is command line program for filling in Backronyms.

"""

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
				word_sequence = words[start:end]
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
	#text_loop('magic')
	keywords_loop('MaGiC')


	

	





