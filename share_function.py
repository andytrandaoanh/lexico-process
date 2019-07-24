import re


def splitLine(line):
	obj = re.search(r'\[[\w]+\]', line)
	key = obj.group(0)
	temp = line.split(key)
	text = temp[1]
	return (key, text)



if __name__ == "__main__":

	line = '[headword]a'
	key, text = splitLine(line)
	print(key, text)