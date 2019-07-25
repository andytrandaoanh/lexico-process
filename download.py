import requests
from bs4 import BeautifulSoup
import lxml
import re
from system_handler import writeJSON, openDir
from alternate_agent import getRamdomUserAgent
from start_private_proxy import startPrivateProxy




def getLexico(word, proxies, headers):
	DATA_STATUS_OK = 200

	#result = requests.get("https://www.lexico.com/en/definition/" + word)
	


	url =  "https://www.lexico.com/en/definition/" + word
	
	response = requests.get(url, proxies=proxies, headers=headers)
	#response = session.get(url, headers=headers)

	if (response.status_code == DATA_STATUS_OK):
		if (response.content):
			try:
				soup = BeautifulSoup(response.content, 'lxml')
				#statusMessage = "Successfully get the word: " + word
							
				#print(data)
				return (str(soup)) 
			except:				
				#statusMessage = "An exception occurred while getting " + word
				return (None)
	



if __name__ == "__main__":

	WORD = "a"
	dirOut = "E:/FULLTEXT/LEXICO/HTML" 
	pathOut = dirOut + '/' +  WORD + ".html"

	proxies = startPrivateProxy()

	user_agent = getRamdomUserAgent()		
	headers = {'User-Agent': user_agent}


	formatWord = WORD.replace(' ' , '_').lower()
	
	
	htmlContent = getLexico(formatWord, proxies, headers)
	if(htmlContent):
		with open(pathOut, "w", encoding='utf-8') as file:
			file.write(htmlContent)
	openDir(dirOut)
	