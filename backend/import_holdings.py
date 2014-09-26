#!/usr/bin/python
# Andrew import_holdings.py Version 1.0
# Created Aug 8, 2014
# Updated Aug 8, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import csv
import string
import import_holdings


def import_holdings():
	holdingscsv = open('holdings.csv', 'rU')
	holdings= csv.reader(holdingscsv)
	holdings_dic = {}
	for row in holdings:
		case_number = row[0].split('\t')[0]
		case_holding = ''.join(row)[len(case_number):]
		case_holding = filter(lambda x: x in string.printable, case_holding)
		holdings_dic[case_number] = case_holding
	return holdings_dic.keys()

