import urllib.parse
import urllib.request
import os
import lxml.html
from bs4 import BeautifulSoup as bs

url = "https://goodgame.ru/news/"
newsid = 27979
articleCount = 1000

i = 0
while (i < articleCount):
	try:
		resp = urllib.request.urlopen(url + str(newsid))
		respData = resp.read()
		soup = bs(respData, "lxml")
		textdiv = soup.find('div', class_="news-text cleafix")
		titlediv = soup.find('h1')

		title = str(titlediv)
		text = str(textdiv)
		title = lxml.html.fromstring(title).text_content()
		text = lxml.html.fromstring(text).text_content()
		
		f = open('F:\\LDA\\news\\' + str(newsid) + '.txt', 'w+')
		f.write(title)
		f.write(text)
		f.close()
		i = i + 1
	except:# urllib.error.HTTPError as err:
		print('id:' + str(newsid) + ' skiped')
		
	newsid = newsid - 1