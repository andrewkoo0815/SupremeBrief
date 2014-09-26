#!/usr/bin/python
# Andrew views.py Version 1.0
# Created Sep 5, 2014
# Updated Sep 5, 2014

from flask import render_template, request
from app import app
import pymysql as mdb
import grab_news
import json

db = mdb.connect(user="root", host="localhost", db="casetext", charset='utf8')

def get_citation_list():

	with db: 
		cur = db.cursor()
		cur.execute("SELECT Citation FROM Cases")
		query_results = cur.fetchall()

	citation_list = []
	for query in query_results:
		citation_list.append(query[0].encode('utf-8'))
	return citation_list

@app.route('/')
@app.route('/index')
def index():
	
	citation_list = get_citation_list()
	return render_template("index.html",
        title = 'Home', citations = citation_list,
        )

@app.route('/chart')
def chart():
	global concept
	concept_list = concept.split('XXXXXX')
	data = []
	for i in range(len(concept_list)/2):
		datapt = {}
		name = concept_list[2*i + 1]
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
		datapt['name'] = name 
		datapt['value'] = concept_list[2*i][:5]
		data.append(datapt)

	return render_template("chart.html",
        title = 'concept', data = data,
        )

@app.route('/slides')
def slides():
	citation_list = get_citation_list()
	return render_template("slides.html",
        title = 'slides', citations = citation_list,
        )

@app.route('/author')
def author():
	citation_list = get_citation_list()
	return render_template("author.html",
        title = 'author', citations = citation_list,
        )

@app.route('/summary', methods = ['GET','POST'])
def summary():
	input_citation = request.form.get("citation", "None")
	citation_list = get_citation_list()

	with db: 
		cur = db.cursor()
		cur.execute("SELECT Summary1, Summary2, Title, The_Date, Concept FROM Cases WHERE Citation = %s;", input_citation)
		query_results = cur.fetchall()
	if (len(query_results) > 0):
		sentences1 = query_results[0][0].replace("\n", "").split('XXXXXX')
		sentences2 = query_results[0][1].replace("\n", "").split('XXXXXX')
		global concept
		concept = query_results[0][4]
		news = grab_news.grab_news(query_results[0][2])
		number1 = sentences1[5]
		number2 = sentences2[5]
		return render_template("summary.html", title = query_results[0][2], number1 = number1, number2 = number2, citations = citation_list, date = query_results[0][3], phrase = query_results[0][4], citation = input_citation, news = news, sen1 = sentences1[0], sen2 = sentences1[1], sen3 = sentences1[2], sen4 = sentences1[3], sen5 = sentences1[4], sen6 = sentences2[0], sen7 = sentences2[1], sen8 = sentences2[2], sen9 = sentences2[3], sen10 = sentences2[4])
	else:
		return render_template("summary.html", title = input_citation, citations = citation_list, sen1 = "Citation number does not exist", sen6 = "Citation number does not exist")