#!/usr/bin/python
# Andrew import_holdings.py Version 1.0
# Created Aug 8, 2014
# Updated Aug 8, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import csv
import string
import nn_apply
import nltk
from nltk.corpus import stopwords
import regex
import numpy
import math

# Create a dictionary of holdings imported from holdings.csv provided by Casetext
def import_holdings():
	holdingscsv = open('holdings.csv', 'rU')
	holdings= csv.reader(holdingscsv)
	holdings_dic = {}
	for row in holdings:
		case_number = row[0].split('\t')[0]
		case_holding = ''.join(row)[len(case_number):]
		case_holding = filter(lambda x: x in string.printable, case_holding)
		holdings_dic[case_number] = case_holding
	return holdings_dic

# Import summary (top picked sentences) from the text file previously created
def import_summary(filename):
	file_dir = 'holdings_opinion_learn_lex/'
	if (os.path.isfile(file_dir + filename)):
		document = open(file_dir + filename, "r")
		document_summary = document.read()
		sentences = document_summary.replace('XXXXXX', ' ')
		return sentences
	else:
		return "None"

# Create the lookup_dic imported from the lookup table (file ID and citation number)
def import_lookup():
	lookuplistcsv = open('lookup.csv', 'rU')
	lookup_list = csv.reader(lookuplistcsv)
	lookup_dic = {}
	for row in lookup_list:
		if (len(row) == 2):
			lookup_dic[row[1]] = row[0][:-4] + '.txt'
		elif (len(row) == 3):
			lookup_dic[row[1]] = row[0][:-4] + '.txt'
			lookup_dic[row[2]] = row[0][:-4] + '.txt'
	return lookup_dic

# Get the corresponding vector of the sentences after removing numbers and the stop words.
def get_vectors(wordlist):
	stopwords = nltk.corpus.stopwords.words('english')
	prefiltered = wordlist.split(' ')
	halffiltered = []
	for j in range(len(prefiltered)):
		halffiltered.append(regex.sub(r'[^a-zA-Z]','',prefiltered[j]))
		filtered_words = [w for w in halffiltered if w.lower() not in stopwords and len(w) > 4]

	vector = nn_apply.get_sen_vec(filtered_words)
	return vector

# Find cosine similarity between holding and algorithm picked summary based on their vectors
def find_similarity(holding, summary):
	vector1 = get_vectors(holding)
	vector2 = get_vectors(summary)
	score = nn_apply.get_sim(vector1, vector2)
	return score

# Compute the N, mean, variance, of cosine similarities between holdings (expert written) and algorithm-picked sentences
def main():
	lookup_dic = import_lookup()
	lookup_list = lookup_dic.keys()
	holdings_dic = import_holdings()
	keys = holdings_dic.keys()
	score_list = []
	case_count = len(keys)

	for i in range(case_count):
		key = keys[i]
		print i
		holding = holdings_dic[key].replace('\t', '')
		if (key in lookup_list):
			summary = import_summary(lookup_dic[key])
			if (summary != "None"):
				score = find_similarity(holding, summary)
				if (math.isnan(score)):
					score = -1
				score_list.append(score)
	print len(score_list)
	print sum(score_list)/len(score_list)
	print numpy.std(score_list)

if __name__ == '__main__':
	main()