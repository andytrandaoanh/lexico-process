import os
from system_handler import writeListToFile, openDir, getFilePath
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
	
	fileList = os.listdir(dirIn)
	
	for item in fileList:
		processHTML(item, dirIn, dirOut)
		#print(pathIn)
	
	openDir(dirOut)