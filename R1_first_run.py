import os
from system_handler import writeListToFile, openDir
from system_handler import getDatedFilePath, getDateStamp
from process_lexico_word import processLexico
import config_handler


def processHTML(fileName, dirIn, dirOut):
	fileOut = fileName.replace(".html", ".txt")
	pathIn = os.path.join(dirIn, fileName)
	pathOut = os.path.join(dirOut, fileOut)
	#print('\npathIn:', pathIn, '\npathOut:', pathOut)
	wordData =[]
	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		wordData = processLexico(contents)
		
	writeListToFile(wordData, pathOut)



if __name__ == "__main__":
	
	dirIn = 'E:/FULLTEXT/LEXICO/HTML'
	dirOut = 'E:/FULLTEXT/LEXICO/TEXT'
	dirLog = 'E:/FULLTEXT/LEXICO/LOG'
	cf = config_handler.ConfigHandler()
	recentFile = cf.get_config_value(cf.RECENT_OPEN_FILE)
	#print(recentFile)
	fileList = os.listdir(dirIn)
	lastFile = ''
	prefix = 'Lexicon_First_Run_Log_'
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
			processHTML(item, dirIn, dirOut)
	
	#WRITE INI
	cf.set_config_value(cf.RECENT_OPEN_FILE, lastFile)	
	timeStamp = getDateStamp()
	message = 'Finished processing at ' + timeStamp
	logData.append(message)
	print(message)
	writeListToFile(logData, logPath)
	openDir(dirOut)
	
