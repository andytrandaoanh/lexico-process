import re


def splitLine(line):
	obj = re.search(r'\[[\w]+\]', line)
	key = obj.group(0)
	temp = line.split(key)
	text = temp[1]
	return (key, text)

def listToString(inputList):
	#SPLIT AND REPACK LIST SEPERATED BY PIPE CHARACTER
	#print('composing...')
	stringOutput = ''
	if(inputList):
		if ('|' in inputList):
			items = inputList.split('|')
			for item in items:
				if (item):
					if (stringOutput):
						stringOutput += ', ' + item
					else:
						stringOutput = item
		else:
			stringOutput = inputList

	return stringOutput	


def listToList(inputList):
	#SPLIT AND REPACK LIST SEPERATED BY PIPE CHARACTER
	#print('composing...')
	outputList = []
	if(inputList):
		if ('|' in inputList):
			items = inputList.split('|')
			for item in items:
				if (item):
					outputList.append(item)
		else:
			outputList.append(inputList) 

	return outputList




if __name__ == "__main__":

	line = '[headword]a'
	key, text = splitLine(line)
	print(key, text)