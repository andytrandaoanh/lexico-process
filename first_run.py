import os
import system_handler as sh
from single_word import ProcessSingleHeadword

def firstRun(word, filePath):

	lines = sh.getLineFromTextFile(filePath)

	#FIRST RUN 
	#Purpose is to determine number of headwords
	hwIndexes = []
	idx = 0
	for line in lines:
		if '[headword]' in line:
			hwIndexes.append(idx)
		idx += 1
	hwTotal = len(hwIndexes) 
	if (hwTotal > 1):
		#print('multiple headwords')
		#print(hwIndexes)
		idxList = []
		for i in range(hwTotal-1):
			#print(hwIndexes[i], hwIndexes[i+1] - 1)
			tup = (hwIndexes[i], hwIndexes[i+1])
			idxList.append(tup)
		lastTup = (hwIndexes[hwTotal-1], len(lines) -1)
		idxList.append(lastTup)
		wordNum = 0
		for tup in idxList:
			lowRange = tup[0]
			highRange = tup[1]
			wordNum += 1
			newLines = []
			for k in range(lowRange, highRange):
				newLines.append(lines[k])
			ProcessSingleHeadword(word, newLines, wordNum)
		#print(lines[217])

	else:
		#print('single headword')
		ProcessSingleHeadword(word, lines, 0)


if __name__ == "__main__":
	dirIn = 'E:/FULLTEXT/LEXICO/TEXT'
	fileList = os.listdir(dirIn)
	for item in fileList:
		word = item.replace('.txt', '')
		pathIn = os.path.join(dirIn, item)
		firstRun(word, pathIn)
		#print(pathIn)
	