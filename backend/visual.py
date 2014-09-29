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
import csv
import nn_apply
import sklearn
from sklearn.manifold import TSNE
import sys
sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python")
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
from scipy import *

# Create a csv file with each row as concepts of a case idenfied by case ID
def import_concepts():
	conceptcsv = open('concept.csv', 'wb')
	concept_list = csv.writer(conceptcsv)
	text_database = import_cases.import_data('holdings_cases/')
	keys = text_database.keys()
	for i in range(len(keys)):
		concept_list.writerow([text_database[keys[i]]['concept'], keys[i]])
	conceptcsv.close()

# Load the concepts of cases from the csv and tabulate the counts of each concept
def analyze_concepts():
	concept_database = {}
	conceptcsv = open('concept.csv', 'rU')
	concept_data = csv.reader(conceptcsv)
	for row in concept_data:
		concept_list = row[0].split('XXXXXX')
		if (len(concept_list) > 0):
			length = len(concept_list) / 2
			for i in range(length):
				this_concept = concept_list[2*i + 1]
				if (this_concept in concept_database.keys()):
					concept_database[this_concept] = concept_database[this_concept] + 1
				else:
					concept_database[this_concept] = 1
	
	concept_fulllist = []
	concept_vectors = []
	for keys in concept_database.keys():
		concept_fulllist.append((keys, concept_database[keys]))
		# Get the 25-dimensions vector for each concept
		concept_vectors.append(nn_apply.get_sen_vec(keys.split(' ')))

	vectors = numpy.array(concept_vectors)
	# Use the TSNE library to transform the 25 dimensioned vector to only 2D for plotting
	model = TSNE(n_components=2, random_state=0)
	new_vectors = model.fit_transform(vectors)
	
	data_for_plot = []
	# Modify the label of several concepts so they are shorter
	for j in range(len(concept_fulllist)):
		name = concept_fulllist[j][0]
		name = name.replace("United States", "U.S.");
		name = name.replace("Constitution", "Cons.");
		name = name.replace("Amendment", "Amd.");
		name = name.replace("Federal", "Fed.");
		name = name.replace("government", "Gov.");
		name = name.replace("Supreme Court", "S. Ct.");
		name = name.replace("Court", "Ct.");
		name = name.replace("in the", "in");
		name = name.replace("of the", "of");
		name = name.replace("to the", "/");
		data_for_plot.append((name,concept_fulllist[j][1],new_vectors[j]))
	data_for_plot.sort(key=lambda tup: tup[1], reverse= True)

	return data_for_plot

# Plot the bubble graph based on the data
def plot_bubble_graph(data_for_plot):

	x = []
	y = []
	z = []
	color = []
	for i in range(len(data_for_plot)):
		if (data_for_plot[i][1] >= 15):
			x.append(data_for_plot[i][2][0])
			y.append(data_for_plot[i][2][1])
			z.append(data_for_plot[i][1]*30)
			randomnum = 1.2 * numpy.random.uniform(low=-1.0, high=1.0, size=1)
			text(data_for_plot[i][2][0], data_for_plot[i][2][1] + randomnum[0], data_for_plot[i][0], size=10,horizontalalignment='center',verticalalignment='bottom')
			color.append(numpy.random.rand(3,))

	sct = scatter(x, y, c=color, s=z, linewidths=2, edgecolor='w')
	sct.set_alpha(0.75)

	axis([-30,30,-25,25])
	title('Neural Network Prediction of Associated Concepts')
	xlabel('Axis - 1')
	ylabel('Axis - 2')
	grid()
	show()

def main():
	# import_concepts()
	data_for_plot = analyze_concepts()
	plot_bubble_graph(data_for_plot)

if __name__ == '__main__':
	main()
