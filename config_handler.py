import os, configparser


class ConfigHandler:
    config = configparser.ConfigParser()
    #do not remove this line - needed to preserve case
    config.optionxform = str

    CONFIG_FILE = "lexicon.ini"
    RECENT = 'RECENTS'
    RECENT_FILE_NUMBER = 'RecentFileNumber'
    
    RECENT_DATA = {}



    def prepare_default_config(self):

        self.RECENT_DATA[self.RECENT_FILE_NUMBER] = "1"


    def read_config(self):
        try:
            self.config.read(self.CONFIG_FILE)
            options = self.config.options(self.RECENT)
            for opt in options:
                self.RECENT_DATA[opt] = self.config.get(self.RECENT, opt)
        except Exception as e:
            self.reset_config_file()


    def write_config(self):
        cfgfile = open(self.CONFIG_FILE,'w')
        
        try:
            if not self.config.has_section(self.RECENT): 
                self.config.add_section(self.RECENT)
        
            for key, value in self.RECENT_DATA.items():
                self.config.set(self.RECENT, key, value)

            self.config.write(cfgfile)
        except Exception as e:
            print(e)

        cfgfile.close()


    def reset_config_file(self):
        self.prepare_default_config()
        self.write_config()



    def get_config_value(self, key):
        exists = os.path.isfile(self.CONFIG_FILE)
        if exists:
            self.read_config()

        else:
            self.prepare_default_config()
            
        return self.RECENT_DATA[key]



    def set_config_value(self, key, value):
        exists = os.path.isfile(self.CONFIG_FILE)
        if exists:
            self.read_config()
        else:
            self.prepare_default_config()

        self.RECENT_DATA[key] = value

        self.write_config()






def main():
    cf = ConfigHandler()
    cf.reset_config_file()

