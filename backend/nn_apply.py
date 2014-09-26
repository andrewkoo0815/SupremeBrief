#!/usr/bin/python
# Andrew main.py Version 1.0
# Created Sep 6, 2014
# Updated Sep 6, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import nltk
from nltk.corpus import stopwords
import import_cases
import gensim
import logging
import numpy as np
import sk_learn
import scipy
from scipy import spatial
import networkx as nx
import regex

model = gensim.models.Word2Vec.load('NN_model2')
keys = model.vocab.keys()
size = 25

def get_sen_vec(sentence):
	count = 0
	vector = [0] * size
	for j in range(len(sentence)):
		if sentence[j] in keys:
			vector = np.add(vector, model[sentence[j]])
			count = count + 1
	vector = np.divide(vector, count)
	return vector

def get_sim(vector1, vector2):
	return spatial.distance.cosine(vector1, vector2)

def get_top_sentences(pr, N):
	keys = pr.keys()
	sentence_list = []
	for i in range(len(keys)):
		sentence_list.append((pr[keys[i]],keys[i]))
	sentence_list.sort(key=lambda tup: tup[0], reverse=True)
	j = 0
	top_sentences = []
	document_length = len(sentence_list)
	while (j < N and j < document_length):
		top_sentences.append(sentence_list[j][1])
		j = j + 1
	return top_sentences

def create_summary(text, output_file = "nn_summary.txt"):
	stopwords = nltk.corpus.stopwords.words('english')
	fulllist = []

	retain_list = []

	wordlist = text.split('.')
	for i in range(len(wordlist)):
		prefiltered = wordlist[i].split(' ')
		halffiltered = []
		for j in range(len(prefiltered)):
			halffiltered.append(regex.sub(r'[^a-zA-Z]','',prefiltered[j]))
		filtered_words = [w for w in halffiltered if w.lower() not in stopwords and len(w) > 4]
		if (len(filtered_words) > 15):
			fulllist.append(filtered_words)
			retain_list.append(i)
	
	paragraph_size = len(fulllist)
	vector_list = []
	for i in range(paragraph_size):
		vector_list.append(get_sen_vec(fulllist[i]))

	matrix = np.zeros(shape=(paragraph_size, paragraph_size))
	for j in range(paragraph_size):
		for k in range(paragraph_size):
			matrix[j][k] = get_sim(vector_list[j], vector_list[k])

	G = nx.Graph(matrix)
	pr = nx.pagerank(G, alpha = 0.9)
	N = 5
	toplist = get_top_sentences(pr, N)
	
	record = open(output_file, "w")
	ordered_list = toplist[:]
	ordered_list.sort()
	position = ordered_list.index(toplist[0])
	for l in range(len(ordered_list)):
		record.write(wordlist[retain_list[ordered_list[l]]]+ '.XXXXXX')
	record.write(str(position)+ 'XXXXXX')
	record.close()


if __name__ == '__main__':
	main()
