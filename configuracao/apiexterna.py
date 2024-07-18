import pathlib
from configparser import ConfigParser

class ConfigApiExterna:
    def __init__(self, section, filename='apiexterna.ini' ):
        
        # set lista de apis disponíveis
        self.__apiname_lista = ["api-externa"]
        
        #recupera fonte api conforme parâmetro passado no construtor da classe
        self.config = {}
        self.__load_config(filename, section)
        
    @property
    def api_externa(self):
        return self.__apiname_lista[0]
    
    def __load_config(self, filename, section):
        config_path = pathlib.Path(__file__).parent.absolute() / filename 
        parser = ConfigParser()
        parser.read(config_path)

        # get section
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    def get_url_api_externa(self):
        params    =  self.config 
        urlstring = params['urlstring']
        return urlstring            
