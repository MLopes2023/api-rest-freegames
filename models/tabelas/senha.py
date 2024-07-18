from sqlalchemy     import Column, String, Integer, DateTime, ForeignKey 
from datetime       import datetime
from typing         import Union
from models.base    import Base
from models.tabelas.usuario import Usuario

#Tabela de usuários 
class Senha(Base):
    __tablename__ = "senha"

    idusuariopwd            = Column(Integer,       ForeignKey(Usuario.idusuario), primary_key=True)
    senhapwd                = Column(String(30),    primary_key=True)
    dtvigenciapwd           = Column(DateTime,      default=datetime.now(),         nullable=False)
    
    # Define chave primária composta
    #__table_args__ = (
    #    PrimaryKey(idusuariopwd, senhapwd, unique=True),
    #    {},
    #)
    
    # construtor
    def __init__(self,  idusuariopwd:int,        senhapwd:str,  dtvigenciapwd:Union[DateTime, None] = None  ):
        """
        Inseri senha

        Arguments:
            idusuariopwd: Id do usuário
            senhapwd: Senha 
            dtvigenciapwd: Data/hora de vigência da senha
        """
        self.idusuariopwd   = idusuariopwd
        self.senhapwd       = senhapwd
        
        if not dtvigenciapwd:
            self.dtvigenciapwd = datetime.now()
        else:
            self.dtvigenciapwd = dtvigenciapwd
  
    def to_dict(self):
        """
        Retorna dicionário do objeto senha.
        """
        return{
            "idusuariopwd": self.idusuariopwd,
            "senhapwd": self.senhapwd,
            "dtvigenciapwd": self.dtvigenciapwd
        }

    def __repr__(self):
        """
        Retorna senha em forma de texto.
        """
        return f"Senha(idusuariopwd={self.idusuariopwd}, senhapwd={self.senhapwd}, dtvigenciapwd={self.dtvigenciapwd})"            
    