import pronouncing
import random
import re
from model import librarian


def stresses_for_text(text):
	line_stresses = []
	for word in text.lower().split():
		word_stresses = pronouncing.stresses_for_word(word)
		if len(word_stresses) == 0:
			return ''
		else:
			line_stresses.extend(pronouncing.stresses_for_word(word)[0])
	return ''.join(line_stresses)


def lines_and_stresses_for_path(fpath):
	with open(fpath) as f:
		lines = f.readlines()

	lines = [line.strip() for line in lines]
	lines = [line for line in lines if len(line) > 0]

	lines_and_tags = [line.split('\t') for line in lines]

	#return [(line, get_property(tag, 'stress')) for line, tag in lines_and_tags]
	return [(line, re.compile('^' + get_property(tag, 'stress') + '$')) for line, tag in lines_and_tags]


def get_property(tag_string, prop_to_get):
	
	if not tag_string[0] == '<' and tag_string[-1] == '>':
		raise InputError(tag_string, "must start with '<' and end with '>'")
	else:
		contents = tag_string[1:-1]
		for element in contents:
			parts = contents.split("=")
			if len(parts) == 2:
				prop = parts[0]
				value = parts[1].replace('"','').replace("'", '')
				if prop == prop_to_get:
					return value
		print(tag_string)
		print(prop_to_get)
		raise InputError(prop_to_get, "not in tag string")
	

def play_song(lines_and_stresses, matches_by_stress, title=None, artist=None, voice=None):

	indent_distance = 70

	print()
	if title:
		print(title.upper())
	if artist:	
		print('by', artist.upper())
	if voice:	
		print('in the voice of', voice.upper())
	print()

	used_lines = set([])

	for line, stress in lines_and_stresses:

		original_line = '("%s")' % line

		if not input('') == 'n':

			options = list(matches_by_stress[stress])
			unused_options = list(matches_by_stress[stress] - set(used_lines))

			if len(unused_options) > 0:
				choice = random.choice(unused_options)				
				used_lines.add(choice)
			elif len(options) > 0:
				choice = random.choice(options)
			else:
				choice = line

			to_print = choice.upper()
			to_print += " " * (indent_distance - len(to_print))
			to_print += original_line
			print(to_print)






if __name__ == '__main__':
	
	lines_and_stresses = lines_and_stresses_for_path('songs/yesterday.txt')
	#lines_and_stresses = lines_and_stresses_for_path('songs/eye-of-the-tiger-2.txt')

	stresses = set([stress for line, stress in lines_and_stresses])

	matches_by_stress = {stress: set([]) for stress in stresses}

	category = 'Yelp'
	#category = 'harrypotter'
	dirpath = '/Users/jbrew/desktop/boom-lyrics/resources/%s' % category
	#dirpath = '/Users/jbrew/desktop/library/prose/%s' % category

	candidate_lines = librarian.lines_from_directory(dirpath)
	candidate_sentences = librarian.sentences_from_directory(dirpath)
	candidate_lines = list(set(candidate_lines).union(set(candidate_sentences)))
	candidate_lines = librarian.in_size_range(candidate_lines, 1, 65)
	candidate_lines = librarian.filter_characters(candidate_lines, '()[]')
	candidate_lines = librarian.clean_all(candidate_lines)

	print(len(candidate_lines), 'candidate lines')

	for i, candidate_line in enumerate(candidate_lines):
		
		line_stresses = stresses_for_text(candidate_line)

		for stress_regex, match_set in matches_by_stress.items():
			if stress_regex.match(line_stresses):
				match_set.add(candidate_line)
	
	play_song(lines_and_stresses, matches_by_stress, title="Yesterday", artist='The Beatles', voice=category)

	"""
	for stress_regex, match_set in matches_by_stress.items():
		print(stress_regex)
		print(len(match_set))
		print(match_set)
	"""


def regex_from_stresses(stresses):
	"""
	given a list of possible stresses for each word, return a regex representing them
	"""
	pass