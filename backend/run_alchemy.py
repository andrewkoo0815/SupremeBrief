#!/usr/bin/python
# Andrew main.py Version 1.0
# Created Sep 15, 2014
# Updated Sep 15, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
# import sys; sys.path.append("/Users/andrewkoo/Workspace/Casetext/alchemyapi/")
import import_cases
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

def get_concepts(text):

	response = alchemyapi.concepts("text", text)

	if "concepts" in response.keys():
		concepts = response["concepts"]

		concept_list = []
		count = 0
		for i in range(len(concepts)):
			if (count < 5 and concepts[i]['text'] != "United States"):
				concept_list.append(concepts[i]['relevance'].encode('utf-8'))
				concept_list.append(concepts[i]['text'].encode('utf-8'))
				count = count + 1
		concept_list = 'XXXXXX'.join(concept_list)
		return concept_list
	else:
		print "No Concepts Returned"
		return "None"


def main():
	
	text_database = import_cases.import_data('test_cases/')
	filelist = text_database.keys()
	
	for i in range(len(filelist)):
		if (i < 1):
			file_id = filelist[i]
			text = text_database[file_id]['opinion_text']
			concept_list = get_concepts(text)
	print concept_list


if __name__ == '__main__':
	main()
