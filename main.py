import sys, time 	
import requests, json
import system_handler as sysHand
from alternate_agent import getRamdomUserAgent
from start_private_proxy import startPrivateProxy
from bs4 import BeautifulSoup
import lxml



def getSingleWord(wordIn, proxies, headers):
	
	DATA_STATUS_OK = 200

	apiCompatibleWord = wordIn.replace(' ' , '_').lower()
	apiCompatibleWord = apiCompatibleWord .replace('/' , '%')


	url =  "https://www.lexico.com/en/definition/" + apiCompatibleWord

	response = requests.get(url, proxies=proxies, headers=headers)


	if (response.status_code == DATA_STATUS_OK):
		if (response.content):
			try:
				soup = BeautifulSoup(response.content, 'lxml')
				data = str(soup)
				statusMessage = "Successfully get the word: " + wordIn + "=>" + apiCompatibleWord
				return (data, statusMessage) 
			except:				
				statusMessage = "An exception occurred while getting "  + wordIn + "=>" + apiCompatibleWord
				return (None, statusMessage)

	else:		
		statusMessage = "Fail to remotely get the word " + wordIn
		return (None, statusMessage)



def runDownLoad(START_NUMBER, proxies, headers, mode, location):
	
	PATH_IN = "E:/FULLTEXT/DICTIONARY/NORMALCASE/Combined Lexico Oxford.txt"

	
	DIR_DATA_OUT = ''
	DIR_LOG_OUT = ''


	print('Path In:', PATH_IN)
	#For Home only

	if (mode == "local"):
		DIR_DATA_OUT = "E:/FULLTEXT/LEXICO/HTML"
		DIR_LOG_OUT = "E:/FULLTEXT/LEXICO/LOG"
	
	elif (mode == "remote"):
		if (location == "home"):
			DIR_DATA_OUT = "C:/Users/Andy Anh/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/HTML"
			DIR_LOG_OUT = "C:/Users/Andy Anh/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/LOG"
		elif (location == "office"): 
			DIR_DATA_OUT = "C:/Users/Administrator/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/HTML"
			DIR_LOG_OUT = "C:/Users/Administrator/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/LOG"

	print('\nData Path:', DIR_DATA_OUT, '\nLog Path:', DIR_LOG_OUT)



	STOP_NUMBER = START_NUMBER + 10

	print('starting at:', START_NUMBER)
	print('using agent:', headers['User-Agent'])
	urlTest = "http://icanhazip.com"
	resTest = requests.get(urlTest, proxies=proxies, headers=headers)
	print('using IP:', resTest.text)


	#NOTE: LOG IS FOR EVERY BATCH
	#pathDataOut, pathStatusOut = sysHand.getIncrementPath(START_NUMBER, PATH_DATA_OUT, PATH_LOG_OUT)
	pathStatusOut = sysHand.getIncrementLogPath(START_NUMBER, DIR_LOG_OUT)

	wordList = sysHand.getLineFromTextFile(PATH_IN)
	
	#results = []
	status = []
	dateStamp = sysHand.getDateStamp()
	status.append('Starting scraping Lexico at  ' + dateStamp)
	status.append('Starting scraping at index ' + str(START_NUMBER))
	status.append('Starting scraping using IP ' + resTest.text)
	status.append('Starting scraping using agent ' + headers['User-Agent'])



	for i in range(START_NUMBER, STOP_NUMBER):
		pathDataOut = sysHand.getIncrementDataPath(i, DIR_DATA_OUT)
		word = wordList[i]
		(htmlData, message) = getSingleWord(word, proxies, headers)
		if(htmlData):
			with open(pathDataOut, "w", encoding='utf-8') as file:
				file.write(htmlData)
		print(i, ':',  message)
		status.append(str(i) + ' ' + message)
		time.sleep(5)

	#sysHand.writeDataToJSON(results, pathDataOut)
	dateStamp = sysHand.getDateStamp()
	status.append('Ending scraping Lexico at ' + dateStamp)
	sysHand.writeListToFile(status, pathStatusOut)


def startLoop(startNumber, mode, location):
	#START_NUMBER = 107200
	START_NUMBER = startNumber 
	STOP_NUMBER	 = START_NUMBER + 10000
	STEP_NUMBER = 10

	proxies = startPrivateProxy()

	for i in range(START_NUMBER, STOP_NUMBER, STEP_NUMBER):		
		user_agent = getRamdomUserAgent()		
		headers = {'User-Agent': user_agent}
		runDownLoad(i, proxies, headers, mode, location)
		time.sleep(15)


if __name__ == '__main__':
	try:

		#default argument
		startNumber = 1	
		mode = "local"
		location = "home"


		lenArgs = len(sys.argv)
		#print('length of argument list:', lenArgs)

		if (lenArgs > 1):
			startNumber = int(sys.argv[1])			
		
		if (lenArgs > 2):
			if (sys.argv[2] == "local" or sys.argv[2] == "remote"):
				mode = sys.argv[2]

		if (lenArgs > 3):
			if (sys.argv[3] == "home" or sys.argv[3] == "office"):
				location = sys.argv[3]


		print('\nstartNumber:', startNumber, '\nmode:', mode, '\nlocation:', location)
		startLoop(startNumber, mode, location)



	except Exception as e:
		print (e)

		
