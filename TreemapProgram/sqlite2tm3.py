import sqlite3, sys, operator

pathToDB = "/Users/alexandrecourouble/Documents/Research/postgres/postgres/data.db"

"""change to dir passed in args if applicable"""
try:
	if sys.argv[1] != None:
		DIR = sys.argv[1]
except IndexError:
	"""default dir"""
	DIR = "doc"





connection = sqlite3.connect(pathToDB)
cursor = connection.cursor()

rows = []
filesAndAuthorsTemp = {}

for row in cursor.execute("SELECT author,filename FROM blame"):
	# if DIR + "/" in row[1]:
	# 	rows.append(row)
	# 	if row[1] not in filesAndAuthorsTemp.keys():
	# 		filesAndAuthorsTemp[row[1]] = [row[0]]
	# 	else: 
	# 		filesAndAuthorsTemp[row[1]].append(row[0])
	rows.append(row)
	if row[1] not in filesAndAuthorsTemp.keys():
		filesAndAuthorsTemp[row[1]] = [row[0]]
	else: 
		filesAndAuthorsTemp[row[1]].append(row[0])

# fileName = "authorData" + DIR + ".tm3"
fileName = "postgresData.tm3"
outputTM3 = open(fileName, "w")
outputTM3.write('"File Name"\t"Author"\t"Percentage Owned"\n')
outputTM3.write("STRING\tSTRING\tFLOAT\n")

for i in filesAndAuthorsTemp:
	authors = {}
	for j in filesAndAuthorsTemp[i]:
		if j not in authors.keys():
			authors[j] = 1
		else:
			authors[j] += 1
	author = max(authors.iteritems(), key=operator.itemgetter(1))[0]
	# print i, author, 100*(float(authors[author])/float(len(filesAndAuthorsTemp[i])))
	split = i.split("/")
	# print split[len(split)-1]
	outputLine = split[len(split)-1] + "\t" + author + "\t" + str(100*(float(authors[author])/float(len(filesAndAuthorsTemp[i])))) + "\t" 
	for k in split:
		outputLine = outputLine + k + "\t"
	outputTM3.write(outputLine + "\n")


outputTM3.close()