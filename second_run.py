import os
from system_handler import writeListToFile, getLineFromTextFile, openDir
from share_function import splitLine

def secondRun(fileName, dirIn, dirOut):

	pathIn = os.path.join(dirIn, fileName)

	pathOut = os.path.join(dirOut, fileName)

	lines = getLineFromTextFile(pathIn)

	lineTuple = []

	for line in lines:
		if(line):
			key, text = splitLine(line)
			lineTuple.append((key, text))
	#print(lineTuple)

	span = []
	lineMap = []

	for i in range(len(lineTuple) - 1):
		#print(lineTuple[i])
		#key = lineTuple[i][0]
		#value = lineTuple[i][1]
		#print(key, value)
		if (lineTuple[i][0] == lineTuple[i+1][0]):
			#match
			span.append(i)
		else:
			span.append(i)
			lineMap.append(span)
			span = []

		#last item
		if (i == len(lineTuple) - 2):
			#print('i+1:', i+1)
			#print(lineTuple[i], lineTuple[i+1])
			if (lineTuple[i][0] != lineTuple[i+1][0]):
				span=[]
				span.append(i+1)
				lineMap.append(span)


	dataOut = []
	#print(lineMap)
	for items in lineMap:
		if len(items) == 1:
			#print('single', items)
			#print()
			idx = items[0]
			#print(lineTuple[idx])
			line = lineTuple[idx][0] + lineTuple[idx][1]
			#print(line)
			dataOut.append(line)
		else:
			#print('series', items)
			header = ''
			text = ''
			for idx in items:
				if lineTuple[idx]:
					#print(lineTuple[idx][0],  lineTuple[idx][1])
					if not header:
						header = lineTuple[idx][0]
					text += lineTuple[idx][1] + '|'
			line = header + text
			dataOut.append(line)


	writeListToFile(dataOut, pathOut)
	#openDir(dirOut)

if __name__ == "__main__":
	
	dirIn = 'E:/FULLTEXT/LEXICO/OUTPUT'
	dirOut = 'E:/FULLTEXT/LEXICO/COMPACT/'
	fileList = os.listdir(dirIn)
	for item in fileList:
		secondRun(item, dirIn, dirOut)
	
	#for debug
	#item = fileList[0]
	#print('item:', item)
	secondRun(item, dirIn, dirOut)


	openDir(dirOut)