#!/usr/bin/python
# Andrew import_cases.py Version 1.0
# Created Sep 8, 2014
# Updated Sep 8, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import xml.etree.ElementTree as ET
import csv
import string
import shutil
import import_holdings
import extract_keywords
import run_alchemy
mode = "test" # "test" or "all" or "holdings"

default_dir = '/Users/andrewkoo/Workspace/Casetext/' + mode +'_cases/'

def get_citation(root):
	citation_text = []
	for citation in root.iter('citation'):
		citation_text.append(citation.text)
	if (len(citation_text) > 0):
		return citation_text
	else:
		return "None"

def get_date(root):
	date = root.find('date')
	date_text = date[0].text
	if (len(date_text) > 0):
		if (date_text[-5] == " "):
			return date_text[-4:]
		else:
			return date_text[-5:-1]
	else:
		return "None"

def get_title(root):
	reporter_caption = root.find('reporter_caption')
	reporter_caption_text = ''
	for text in reporter_caption.itertext():
		reporter_caption_text = reporter_caption_text + text
	textlist = reporter_caption_text.split(',')
	return textlist[0]

def get_text(root, type):
	section = root.findall(type)
	section_text = ''
	if (section is not None):
		if (type == 'opinion_text'):
			if (len(section) > 0):
				for text in section[-1].itertext():
					section_text = section_text + text
		else:
			for j in range(len(section)):
				for text in section[j].itertext():
					section_text = section_text + text
		section_text = filter(lambda x: x in string.printable, section_text.encode('utf-8'))
		return section_text
	else:
		return "None"

def import_concept():
	concept_database = {}
	conceptcsv = open('concept.csv', 'rU')
	concept_data = csv.reader(conceptcsv)
	for row in concept_data:
		concept_database[row[1]] = row[0]
	return concept_database


def import_data(cases_dir = default_dir):
    text_database = {}
    concept_database = import_concept()
    concept_keys = concept_database.keys()
    case_name_list = os.listdir(cases_dir)
    case_name_list.sort()

    # holdings_list = import_holdings.import_holdings()

    allcitations = []
    lookupcsv = open('lookup.csv', 'wb')
    lookup_table = csv.writer(lookupcsv)

    for i in range(len(case_name_list)):
    # for i in range(len(case_name_list)):
    	# print file_id
    	print i
    	file_id = case_name_list[i][:-4]
    	file = cases_dir + case_name_list[i]
    	if (file[-3:] == 'xml'):
			tree = ET.parse(file)
			root = tree.getroot()
			text_database[file_id] = {}
			text_database[file_id]['citation'] = get_citation(root)
			text_database[file_id]['date'] = get_date(root)
			text_database[file_id]['title'] = get_title(root)
			text_database[file_id]['syllabus'] = get_text(root, 'syllabus')
			text_database[file_id]['attorneys'] = get_text(root, 'attorneys')
			text_database[file_id]['opinion_byline'] = get_text(root, 'opinion_byline')
			text_database[file_id]['opinion_text'] = get_text(root, 'opinion_text')
			text_database[file_id]['concurrence_byline'] = get_text(root, 'concurrence_byline')
			text_database[file_id]['concurrence_text'] = get_text(root, 'concurrence_text')
			text_database[file_id]['dissent_byline'] = get_text(root, 'dissent_byline')
			text_database[file_id]['dissent_text'] = get_text(root, 'dissent_text')
			if (file_id in concept_keys):
				text_database[file_id]['concept'] = concept_database[file_id]
			else:
				text_database[file_id]['concept'] = "None"


			# text_database[file_id]['key_phrase'] = extract_keywords.extract_keywords(text_database[file_id]['opinion_text'])
			# text_database[file_id]['concept'] = run_alchemy.get_concepts(text_database[file_id]['opinion_text'])

			### Code for generating lookuplist
			citations = get_citation(root)
			if (len(citations) == 1):
				lookup_table.writerow([case_name_list[i], citations[0]])
			elif (len(citations) == 2):
				lookup_table.writerow([case_name_list[i], citations[0], citations[1]])

			### Codes to copy files that have sumary into another directory
			# citations = get_citation(root)
			# for j in range(len(citations)):
			# 	if (citations[j] in holdings_list):
			# 		shutil.copyfile(mode + '_cases/' + file_id + '.xml', 'holdings_cases/' + file_id + '.xml')
    lookupcsv.close()
    return text_database
