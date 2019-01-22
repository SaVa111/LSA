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

def removelinks(s):
	regex = "[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
	return re.sub(regex, '', s)

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