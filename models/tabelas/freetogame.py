from sqlalchemy     import Column, String, Integer, DateTime
from datetime       import datetime
#from typing         import Union
from models.base    import Base


#Tabela de games da lista de usuários anexada aos dados do game da api externa FreeToGame 
class FreeToGame(Base):
    __tablename__ = "freetogame"

    idusuariogame   = Column(Integer,       primary_key=True)
    idgame          = Column(Integer,       primary_key=True)
    observacao      = Column(String(255),   nullable=False)
    dtcadastrogame  = Column(DateTime,      nullable=False)
    dtalteracaogame = Column(DateTime,      nullable=False)
    titulo          = Column(String(300),   nullable=False)
    capa            = Column(String(255),   nullable=False)
    descricao       = Column(String(500),   nullable=False)
    urlgame         = Column(String(300),   nullable=False)
    genero          = Column(String(30),    nullable=False)
    plataforma      = Column(String(30),    nullable=False)
    urlgameperfil   = Column(String(300),   nullable=False)
    dtlancamento    = Column(String(10),    nullable=False)
    
    # construtor
    def __init__(self,  idusuariogame:int,              idgame:int,                 observacao:str,  
                        dtcadastrogame:datetime,        dtalteracaogame:datetime,   titulo:str,
                        capa:str,                       descricao:str,              urlgame:str,
                        genero:str,                     plataforma:str,             urlgameperfil:str,
                        dtlancamento:str   ):
        
        self.idusuariogame      = idusuariogame
        self.idgame             = idgame        
        self.observacao         = observacao
        self.dtcadastrogame     = dtcadastrogame
        self.dtalteracaogame    = dtalteracaogame
        self.titulo             = titulo
        self.capa               = capa
        self.descricao          = descricao
        self.urlgame            = urlgame
        self.genero             = genero
        self.plataforma         = plataforma
        self.urlgameperfil      = urlgameperfil
        self.dtlancamento       = dtlancamento