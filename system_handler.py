import os, sys
from datetime import datetime

def openDir(targetdir):
	#open directory when done	
	rpath = os.path.realpath(targetdir)
	os.startfile(rpath)

def getFilePath(pathIn, dirOut):
	EXT = ".txt"
	temp_path = pathIn
	temp_path = os.path.basename(temp_path)
	fname, fext = os.path.splitext(temp_path)
	pathOut =  os.path.join(dirOut, fname + EXT) 
	#pathOut =  os.path.join(dirOut, FILNAME_OUT) 
	return pathOut
	
def getIncrementDataPath(incNumber, dataOutDir):
	PADDING_ZEROS = 8
	HTML_HEADER = "Lexico_Extract_Data_"
	HTML_EXT = ".html"
	incString = str(incNumber)
	increment = incString.zfill(PADDING_ZEROS)	
	data_path =  os.path.join(dataOutDir, HTML_HEADER + increment + HTML_EXT) 
	return(data_path)

def getIncrementLogPath(incNumber, logOutDir):
	PADDING_ZEROS = 8
	TEXT_HEADER = "Lexico_Extract_Log_"
	TEXT_EXT = ".txt"
	incString = str(incNumber)
	increment = incString.zfill(PADDING_ZEROS)		
	log_path =  os.path.join(logOutDir, TEXT_HEADER + increment + TEXT_EXT) 
	return(log_path)

def getDatedFilePath(prefix, dirOut):
	time_now = datetime.now()
	time_string = time_now.strftime("%Y%m%d_%H%M%S")
	temp_path = prefix + time_string + ".txt"
	pathOut =  os.path.join(dirOut, temp_path) 
	return(pathOut)

def getDateStamp():
	getDateStamp = str(datetime.now())
	return(getDateStamp)
	

def readTextFile(filepath):
	try:
	    ofile = open(filepath, 'r', encoding = 'utf-8') 
	    data = ofile.read()
	    return data
	except FileNotFoundError:
	    print("file not found")    
	except Exception as e:
	    print(e)  


def getLineFromTextFile(filepath):
    try:
        ofile = open(filepath, 'r', encoding = 'utf-8') 
        data = ofile.read()
        lines = data.split('\n')
        return lines

    except FileNotFoundError:
        print("file not found")    
    except Exception as e:
        print(e)    
        

def writeListToFile(vlist, vpath):
    with open(vpath, 'w', encoding ='utf-8') as file:
        for item in vlist:    
            file.write(item + "\n")

 

def loadDictionaries(dirDic):
	dicFiles = os.listdir(dirDic)
	bigDic = []
	for fp in dicFiles:
		bigDic  += fileToList(os.path.join(dirDic, fp))

	dicData = list(dict.fromkeys(bigDic))
	dicData.sort()
	return dicData


def writeJSON(data, pathOut):
	with open(pathOut, 'w', encoding ="utf-8") as outfile:  
		json.dump(data, outfile)

