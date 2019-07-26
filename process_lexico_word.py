import re
from bs4 import BeautifulSoup
import lxml
from system_handler import writeListToFile, openDir, getFilePath
from pprint import pprint


def processSpan(item):
	#spanString = str(item)
	#spanText = item.get_text()
	spans = []
	if item.has_attr('class'):
		className = item['class'][0] 
		if(className == 'hw'):
			spanText = item.get_text().strip()
			if(spanText):				
				sup = item.find('sup')
				if(sup):
					#print('sup text:', sup.get_text())
					supText =  sup.get_text()		
					temp = spanText.replace(supText, '')
					span =  '[headword]' + temp
					spans.append(span)
					span = '[graphnum]' + supText
					spans.append(span)
				else:
					span =  '[headword]' + spanText
					spans.append(span)


		elif(className == 'phoneticspelling'):
			if(item.get_text().strip()):
				span = '[phonetic]' + item.get_text()
				spans.append(span)
		elif(className == 'pos'):
			if(item.get_text().strip()):
				span = '[category]' + item.get_text()
				spans.append(span)
		elif(className == 'iteration'):
			if(item.get_text().strip()):
				span = '[sensenum]' + item.get_text()
				spans.append(span)
		elif(className == 'subsenseIteration'):
			if(item.get_text().strip()):
				span = '[sensenum]' + item.get_text()
				spans.append(span)		
		elif(className == 'inflection-text'):
			temp = item.get_text().strip()
			itemText = temp.replace(',', '') 
			if(itemText):
				span = '[inflects]' + itemText
				spans.append(span)

		elif(className == 'form-groups'):
			if(item.get_text().strip()):
				span = '[notebold]' + item.get_text()
				spans.append(span)
				
		elif(className == 'grammatical_note'):
			if(item.get_text().strip()):
				span = '[notegram]' + item.get_text()
				spans.append(span)
		elif(className == 'sense-registers'):
			if(item.get_text().strip()):
				span = '[notetone]' + item.get_text()
				spans.append(span)
		elif(className == 'sense-regions'):
			if(item.get_text().strip()):
				span = '[notearea]' + item.get_text()
				spans.append(span)				
		elif(className == 'ind'):
			if(item.get_text().strip()):
				span = '[meanings]' + item.get_text()
				spans.append(span)
		elif(className == 'syn'):
			if(item.get_text().strip()):
				span = '[synonyms]' + item.get_text()
				spans.append(span)




	return spans

def processDiv(item):
	divData = []

	if item.has_attr('class'):
		className = item['class'][0] 
		if(className == 'variant'):
			div = '[variants]' + item.get_text()
			divData.append(div)
		elif (className == 'senseInnerWrapper'):
			if item.parent.has_attr('class'):
				parentClass = item.parent['class'][0]
				if (parentClass == 'etymology'):
					textH3 = item.parent.find('h3').get_text()
					textP = item.find('p').get_text()
					if (textH3 == 'Usage'):						
						div = '[wrdusage]' + textP
						divData.append(div)
					elif (textH3 == 'Origin'):
						div = '[wordroot]' + textP
						divData.append(div)
		elif (className == 'crossReference'):
			div = '[crossref]' + item.get_text()
			divData.append(div)



					
	return divData


def processEm(item):
	em = ''
	
	if item.parent.has_attr('class'):
		parentClass = item.parent['class'][0]
		if (parentClass == 'ex'):
			itemText = item.get_text()
			if(itemText):
				em = '[examples]' + itemText.strip()		
	
	return(em)

def processStrong(item):
	strong = ''
	
	if item.has_attr('class'):
		itemClass = item['class'][0]
		if (itemClass == 'phrase'):
			itemText = item.get_text()
			if(itemText):
				strong = '[phrshead]' + itemText.strip()		
		elif (itemClass == 'syn'):
			itemText = item.get_text()
			if(itemText):
				strong = '[synonyms]' + itemText.strip()			
	else:
		itemText = item.get_text()
		if (itemText == 'Phrasal Verbs'):
			strong = '[secphrasal]Phrasal Verbs'
		elif (itemText == 'Phrases'):
			strong = '[secphrases]Phrases'
		elif (itemText == 'Pronunciation'):
			strong = '[secpronun]Pronunciation'
		elif (itemText == 'Usage'):
			strong = '[secusage]Usage'
		elif (itemText == 'Origin'):
			strong = '[secorigin]Origin'


	return strong



	


def processLexico(contents):
	soup = BeautifulSoup(contents, "lxml")
	itemList = soup.find_all(['span', 'em', 'div', 'strong'])
	#itemList = soup.find_all('span')
	#pprint(itemList)
	
	itemData = []

	for item in itemList:
		if (item.name == 'span'):
			wordSpans = processSpan(item)
			#pprint(wordSpans)
			if(wordSpans):
				#pprint(wordSpans)
				for wordSpan in wordSpans:
					itemData.append(wordSpan)
		elif (item.name == 'em'):
			wordEm = processEm(item)
			if(wordEm):
				itemData.append(wordEm)
		elif (item.name == 'div'):
			wordDivs = processDiv(item)
			#pprint(wordDivs)
			if(wordDivs):
				for wordDiv in wordDivs:
					itemData.append(wordDiv)
		elif (item.name == 'strong'):
			wordStrong = processStrong(item)
			if(wordStrong):
				itemData.append(wordStrong)
	return itemData

	#entryList = soup.find_all('div', {'class' : 'entryWrapper'})
	#print(len(entryList))
	#for item in entryList:
	#	print(item)

	

	

if __name__ == "__main__":

	WORD = "Aboriginalization"
	dirOut = "E:/FULLTEXT/LEXICO/TEXT"
	pathIn = "E:/FULLTEXT/LEXICO/HTML/" + WORD + ".html"
	pathOut = getFilePath(pathIn, dirOut)
	
	#print(pathOut)
	
	wordData =[]

	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		wordData = processLexico(contents)
	
	
	writeListToFile(wordData, pathOut)
	openDir(dirOut)

		
