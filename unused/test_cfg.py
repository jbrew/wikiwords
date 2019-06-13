from src import cfg
from src import wikiwords


def pos_dict_test():
	text = librarian.text_from_path('texts/Alan Turing.txt')
	tokens = nltk.word_tokenize(text)
	pos_tagged = nltk.pos_tag(tokens)

	pos_dict = word_freq_by_POS(pos_tagged)

	nouns = pos_dict['NN']
	print(dictionary.top_n(nouns, 10))

	## VERBS ##

	vb = pos_dict['VB']		# verb, base form
	print(dictionary.top_n(vb, 10))

	vbz = pos_dict['VBZ']		# third person singular present
	print(dictionary.top_n(vbz, 10))

	vbp = pos_dict['VBP']		# non-third person singular present
	print(dictionary.top_n(vbp, 10))

	vbg = pos_dict['VBG']		# gerund or present participle
	print(dictionary.top_n(vbg, 10))

	vbd = pos_dict['VBD']		# past tense
	print(dictionary.top_n(vbd, 10))

	## ADJECTIVES ##

	adjectives = pos_dict['JJ']
	print(dictionary.top_n(adjectives, 10))





def keywords_test():
	grammar = CFG.fromstring(demo_grammar)
	print(grammar)
	text = librarian.text_from_path('texts/Acronym.txt')
	tokens = nltk.word_tokenize(text)
	pos_tagged = nltk.pos_tag(tokens)
	print(pos_tagged[100:150])
	w2pos = word_to_pos_dict(pos_tagged)
	scored_keywords = wikiwords.keywords_with_scores('Acronym')
	print(top_keywords_for_POS('JJ', w2pos, scored_keywords)[:10])
	print(top_keywords_for_POS('NN', w2pos, scored_keywords)[:10])
	print(top_keywords_for_POS('VBZ', w2pos, scored_keywords)[:10])