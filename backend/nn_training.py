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

# Train the neural network for word2vec using all 120K court cases
def main():
	text_database = import_cases.import_data('all_cases/')
	stopwords = nltk.corpus.stopwords.words('english')
	filelist = text_database.keys()
	# fulllist will be used to store all the sentences from the list
	fulllist = []
	for i in range(len(filelist)):
		file_id = filelist[i]
		if (len(file_id) > 10):
			text = text_database[file_id]['opinion_text']
			# Separate the text into sentences
			wordlist = text.split('.')
			for i in range(len(wordlist)):
				# Separate the words
				prefiltered = wordlist[i].split(' ')
				# Remove stop words
				filtered_words = [w for w in prefiltered if w.lower() not in stopwords]
				fulllist.append(filtered_words)
	
	print "Model Training Begin"
	# Train the neural network model (size=25, 4 processors) with 
	model = gensim.models.Word2Vec(fulllist, size=25, window=5, min_count=5, workers=4)
	
	# model = gensim.models.Word2Vec.load('NN_model')
	# print model.similarity('federal', 'court')
	# print model['federal']
	# print model['court']
	model.save('NN_model2')

if __name__ == '__main__':
	main()
