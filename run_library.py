from system_handler import writeListToFile
from share_function import splitLine, listToString, listToList
from pprint import pprint

def ProcessSingleHeadword(word, lines, idx, dirOut):
	if (idx > 0):
		pathOut = dirOut + '/' + word + '_' + str(idx) + '.txt'
	else:
		pathOut = dirOut + '/' + word + '.txt'

	writeListToFile(lines, pathOut)


def processSimpleHeadword(sectLines):
	# CREATE AND RETURN A HEADWORD OBJECT
	headwordObject = {}

	headWordDict = {
		'[headword]': 'head-word', 
		'[graphnum]': 'homograph-index', 
		'[variants]': 'spelling-variants', 
		'[graphnum]': 'homograph-index',
		'[phonetic]': 'phonetic-transcripts',
		'[crossref]': 'cross-reference'
		}
	

	for line in sectLines:
		#print('\n', line)
		key, text = splitLine(line)
		newKey = headWordDict[key]
		newText = listToString(text)
		headwordObject[newKey] = newText
		#print('newKey', newKey, 'newText', newText)

	return headwordObject

def processHeadWordLines(sectLines):
	# DETERMINE IF THIS IS SIMPLE OR COMPLEX HEADWORD
	#pprint(sectLines)
	
	
	complexHeadWord = False
	hwLastIndex = 0
	num = 0
	for line in sectLines:
		key, text = splitLine(line)
		if (key == '[sensenum]' or key == '[meanings]' or key == '[examples]'): 
			complexHeadWord = True
			hwLastIndex = num
			#print('last index:', hwLastIndex)
			break
		num += 1

	if complexHeadWord:

		newHeadWordLines = []
		newSenseLines = []
		for i in range(hwLastIndex):
			newHeadWordLines.append(sectLines[i])
		for k in range(hwLastIndex, len(sectLines)):
			newSenseLines.append(sectLines[k])
		
		complexObject = processSimpleHeadword(newHeadWordLines)
		senseObject =  processMeanings(newSenseLines)
		#merge to objext
		for key in senseObject:
			complexObject[key] = senseObject[key]
		return complexObject
			
	else:
		simpleObject = processSimpleHeadword(sectLines)
		return simpleObject


def processCategoryHeader(headLines):
	objectOut = {}
	categoryKey =''

	for line in headLines:
		key, text = splitLine(line)
		if (key == '[category]'):
			categoryKey = text
			objectOut[categoryKey] = {'senses': []}
		elif (key == '[inflects]'):
			textInflects = listToString(text)
			objectOut[categoryKey]['inflections'] = textInflects

	return (objectOut, categoryKey)

def processMeanings(senseLines):
	objectOut = {}
	termDict = {
		'[sensenum]': 'sense-number', 
		'[notegram]': 'grammer-notes',
		'[meanings]': 'meaning',
		'[examples]': 'examples',
		'[synonyms]': 'synonyms',
		'[notebold]': 'highlight',
		'[notetone]': 'register',
		'[notearea]': 'region-domain',
		'[crossref]': 'cross-reference',
		'[variants]': 'spelling-variants'
		}

	for line in senseLines:
		#print('\n', line)
		key, text = splitLine(line)
		newKey = termDict[key]
		if (key == '[examples]'):
			newText = listToList(text)
		else:	
			temp = listToString(text)
			newText= temp.replace(', ,', ',')
		objectOut[newKey] = newText

	#pprint(objectOut)
	return objectOut

def processComplexCategory(sectLines):
	#PROCESSING A PART OF SPEECH	
	num = 0
	lineMap = []
	
	#STEP 1: EXTRACT START INDEXES OF PART OF SPEECH HEADER AND MEANINGS
	for line in sectLines:
		key, text = splitLine(line)
		#print('\nkey:', key, 'text:', text)
		if (key == '[category]'):
			lineMap.append((key, num))
		elif (key == '[sensenum]'):
			lineMap.append((key, num))
		num += 1

	#STEP 2: EXTRACT START AND END INDEXES
	idxMap = []
	for i in range(len(lineMap)-1):
		tup = (lineMap[i][0], lineMap[i][1], lineMap[i+1][1])
		idxMap.append(tup)
		if (i == len(lineMap)-2):
			lastIdx = i + 1
			#print(lineMap[lastIdx][1])
			tup = (lineMap[lastIdx][0], lineMap[lastIdx][1], len(sectLines) -1)
			idxMap.append(tup)

	#STEP 3: PROCESS EACH PART
	objectSenses = []
	objCatHeader = {}
	categoryKey =''

	for item in idxMap:
		partName, firstIdex, lastIndex = item
		partLines =[]
		for i in range(firstIdex, lastIndex):
			partLines.append(sectLines[i])	
		
		if (partName == '[category]'):
			objCatHeader, categoryKey = processCategoryHeader(partLines)
			
			#print(objHW)
		if (partName == '[sensenum]'):
			objMeaning = processMeanings(partLines)
			objectSenses.append(objMeaning)


	#ASSEMBLY
	objCatHeader[categoryKey]['senses'] = objectSenses
	#pprint(objCatHeader)

	return objCatHeader

def processSimpleCategory(sectLines):
	objectOut = {}
	
	termDict = {
		'[notegram]': 'grammar-notes',
		'[meanings]': 'meaning',
		'[examples]': 'examples',
		'[synonyms]': 'synonyms',
		'[notebold]': 'highlight',
		'[notetone]': 'register',
		'[notearea]': 'region-domain',
		'[crossref]': 'cross-reference'
		}


	categoryKey = ''
	for line in sectLines:
		key, text = splitLine(line)
		if (key == '[category]'):
			categoryKey = text
			objectOut[categoryKey] = {'senses': [{}]}
		elif (key == '[inflects]'):
			textInflects = listToString(text)
			objectOut[categoryKey]['inflections'] = textInflects
		else:
			newKey = termDict[key]
			if (key == '[examples]'):
				newText = listToList(text)
			else:	
				temp = listToString(text)
				newText= temp.replace(', ,', ',')
			
			objectOut[categoryKey]['senses'][0][newKey] = newText


	#pprint(objectOut)
	return objectOut



def processCategoryLines(sectLines):
	#FIRST MAKE SURE THIS IS SIMPLE OF COMPLEX CATEGORY
	#pprint(sectLines)
	senseTotal = 0

	for line in sectLines:
		key, text = splitLine(line)
		if (key == '[sensenum]'):
			senseTotal += 1
	#print('senseTotal', senseTotal)

	objectList = []

	if (senseTotal > 0):
		#print('complex')
		objectList = processComplexCategory(sectLines)
	else:
		#print('simple')
		objectList = processSimpleCategory(sectLines)

	return objectList



def processUsageLines(sectLines):
	objectOut = {}
	for line in sectLines:
		key, text = splitLine(line)
		#print('key:', key, 'text:', text)
		if (key == '[wrdusage]'):
			objectOut['usage'] = text
	#print(objectOut)
	return objectOut


def processOriginLines(sectLines):
	objectOut = {}
	for line in sectLines:
		key, text = splitLine(line)
		#print('key:', key, 'text:', text)
		if (key == '[wordroot]'):
			objectOut['word-origin'] = text
	#print(objectOut)
	return objectOut


def processPhoneticLines(sectLines):
	objectOut = {}
	for line in sectLines:
		key, text = splitLine(line)
		#print('key:', key, 'text:', text)
		if (key == '[phonetic]'):
			temp = listToString(text)
			objectOut['phonetic'] = temp
	#print(objectOut)
	return objectOut


def processSimplePhrase(lines):
	objectOut = {}
	

	termDict = {
		'[phrshead]': 'phrase',
		'[notegram]': 'grammar-notes',
		'[meanings]': 'meaning',
		'[examples]': 'examples',
		'[synonyms]': 'synonyms',
		'[notebold]': 'highlight',
		'[notetone]': 'register',
		'[notearea]': 'region-domain',
		'[sensenum]': 'sense-number',
		'[crossref]': 'cross-reference'
	}


	for line in lines:
		key, text = splitLine(line)
		newKey = termDict[key]
		if (key == '[examples]'):
			newText = listToList(text)
		else:	
			temp = listToString(text)
			newText= temp.replace(', ,', ',')		
		objectOut[newKey] = newText
	return objectOut


def processComplexPhrase(phraseLines):
	objPhraseList = []
	phraseHead = ''
	lineMap =[]
	num = 0
	for line in phraseLines:
		key, text = splitLine(line)
		#print('\nkey:', key, 'text:', text)
		if (key == '[phrshead]'):
			phraseHead = text
		elif (key == '[sensenum]'):
			lineMap.append((key, num))
		num += 1

	#pprint(lineMap)
	#STEP 2: EXTRACT START AND END INDEXES
	idxMap = []
	for i in range(len(lineMap)-1):
		tup = (lineMap[i][0], lineMap[i][1], lineMap[i+1][1])
		idxMap.append(tup)
		if (i == len(lineMap)-2):
			lastIdx = i + 1
			#print(lineMap[lastIdx][1])
			tup = (lineMap[lastIdx][0], lineMap[lastIdx][1], len(phraseLines) -1)
			idxMap.append(tup)	
	#pprint(idxMap)
	#STEP 3: PROCESS EACH PART

	for item in idxMap:
		partName, firstIdex, lastIndex = item
		partLines =[]
		for i in range(firstIdex, lastIndex):
			partLines.append(phraseLines[i])	
		
		if (partName == '[sensenum]'):
			objPhrasePart = processSimplePhrase(partLines)
			objPhrasePart['phrase'] = phraseHead
			objPhraseList.append(objPhrasePart)

	#pprint(objPhraseList)
	return objPhraseList


def processPhrase(phraseLines):
	#COUNT NUMBER OF SENSES TO DECIDE SIMPLE OR COMPLEX PHRASE
	objectList = []
	senseTotal = 0
	for line in phraseLines:
		key, text = splitLine(line)
		#print('\nkey:', key, 'text:', text)

		if (key == '[sensenum]'):
			senseTotal += 1

	if (senseTotal > 0):
		#print('complex phrase')
		objList = processComplexPhrase(phraseLines)

	else:
		#print('simple phrase')
		objectPhrase = processSimplePhrase(phraseLines)
		objectList.append(objectPhrase)		


	return objectList



def processPhraseLines(sectLines):
	objectOut = {}
	#STEP 1: EXTRACT START INDEXES OF PART OF SPEECH HEADER AND MEANINGS
	lineMap = []
	num = 0
	for line in sectLines:
		key, text = splitLine(line)
		#print('\nkey:', key, 'text:', text)
		if (key == '[phrshead]'):
			lineMap.append((key, num))

		num += 1

	#print(lineMap)
	#STEP 2: EXTRACT START AND END INDEXES
	idxMap = []
	for i in range(len(lineMap)-1):
		tup = (lineMap[i][0], lineMap[i][1], lineMap[i+1][1])
		idxMap.append(tup)
		if (i == len(lineMap)-2):
			lastIdx = i + 1
			#print(lineMap[lastIdx][1])
			tup = (lineMap[lastIdx][0], lineMap[lastIdx][1], len(sectLines) -1)
			idxMap.append(tup)

	#print(idxMap)


	#STEP 3: PROCESS EACH PART
	objectPhrases = []

	for item in idxMap:
		partName, firstIdex, lastIndex = item
		partLines =[]
		for i in range(firstIdex, lastIndex):
			partLines.append(sectLines[i])	
		
		if (partName == '[phrshead]'):
			objPhrase = processPhrase(partLines)
			objectPhrases.append(objPhrase)	

	newObjectList = [item for item in objectPhrases if item]
	
	objectOut['phrases'] = newObjectList

	return objectOut




def processPhraseVerbLines(sectLines):

	objectOut = {}
	#STEP 1: EXTRACT START INDEXES OF PART OF SPEECH HEADER AND MEANINGS
	lineMap = []
	num = 0
	for line in sectLines:
		key, text = splitLine(line)
		#print('\nkey:', key, 'text:', text)
		if (key == '[phrshead]'):
			lineMap.append((key, num))

		num += 1

	#print(lineMap)
	#STEP 2: EXTRACT START AND END INDEXES
	idxMap = []
	for i in range(len(lineMap)-1):
		tup = (lineMap[i][0], lineMap[i][1], lineMap[i+1][1])
		idxMap.append(tup)
		if (i == len(lineMap)-2):
			lastIdx = i + 1
			#print(lineMap[lastIdx][1])
			tup = (lineMap[lastIdx][0], lineMap[lastIdx][1], len(sectLines) -1)
			idxMap.append(tup)

	#print(idxMap)


	#STEP 3: PROCESS EACH PART
	objectPhrases = []

	for item in idxMap:
		partName, firstIdex, lastIndex = item
		partLines =[]
		for i in range(firstIdex, lastIndex):
			partLines.append(sectLines[i])	
		
		if (partName == '[phrshead]'):
			objPhrase = processPhrase(partLines)
			objectPhrases.append(objPhrase)			

	#remove empty phrase
	newObjectList = [item for item in objectPhrases if item]

	objectOut['phrases-verbs'] = newObjectList

	return objectOut