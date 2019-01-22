# Латентно-семантический анализ(LSA)

### Загрузка веб-страниц

Скрипт upload.py загружает 1000 новостей с сайта goodgame.ru и сохраняет их в текстовые файлы с соответствующим id в качестве названия

```python
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
```
Далее скрипт formatate.py форматирует все тексты удаляя из них стоп-слова(слова, что встречаются почти во всех текстах и не несут смысловой нагрузки), также применяется к словам стеммиг по алгоритму Портера.
```python
import re

class Porter:
	PERFECTIVEGROUND =  re.compile(u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$")
	REFLEXIVE = re.compile(u"(с[яь])$")
	ADJECTIVE = re.compile(u"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$")
	PARTICIPLE = re.compile(u"((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$")
	VERB = re.compile(u"((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$")
	NOUN = re.compile(u"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$")
	RVRE = re.compile(u"^(.*?[аеиоуыэюя])(.*)$")
	DERIVATIONAL = re.compile(u".*[^аеиоуыэюя]+[аеиоуыэюя].*ость?$")
	DER = re.compile(u"ость?$")
	SUPERLATIVE = re.compile(u"(ейше|ейш)$")
	I = re.compile(u"и$")
	P = re.compile(u"ь$")
	NN = re.compile(u"нн$")

	def stem(word):
		word = word.lower()
		word = word.replace(u'ё', u'е')
		m = re.match(Porter.RVRE, word)
		if m is None:
			return word
		if m.groups():
			pre = m.group(1)
			rv = m.group(2)
			temp = Porter.PERFECTIVEGROUND.sub('', rv, 1)
			if temp == rv:
				rv = Porter.REFLEXIVE.sub('', rv, 1)
				temp = Porter.ADJECTIVE.sub('', rv, 1)
				if temp != rv:
					rv = temp
					rv = Porter.PARTICIPLE.sub('', rv, 1)
				else:
					temp = Porter.VERB.sub('', rv, 1)
					if temp == rv:
						rv = Porter.NOUN.sub('', rv, 1)
					else:
						rv = temp
			else:
				rv = temp
			
			rv = Porter.I.sub('', rv, 1)

			if re.match(Porter.DERIVATIONAL, rv):
				rv = Porter.DER.sub('', rv, 1)

			temp = Porter.P.sub('', rv, 1)
			if temp == rv:
				rv = Porter.SUPERLATIVE.sub('', rv, 1)
				rv = Porter.NN.sub(u'н', rv, 1)
			else:
				rv = temp
			word = pre+rv
		return word
	stem=staticmethod(stem)
```
