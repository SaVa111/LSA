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
#print(newdict)
		
for file in files:
	f = open(loadpath + file, 'r')
	text = f.read()
	f.close()
	words = text.split()

	newwords = []
	for word in words:
		if newdict.get(word) is not None:
			newwords.append(word)

	if len(newwords) < 10:
		os.remove(loadpath + file)
		continue

	f = open(loadpath + file, 'w+')
	for word in newwords:
		f.write(word + '\n')
	f.close()