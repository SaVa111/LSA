# Латентно-семантический анализ(LSA)
Латентно-семантический анализ отображает документы и отдельные слова в так называемое «семантическое пространство», в котором и производятся все дальнейшие сравнения. При этом делаются следующие предположения:
<br>
1) Документы это просто набор слов. Порядок слов в документах игнорируется. Важно только то, сколько раз то или иное слово встречается в документе.<br>
2) Семантическое значение документа определяется набором слов, которые как правило идут вместе. Например, в биржевых сводках, часто встречаются слова: «фонд», «акция», «доллар»<br>
3) Каждое слово имеет единственное значение. Это, безусловно, сильное упрощение, но именно оно делает проблему разрешимой.<br>
На первом шаге требуется составить частотную матрицу индексируемых слов. В этой матрице строки соответствуют индексированным словам, а столбцы — документам. В каждой ячейке матрицы указано какое количество раз слово встречается в соответствующем документе. <br>
Следующим шагом мы проводим сингулярное разложение полученной матрицы. Сингулярное разложение это математическая операция раскладывающая матрицу на три составляющих. Т.е. исходную матрицу M мы представляем в виде: <br>

M = U/*W/*Vt

где U и Vt – ортогональные матрицы, а W – диагональная матрица. Причем диагональные элементы матрицы W упорядочены в порядке убывания. Диагональные элементы матрицы W называются сингулярными числами.

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
import os
import stemmer

loadpath = 'F:\\LDA\\news\\'
savepath = 'F:\\LDA\\formatatednews\\'
items = os.listdir(loadpath)

f = open('F:\\LDA\\stopwords.txt')
stopwords = f.read().split()

def is_stopword(word):
	return word in stopwords

newlist = []
for name in items:
    if name.endswith(".txt"):
        newlist.append(name)

for file in newlist:
	f = open(loadpath + file, 'r')
	text = f.read()
	f.close()
	text = removelinks(text)
	for char in "~\`1234567890-=+!@#$%^&*”“–—»«‘’©„(){}[]:;\'\"|\\<>?/.,":  
		text = text.replace(char,'') 
	wordlist = text.split()
	
	stems = []
	for word in wordlist:
		if word.isdigit() or is_stopword(word):
			wordlist.remove(word)
		word = stemmer.Porter.stem(word)
		if not (len(word) < 2 or is_stopword(word)):
			stems.append(word)
	
	f = open(savepath + file, 'w+')
	for word in stems:
		f.write(word + '\n')
	f.close()
```
Далее скрипт createdict.py составляет словать для всех слов используемых уже отформатированными текстами. Из словоря исключаются слова что встречаются реже 20 раз и чаще 400.
```python
import os

loadpath = 'F:\\LDA\\formatatednews\\'
items = os.listdir(loadpath)

LOW_LIMIT = 20
HIGHT_LIMIT = 400

files = []
for name in items:
    if name.endswith(".txt"):
        files.append(name)

dict = {}
for file in files:
	#print(file)
	f = open(loadpath + file, 'r')
	text = f.read()
	f.close()
	words = text.split()
	for word in words:
		if dict.get(word) is None:
			dict[word] = 1
		else:
			dict[word] += 1

dict = sorted(dict.items(), key=lambda kv: kv[1])

newdict = {}
for word, count in dict:
	if count > LOW_LIMIT and count < HIGHT_LIMIT:
		newdict[word] = count
allstems = newdict.keys()

f = open('F:\\LDA\\dict.txt', 'w+')
for word in allstems:
	f.write(word + '\n')
```
Скрипт createMatrix составляет матрицу для каждого слова из словоря и для каждого документа, в каждой ячейке храня количество употребления iго слова в jм документе. Далее применяется нормализация данной матрицы методом TF-IDF. К полученной матрице применяется сингулярное разложение матрицы, после чего оно сохраняется в соответсвующие файлы.
