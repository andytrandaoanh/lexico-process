import configparser
config = configparser.ConfigParser()

CONFIGFILE = 'lexicon.ini'

try:
    fh = open(CONFIGFILE, 'r')
    # Store configuration file values
    print("config file found!")
    fh.close()
    
except FileNotFoundError:
    # create file ini
    config['DEFAULT'] = {
    'InputFilePath': 'input.txt',
    'NormalOutputPath': 'output.txt',
    'SpecialOutputPath': 'special.txt'}

    with open(CONFIGFILE, 'w') as configfile:
    	config.write(configfile)
     