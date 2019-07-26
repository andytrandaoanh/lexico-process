
import os, json
from system_handler import writeListToFile, getLineFromTextFile, openDir
from system_handler import getDatedFilePath, getDateStamp
from share_function import splitLine
import config_handler
import run_library as runlib
from pprint import pprint


def runFourthProcess(fileName, dirIn, dirOut):
	
	fileNameJSON = fileName.replace(".txt", ".json")

	pathIn = os.path.join(dirIn, fileName)
	pathOut = os.path.join(dirOut, fileNameJSON)
	lines = getLineFromTextFile(pathIn)

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
			objHW = runlib.processHeadWordLines(sectLines)
			objectList.append(objHW)
			#print(objHW)
		elif (sectionName == '[category]'):
			objCategory = runlib.processCategoryLines(sectLines)
			objectList.append(objCategory)
			
		elif (sectionName == '[secphrases]'):
			objPhrases = runlib.processPhraseLines(sectLines)
			objectList.append(objPhrases)

		elif (sectionName == '[secphrasal]'):
			objPhrases = runlib.processPhraseVerbLines(sectLines)
			objectList.append(objPhrases)

		elif (sectionName == '[secusage]'):
			objUsage = runlib.processUsageLines(sectLines)
			objectList.append(objUsage)
		
		elif (sectionName == '[secorigin]'):
			objOrigin = runlib.processOriginLines(sectLines)
			objectList.append(objOrigin)
		
		elif (sectionName == '[secpronun]'):
			objPhonetic = runlib.processPhoneticLines(sectLines)
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

	message = 'Finished converting ' + fileName + ' to JSON' 
	return message


if __name__ == "__main__":
	
	dirIn = 'E:/FULLTEXT/LEXICO/TEXT3'
	dirOut = 'E:/FULLTEXT/LEXICO/JSON'
	dirLog = 'E:/FULLTEXT/LEXICO/LOG'
	cf = config_handler.ConfigHandler()
	recentFile = cf.get_config_value(cf.RECENT_OPEN_FILE4)
	#print(recentFile)
	fileList = os.listdir(dirIn)
	lastFile = ''
	prefix = 'Lexicon_Fourth_Run_Log_'
	logData = []
	logPath = getDatedFilePath(prefix, dirLog)
	#print('log path:', logPath)
	timeStamp = getDateStamp()
	message = 'Starting processing at ' + timeStamp
	logData.append(message)
	print(message)

	for item in fileList:
		if (item > recentFile):
			lastFile = item
			message = 'Processsing item ' + item
			logData.append(message)
			print(message)
			message = runFourthProcess(item, dirIn, dirOut)
			logData.append(message)
			print(message)
	
	#WRITE INI
	cf.set_config_value(cf.RECENT_OPEN_FILE4, lastFile)	
	timeStamp = getDateStamp()
	message = 'Finished processing at ' + timeStamp
	logData.append(message)
	print(message)
	writeListToFile(logData, logPath)
	openDir(dirOut)
	
