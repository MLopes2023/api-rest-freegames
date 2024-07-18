from sqlalchemy     import Column, String, Integer, DateTime, ForeignKey 
from datetime       import datetime
from typing         import Union
from models.base    import Base
from models.tabelas.usuario import Usuario

#Tabela de games 
class Game(Base):
    __tablename__ = "game"

    idusuariogame   = Column(Integer,       ForeignKey(Usuario.idusuario), primary_key=True)
    idgame          = Column(Integer,       primary_key=True)
    observacao      = Column(String(255),   nullable=False)
    dtcadastrogame  = Column(DateTime,      default=datetime.now(),     nullable=False)
    dtalteracaogame = Column(DateTime,      default=datetime.now(),     nullable=False)
    
    # construtor
    def __init__(self,  idusuariogame:int,  idgame:int,  observacao:str,  dtcadastrogame:Union[DateTime, None] = None, dtalteracaogame:Union[DateTime, None] = None  ):
        """
        Inseri game

        Arguments:
            idusuariogame: Id do usuário 
            idgame: Id do game
            observacao: Observação
            dtcadastrogame: Data/hora do cadastro
            dtalteracaogame: Data/hora da alteração
        """
        
        self.idusuariogame  = idusuariogame
        self.idgame         = idgame        
        self.observacao     = observacao
        
        if not dtcadastrogame:
            self.dtcadastrogame = datetime.now()
        else:
            self.dtcadastrogame = dtcadastrogame
            
        if not dtalteracaogame:
            self.dtalteracaogame = datetime.now()
        else:
            self.dtalteracaogame = dtalteracaogame            
  
    def to_dict(self):
        """
        Retorna dicionário do objeto game.
        """
        return{
            "idusuariogame": self.idusuariogame,
            "idgame": self.idusuariopwd,
            "dtcadastrogame": self.dtcadastrogame,
            "dtalteracaogame": self.dtalteracaogame
        }

    def __repr__(self):
        """
        Retorna game em forma de texto.
        """
        return f"Game(idusuariogame={self.idusuariogame}, idgame={self.idgame}, dtcadastrogame={self.dtcadastrogame}, dtalteracaogame={self.dtalteracaogame})"            
    