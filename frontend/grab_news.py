#!/usr/bin/python
# Andrew grab_news.py Version 1.0
# Created Sep 11, 2014
# Updated Sep 11, 2014

import json
import urllib2

def perse_news(news):
	headlinelist = []
	newslist = []
	count = 0
	index = 0
	listlength = len(news)
	while (count < 5 and index < listlength ):
		if (news[index]['headline'] not in headlinelist):
			headlinelist.append(news[index]['headline'])
			newslist.append(news[index])
			count = count + 1
		index = index + 1
	return newslist



def grab_news(title):
	news = []
	url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=supreme ' + title + '&fq=source:("The New York Times")&api-key=193841abf961eaa42f626bbfb13c9e68:15:69793059'
	url = url.replace(' ','%20')
	data = json.load(urllib2.urlopen(url))
	for i in range(len(data['response']['docs'])):
		title = data['response']['docs'][i]['headline']['main'].encode("ascii", "ignore")
		if (len(title) > 100):
			title = title[:100] + ' ... '
		news.append(dict(headline= title, date=data['response']['docs'][i]['pub_date'][:10].encode('utf-8'), url=data['response']['docs'][i]['web_url'].encode('utf-8')))
	news = perse_news(news)
	return news

