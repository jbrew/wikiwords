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
