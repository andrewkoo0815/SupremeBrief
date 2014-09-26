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
import numpy


def main():
	text_database = import_cases.import_data('all_cases/')
	stopwords = nltk.corpus.stopwords.words('english')
	filelist = text_database.keys()
	fulllist = []
	for i in range(len(filelist)):
		file_id = filelist[i]
		if (len(file_id) > 10):
			text = text_database[file_id]['opinion_text']
			wordlist = text.split('.')
			for i in range(len(wordlist)):
				prefiltered = wordlist[i].split(' ')
				filtered_words = [w for w in prefiltered if w.lower() not in stopwords]
				fulllist.append(filtered_words)
	
	print "Model Training Begin"
	model = gensim.models.Word2Vec(fulllist, size=25, window=5, min_count=5, workers=4)
	
	# model = gensim.models.Word2Vec.load('NN_model')
	# print model.similarity('federal', 'court')
	# print model['federal']
	# print model['court']
	model.save('NN_model2')

if __name__ == '__main__':
	main()
