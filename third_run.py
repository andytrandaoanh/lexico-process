import os
import system_handler as sh
from share_function import splitLine

fileName = 'big_1.txt'
dirIn = 'E:/FULLTEXT/LEXICO/COMPACT'
dirOut = 'E:/FULLTEXT/LEXICO/JSON'
pathIn = os.path.join(dirIn, fileName)
pathOut = os.path.join(dirOut, fileName)
lines = sh.getLineFromTextFile(pathIn)

sLines = []

if(lines):
	for line in lines:
		if(line):
			key, text = splitLine(line)
			sLines.append((key,text))

	#run for significant index
	keyList =[]
	idx = 0
	tokenList = ['[headword]','[category]', '[wrdusage]', '[wordroot]']

	for sLine in sLines:
		#print(sLine[0], sLine[1])
		#if sLine[0] == '[headword]'
		for token in tokenList:
			if (sLine[0]) == token:
				keyList.append((token, idx))

		idx += 1		


print(keyList)