import nltk
from model import librarian


if __name__ == '__main__':

	wikitext = librarian.text_from_directory('texts')
	text = nltk.Text(word.lower() for word in wikitext.split())
	text.similar('wanted')
	print()
	text.similar('swing')
