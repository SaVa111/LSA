import os
import math
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plot

loadpath = 'F:\\LDA\\formatatednews\\'
items = os.listdir(loadpath)

files = []
for name in items:
    if name.endswith(".txt"):
        files.append(name)
		
f = open('F:\\LDA\\dict.txt', 'r')
text = f.read()
dict = text.split()
dict.reverse()

print(len(dict))
print(len(files))
matrix = np.zeros((len(dict), len(files)))

wordscount = []
for i in range(0, len(files)):
	f = open(loadpath + files[i], 'r')
	text = f.read()
	f.close()
	words = text.split()
	wordscount.append(len(words))
	print(files[i])
	for word in words:
		matrix[dict.index(word), i] = matrix[dict.index(word), i] + 1
		
#print(matrix)

docsword = []
for string in matrix:
	count = 0
	for c in string:
		if c != 0:
			count = count + 1
	docsword.append(count)
	
#print(wordscount)
#print(docsword)

#for i in range(0, len(dict)):
#	idf = math.log10(len(files) / docsword[i])
#	for j in range(0, len(files)):
#		print(files[j], dict[i])
#		tf = matrix[i, j] / wordscount[j]
#		matrix[i, j] = tf * idf
#print(matrix)
u, s, vh = linalg.svd(matrix)
np.savetxt('F:\\LDA\\u.txt', u)
np.savetxt('F:\\LDA\\s.txt', s)
np.savetxt('F:\\LDA\\vh.txt', vh)

plot.plot(u[:, 0], u[:, 1], 'go')
plot.plot(vh[0, :], vh[1, :], 'ro')

for i, txt in enumerate(dict):
    plot.annotate(txt, (u[i, 0], u[i, 1]))
for i, txt in enumerate(files):
    plot.annotate(txt, (vh[0, i], vh[1, i]))

plot.show()


#print(u, s, vh)