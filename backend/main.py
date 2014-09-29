#!/usr/bin/python
# Andrew main.py Version 1.0
# Created Sep 6, 2014
# Updated Sep 6, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import sk_learn
import sumy_learn
import import_cases
import import_holdings
import nn_apply

# Excute the summary algorithms
def execute_learning():
	input_dir = 'holdings_opinion/'
	output_dir = 'holdings_opinion_learn_text2/'
	input_name_list = os.listdir(input_dir)


	# Algorithm options: "lsa", "edmundson", "lex", "luhn", "random", "text"
	algorithm_list = ["lsa", "edmundson", "lex", "luhn", "random", "text"]
	algorithm = algorithm_list[0]
	# Edmundson requires bonus words
	# The random summarizer doesn't work that well

	# Get all the filenames from the input directory
	for i in range(len(input_name_list)):
		filename = input_name_list[i]
		print i
		document = open(input_dir + filename, "r")
		document_text = document.read()
		# Skip files that are too small (the summary algorithms won't converge) or the hidden files (samll filename length)
		if (len(document_text) > 5000 and len(filename) > 10):
			try:
				# sumy_learn.create_summary(algorithm, input_dir + filename, output_dir + filename[:-4] + ".txt")
				# nn_apply.create_summary(document_text, output_dir + filename[:-4] + ".txt")
				sk_learn.textrank(document_text, output_dir + filename[:-4] + ".txt")
			except:
				# skip creating summary for this file if error message occurs
				continue

def main():
	execute_learning()

if __name__ == '__main__':
	main()
