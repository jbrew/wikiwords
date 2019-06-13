


def choose_from_list(options, display='vertical'):
	enumerated_options = list(enumerate(options))
	line = ''
	for num, topic in enumerated_options:
		if display == 'vertical':
			line += str(num+1) + '. ' + topic + '\n'
		elif display == 'horizontal':
			line += '(%s) %s  ' % (str(num+1), topic)
			dist_to_next_col = len(line) % 5
			line += ' ' * 5
		else:
			line = ''
	print(line)
	choice = input('Enter a number from above\n')
	try:
		num = int(choice)
		if num > 0 and num <= len(enumerated_options):
			return enumerated_options[num-1][1]
		else:
			print('Enter a number in that range!')
			return choose_from_list(options)
	except:
		return choice
