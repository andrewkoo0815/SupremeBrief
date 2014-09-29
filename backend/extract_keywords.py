#!/usr/bin/python
# Andrew main.py Version 1.0
# Created Sep 6, 2014
# Updated Sep 6, 2014

import os; os.chdir('/Users/andrewkoo/Workspace/Casetext/')
import rake
import import_cases

# Extract keywords of the case using the RAKE algorithm
def extract_keywords(text):
	keywords = rake.rake(text)
	if (len(keywords) > 0):
		return keywords[0][0]
	else:
		return ""

