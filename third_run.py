import os, json
import system_handler as sh
from share_function import splitLine
import single_word as sw
from pprint import pprint


fileName = 'A-star.txt'
fileNameJSON = fileName.replace(".txt", ".json")
dirIn = 'E:/FULLTEXT/LEXICO/COMPACT'
dirOut = 'E:/FULLTEXT/LEXICO/JSON'
pathIn = os.path.join(dirIn, fileName)
pathOut = os.path.join(dirOut, fileNameJSON)
lines = sh.getLineFromTextFile(pathIn)

sLines = []

#STEP 1: CREATE A LINE MAP TO MARK WHERE SECTIONS START

if(lines):
	for line in lines:
		if(line):
			key, text = splitLine(line)
			sLines.append((key,text))

	#run for significant index
	lineMap =[]
	idx = 0
	sectionList = ['[headword]','[category]', '[secphrases]', '[secphrasal]','[secusage]','[secpronun]', '[secorigin]']

	for sLine in sLines:
		#print(sLine[0], sLine[1])
		#if sLine[0] == '[headword]'
		for section in sectionList:
			if (sLine[0]) == section:
				lineMap.append((section, idx))

		idx += 1		


#STEP 2: EXTRACT START AND END INDEX FOR EACH SECTION
#print('lineMap:', lineMap)

idxMap = []
for i in range(len(lineMap)-1):
	tup = (lineMap[i][0], lineMap[i][1], lineMap[i+1][1])
	idxMap.append(tup)
	if (i == len(lineMap)-2):
		lastIdx = i + 1
		#print(lineMap[lastIdx][1])
		tup = (lineMap[lastIdx][0], lineMap[lastIdx][1], len(lines) -1)
		idxMap.append(tup)

	


#STEP 3: HANDLE EACH SECTION
#print('\nindex map:', idxMap)

objectList = []
for item in idxMap:
	sectionName, firstIdex, lastIndex = item
	sectLines =[]
	for i in range(firstIdex, lastIndex):
		sectLines.append(lines[i])	
	
	if (sectionName == '[headword]'):
		objHW = sw.processHeadWordLines(sectLines)
		objectList.append(objHW)
		#print(objHW)
	elif (sectionName == '[category]'):
		objCategory = sw.processCategoryLines(sectLines)
		objectList.append(objCategory)
		
	elif (sectionName == '[secphrases]'):
		objPhrases = sw.processPhraseLines(sectLines)
		objectList.append(objPhrases)

	elif (sectionName == '[secphrasal]'):
		objPhrases = sw.processPhraseVerbLines(sectLines)
		objectList.append(objPhrases)

	elif (sectionName == '[secusage]'):
		objUsage = sw.processUsageLines(sectLines)
		objectList.append(objUsage)
	
	elif (sectionName == '[secorigin]'):
		objOrigin = sw.processOriginLines(sectLines)
		objectList.append(objOrigin)
	
	elif (sectionName == '[secpronun]'):
		objPhonetic = sw.processPhoneticLines(sectLines)
		objectList.append(objPhonetic)





#STEP 4: MERGE OBJECTS
masterObject = {}
for obj in objectList:
	for key in obj:
		masterObject[key] = obj[key]


#@pprint(masterObject)


#STEP 5: WRITE OUT JSON FILE
with open(pathOut, 'w', encoding ="utf-8") as outfile:  
	json.dump(masterObject, outfile)
sh.openDir(dirOut)
	

