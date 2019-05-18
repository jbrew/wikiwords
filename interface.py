import os
import wikiwords

def choose_from_list(options):
	col_width = 70
	enumerated_options = list(enumerate(options))
	line = ''
	for num, topic in enumerated_options:
		#print(str(num+1), topic)
		line += '(%s) %s  ' % (str(num+1), topic)
		dist_to_next_col = len(line) % 5
		line += ' ' * 5
		if len(line) > col_width:
			print(line)
			line = ''
	print(line)
	choice = int(input('Enter a number from above\n'))
	if choice > 0 and choice <= len(enumerated_options):
		return enumerated_options[choice-1][1]
	else:
		print('Choose a number in that range!')
		return choose_from_list(options)


if __name__ == '__main__':
	requested = input('Enter search term:\n')
	results = wikiwords.search(requested)

	page = choose_from_list(results)
	print(page)
	quotes = wikiwords.quotes_from_page(page)

	print(quotes)