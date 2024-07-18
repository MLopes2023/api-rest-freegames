import pathlib
from configparser import ConfigParser

class Database_Ini:
    def __init__(self, filename='database.ini', section='default'):
        
        # set lista de bancos disponíveis
        self.__bdname_lista = ["default", "mysql", "postgresql", "sqlite"]
        
        #recupera banco de dados conforme parâmetro passado no construtor da classe
        self.config = {}
        self.__load_config(filename, section)
        
    @property
    def default(self):
        return self.__bdname_lista[0]
    
    @property
    def mysql(self):
        return self.__bdname_lista[1]

    @property
    def postgresql(self):
        return self.__bdname_lista[2]
    
    @property
    def sqlite(self):
        return self.__bdname_lista[3]

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
        
    def get_url_db(self):
        params =  self.config 

        if params['bdname'] == self.postgresql:
            db_url = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
                SGBD = "postgresql+psycopg2",
                usuario = params['user'],
                senha = params['password'],
                servidor = params['host'],
                database = params['database']
            )
        elif params['bdname'] == self.mysql:
            db_url = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
                SGBD = "mysql+mysqlconnector",
                usuario = params['user'],
                senha = params['password'],
                servidor = params['host'],
                database = params['database']
            )    
        elif params['bdname'] == self.sqlite:
            db_url = "{SGBD}:///{servidor}/{database}".format(
                SGBD = "sqlite",
                #usuario = params['user'],
                #senha = params['password'],
                servidor = params['host'],
                database = params['database']
            )       
        return db_url            
