import math
import re
from collections import Counter
from . import dictionary
from . import texthandler


def forward_dict(text, max_ngram_size=3):
	count_dicts = [ngram_count_dict(text, ngram_size) for ngram_size in range(1,max_ngram_size+1)]
	fdict = {}
	for count_dict in count_dicts:
		for ngram, count in count_dict.items():
			head, tail = " ".join(ngram.split()[:-1]), ngram.split()[-1]
			enter_ngram(head, tail, count, fdict)
	return fdict

def backward_dict(text, max_ngram_size=3):
	count_dicts = [ngram_count_dict(text, ngram_size) for ngram_size in range(1,max_ngram_size+1)]
	bdict = {}
	for count_dict in count_dicts:
		for ngram, count in count_dict.items():
			head, tail = ngram.split()[0], " ".join(ngram.split()[1:])
			enter_ngram(tail, head, count, bdict)
	return bdict

def ngram_count_dict(text, ngram_size):
	search_string = regex_string(ngram_size)
	target = "(?=(%s))(?<!\w)" % search_string
	return Counter(re.findall(target, text.lower().replace(".","").replace("\n"," ").replace("'","")))

def regex_string(ngram_size):
	word = "'?\w[\w']*(?:-\w+)*'?"
	space = "\s"
	return word + (space+word)*(ngram_size-1)

# helper function for dictionary building
def enter_ngram(head, tail, count, d):
	if head in d:
		d[head][tail] = count
	else:
		d[head] = {tail: count}

# transition cost of candidate going forward
def forward_cost(before, candidate, after, fdict):
	last_before = before.split()[-1] if len(before) > 0 else ''
	first_after = after.split()[0] if len(after) > 0 else ''
	return transition_cost(" ".join([last_before, candidate, first_after]), fdict)

def transition_cost(seq, fdict, max_cost=20):
	cost = 0
	tokens = seq.split()
	for i in range(len(tokens)-1):
		head, tail = tokens[i], tokens[i+1]
		if head in fdict and tail in fdict[head]:
			cost += -1 * math.log(fdict[head][tail],2)
		else:
			cost += max_cost
	return cost

def scored_bridges(before, bridge_candidates, after, fdict):
	scored_candidates = {candidate: forward_cost(before, candidate, after, fdict) for candidate in bridge_candidates}
	return scored_candidates

def likelihood(seq, fdict):
	likelihood = 1
	tokens = seq.split()
	for i in range(len(tokens)-1):
		head, tail = tokens[i], tokens[i+1]
		if head in fdict and tail in fdict[head]:
			likelihood *= fdict[head][tail]
		else:
			return 0
	return likelihood





