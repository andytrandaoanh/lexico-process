from system_handler import writeListToFile

def ProcessSingleHeadword(word, lines, idx):
	pathOut = 'E:/FULLTEXT/LEXICO/OUTPUT/' + word + '_' + str(idx) + '.txt'
	writeListToFile(lines, pathOut)
