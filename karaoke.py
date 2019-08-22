import wikiwords
import pronouncing
import random
#import cfg
#import nltk
from model import librarian



def stresses_for_line(line):
	"""
	returns the stress pattern of the given line
	"""

	parts = line.split('\t')

	if len(parts) == 2:
		text, info = parts
		stresses_string = get_property(info, 'stress')
		stresses = ''.join(stresses_string.split())
		return list(stresses)
	elif len(parts) == 1:
		return stresses_for_text(parts[0])

def stresses_for_text(text):
	line_stresses = []
	for word in text.lower().split():
		word_stresses = pronouncing.stresses_for_word(word)
		if len(word_stresses) == 0:
			return ''
		else:
			line_stresses.extend(pronouncing.stresses_for_word(word)[0])
	return ''.join(line_stresses)

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

	
# TODO: replace with regular expressions
def is_singable_to_stress_pattern(word_sequence, stress_pattern):

	if len(word_sequence) == 0 and len(stress_pattern) == 0:
		return True
	elif len(word_sequence) == 0 and len(stress_pattern) > 0:
		return False
	elif len(word_sequence) > 0 and len(stress_pattern) == 0:
		return False
	else:
		first_word = word_sequence[0]

		options = stress_options_for_word(first_word)

		for option in options:
			if len(option) <= len(stress_pattern) and option == stress_pattern[:len(option)]:
				return is_singable_to_stress_pattern(word_sequence[1:], stress_pattern[len(option):])

		return False


def stress_options_for_word(word):

	options = pronouncing.stresses_for_word(word)

	all_options = set(options)

	for option in options:
		if len(option) == 1:
			all_options.add(option)
			#all_options.add('1')
			#all_options.add('0')
		else:
			all_options.add(option)
			all_options.add(option.replace('2','0'))		# secondary treated as unstressed
			all_options.add(option.replace('2','1'))		# secondary treated as stressed

	return list(all_options)



def singability_tests():
	assert(is_singable_to_stress_pattern('vestigial hip of the heart'.split(), '01001001') == True)	
	assert(is_singable_to_stress_pattern('vestigial hip of heartbeats'.split(), '01001001') == False)
	
if __name__ == '__main__':

	fill_lines = librarian.lines_from_directory('/Users/jbrew/desktop/boom-lyrics/resources/TED')
	fill_lines = librarian.in_size_range(fill_lines, 10, 100)
	fill_lines = librarian.filter_characters(fill_lines, '()[]')
	fill_lines = librarian.clean_all(fill_lines)

	print(len(fill_lines), 'lines found')

	cue_lines = librarian.lines_from_file('songs/total-eclipse-of-the-heart.txt')

	lines_and_tags = [cue_line.strip().split('\t') for cue_line in cue_lines]
	lines_and_stresses = [(line, get_property(tag, 'stress').replace(' ','')) for line, tag in lines_and_tags]


	replacement_dict = {stress_pattern: [] for line, stress_pattern in lines_and_stresses}

	stress_dict = {}

	for i, line in enumerate(fill_lines):
		print(i)

		stress_pattern = stresses_for_text(line)

		if stress_pattern in stress_dict:
			stress_dict[stress_pattern].add(line)
		else:
			stress_dict[stress_pattern] = set([line])

	print(len(stress_dict), 'entries in stress dict')

	while True:
		if input('>\n') is not 'n':

			for scaffold_line, stress_pattern in lines_and_stresses:

				if stress_pattern in stress_dict:
					print(random.choice(list(stress_dict[stress_pattern])))
				else:
					print(scaffold_line)




	


def total_eclipse_test():
	with open('songs/total-eclipse-of-the-heart.txt') as f:
		lines = [line.strip() for line in f.readlines()]

	last_eight = lines[-8:]

	for line in last_eight:
		print(line)
		print(stresses_for_line(line))




