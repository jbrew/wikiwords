import wikiwords
import random
from model import markov
from model import dictionary


def naive_keyword_fill_loop(word):
	kwords = wikiwords.get_keywords(word)
	keywords = [kw for kw in kwords if kw[0] in list(word)]
	kw_dict = {}
	for kw in keywords:
		if kw[0] in kw_dict:
			kw_dict[kw[0]].append(kw)
		else:
			kw_dict[kw[0]] = [kw]

	while True:
		command = input('Again?\n')

		for letter in word:
			print(random.choice(kw_dict[letter]))

def filter_by_letter(words, letter):
	return [word for word in words if word[0] == letter]

def fill_by_request(acronym, request, keywords, fdict):
	
	"""
	acronym: 	a list of words
	request: 	a same-length string of uppercase and lowercase letters and underscores
				indicating which positions to fill with keywords (uppercase), fill with 
				bridge words (lowercase) or leave alone (underscores)
	keywords:	a list of topical keywords
	fdict:		a dictionary mapping contexts to continuations
	"""

	if not len(request) == len(acronym):
		print('request must be same length as acronym')
		return None

	uppercase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	lowercase = set('abcdefghijklmnopqrstuzwxyz')

	scaffold = [None] * len(acronym)

	for i, letter in enumerate(request):
		if letter in uppercase:
			candidates = filter_by_letter(keywords, letter.lower())
			if len(candidates) > 0:
				scaffold[i] = random.choice(candidates)

	for i, entry in enumerate(scaffold):
		if entry == None:
			candidates = [k for k in fdict.keys() if len(k) > 0 and len(k.split()) == 1 and k[0] == request[i]]
			bridges = markov.scored_bridges(scaffold[i-1], candidates, scaffold[i+1], fdict)
			top_bridges = dictionary.sort_ascending(bridges)[:10]
			scaffold[i] = random.choice(top_bridges)[0]

	return scaffold


def backronym_loop(request):
	text = wikiwords.text_from_search_term(request.lower())
	keywords = wikiwords.get_keywords(request.lower())[:150]
	print('first ten keywords:',keywords[:10])
	fdict = markov.forward_dict(text)
	bdict = markov.backward_dict(text)
	while True:
		if not input('Find another backronym?\n') in ['no','n','NO','NO!']:
			backronym = fill_by_request(list(request), request, keywords, fdict)
			capitalized = [word[0].upper() + word[1:] for word in backronym]
			print(" ".join(capitalized))



### TESTS ###

def paris_test():
	paris_text = wikiwords.text_from_search_term('paris')
	keywords = wikiwords.get_keywords('paris')[:150]
	print('first ten keywords:',keywords[:10])

	fdict = markov.forward_dict(paris_text)
	bdict = markov.backward_dict(paris_text)
	

	while True:
		if not input('Find another backronym?\n') in ['no','n','NO','NO!']:
			print(fill_by_request(list('paris'), 'PaRiS', keywords, fdict))

if __name__ == '__main__':
	#paris_test()

	#backronym_loop('PaRiS')
	backronym_loop('LoNDoN')

	





