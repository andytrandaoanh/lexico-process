import os
from system_handler import writeListToFile, openDir, getLineFromTextFile
from system_handler import getDatedFilePath, getDateStamp
from process_lexico_word import processLexico
import config_handler
from run_library import ProcessSingleHeadword


def splitHeadWord(lines, word, dirOut):

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
			ProcessSingleHeadword(word, newLines, wordNum, dirOut)
		#print(lines[217])

	else:
		#print('single headword')
		ProcessSingleHeadword(word, lines, 0, dirOut)
	message = 'File ' + word + ' is split into ' +  str(hwTotal) + ' files'
	return message 

def processRawText(item, dirIn, dirOut):
	word = item.replace('.txt', '')
	pathIn = os.path.join(dirIn, item)

	lines = getLineFromTextFile(pathIn)
	lineTotal =  len(lines)
	if lineTotal == 1 and not lines[0].strip():
		message = 'File ' + word + ' is empty' 
	else:
		message = splitHeadWord(lines, word, dirOut)
	
	return message



if __name__ == "__main__":
	
	dirIn = 'E:/FULLTEXT/LEXICO/TEXT'
	dirOut = 'E:/FULLTEXT/LEXICO/TEXT2'
	dirLog = 'E:/FULLTEXT/LEXICO/LOG'
	cf = config_handler.ConfigHandler()
	recentFile = cf.get_config_value(cf.RECENT_OPEN_FILE2)
	#print(recentFile)
	fileList = os.listdir(dirIn)
	lastFile = ''
	prefix = 'Lexicon_Second_Run_Log_'
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
			message = processRawText(item, dirIn, dirOut)
			logData.append(message)
			print(message)
	
	#WRITE INI
	cf.set_config_value(cf.RECENT_OPEN_FILE2, lastFile)	
	timeStamp = getDateStamp()
	message = 'Finished processing at ' + timeStamp
	logData.append(message)
	print(message)
	writeListToFile(logData, logPath)
	openDir(dirOut)
	
