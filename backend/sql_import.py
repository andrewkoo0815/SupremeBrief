#!/usr/bin/python
# Andrew main.py Version 1.0
# Created Aug 21, 2014
# Updated Aug 21, 2014

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python")

import pymysql as mdb
import os
import csv
import import_cases

cases_info = import_cases.import_data('holdings_cases/')
print "data_import_complete"
file_dir_1 = 'holdings_opinion_learn_lsa/'
file_dir_2 = 'holdings_opinion_learn_nn/'

importlistcsv = open('lookup.csv', 'rU')
import_list = csv.reader(importlistcsv)
import_dic = {}
for row in import_list:
	if (len(row) == 2):
		import_dic[row[1]] = row[0][:-4] + '.txt'
	elif (len(row) == 3):
		import_dic[row[1]] = row[0][:-4] + '.txt'
		import_dic[row[2]] = row[0][:-4] + '.txt'

con = mdb.connect('localhost', 'root', '', 'casetext') #host, user, password, #database


with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Cases")
	cur.execute("CREATE TABLE Cases(Citation VARCHAR(25), Title text, The_Date VARCHAR(25), Summary1 text, Summary2 text, Concept text)")
	for key in import_dic.keys():
		case_id = import_dic[key][:-4]
		if (os.path.isfile(file_dir_1 + import_dic[key]) and os.path.isfile(file_dir_2 + import_dic[key])):
			document1 = open(file_dir_1 + import_dic[key], "r")
			document2 = open(file_dir_2 + import_dic[key], "r")
			document_summary1 = document1.read()
			document_summary2 = document2.read()
			sentences1 = document_summary1.split('XXXXXX')
			sentences2 = document_summary2.split('XXXXXX')
			if (len(sentences1) >= 5 and len(sentences2) >= 5 and cases_info[case_id]['concept'] != "None"):
				cur.execute("INSERT INTO Cases (Citation, Title, The_Date, Summary1, Summary2, Concept) VALUES(%s, %s, %s, %s, %s, %s)", (key, cases_info[case_id]['title'], cases_info[case_id]['date'], document_summary1, document_summary2, cases_info[case_id]['concept']))

# with con: 
#     cur = con.cursor()
#     cur.execute("SELECT * FROM Cases")
#     rows = cur.fetchall()
#     for row in rows:
#         print row