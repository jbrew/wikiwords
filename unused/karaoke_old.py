import pronouncing
import random

def stress_map(words):
	"""
	returns dictionary mapping words to stress patterns
	"""
	# note: currently taking stress only for PRIMARY pronunciation
	return {word: pronouncing.stresses_for_word(word) for word in words}


def swap(original_word, tag, candidate_words, pos_dict=None):
	"""
	if there are any candidates in the list with the same stress
	pattern as the given word, return one of them. otherwise,
	return the original word
	"""

	stresses = pronouncing.stresses_for_word(original_word)

	if len(stresses) > 0:
		slot = stresses[0]
		#print(slot)

		candidates = stress_map(candidate_words)
		candidates = [k for k, v in candidates.items() if len(v) > 0 and v[0] == ''.join(slot)]
		#print(tag)
		#print(pos_dict[tag])
		if pos_dict:
			candidates = [c for c in candidates if c.lower() in pos_dict[tag]]

	if len(candidates) > 0:
		return random.choice(candidates)
	else:
		return original_word



### TESTS



def japan_test():
	keywords = wikiwords.get_keywords_from_file_and_directory('texts/Japan.txt', 'texts')

	text = librarian.text_from_path('texts/Japan.txt')
	pos_tagged = cfg.pos_tagged_from_text(text)
	pos_dict = cfg.word_frequency_by_pos(pos_tagged)
	pos_dict = {k: {vk.lower(): vv for vk, vv in v.items()} for k, v in pos_dict.items()}
	#print(list(pos_dict.items())[:2])

	#print(keywords[:100])

	lines = librarian.lines_from_file('songs/eye-of-the-tiger.txt')
	print(stresses_for_line(lines[10]))

	# "survivor"
	slot = pronouncing.stresses_for_word('survivor')[0]

	#print([pronouncing.stresses_for_word(kw) for kw in keywords[:20]])

	candidates = stress_map(keywords[:100])
	candidates = [k for k, v in candidates.items() if len(v) > 0 and v[0] == ''.join(slot)]


	tagged_line = cfg.pos_tagged_from_text(lines[10].lower())
	print(tagged_line)