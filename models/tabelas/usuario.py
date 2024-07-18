from sqlalchemy     import Column, String, Integer, DateTime
from datetime       import datetime
from typing         import Union
from models.base    import Base

#Tabela de usuários 
class Usuario(Base):
    __tablename__ = "usuario"

    idusuario               = Column(Integer,       primary_key=True, autoincrement=False )
    email                   = Column(String(150),   unique=True)
    nome                    = Column(String(100),   nullable=False)
    cep                     = Column(String(8),     nullable=False)
    endereco                = Column(String(80),    nullable=False)
    numero                  = Column(String(15),    nullable=False)
    complemento             = Column(String(50),    nullable=True)
    cidade                  = Column(String(50),    nullable=False)
    bairro                  = Column(String(50),    nullable=False)
    uf                      = Column(String(2),     nullable=False)
    dtcadastro              = Column(DateTime,      default=datetime.now(),     nullable=False)
    dtalteracao             = Column(DateTime,      default=datetime.now(),     nullable=False)
    
    #construtor
    def __init__(self,  email:str,      nome:str,       
                        cep:str,        endereco:str,   
                        numero:str,     complemento:str,    
                        cidade:str,     bairro:str,     
                        uf:str,         dtcadastro:Union[DateTime, None] = None, 
                        dtalteracao:Union[DateTime, None] = None  ):
        """
        Cria usuário

        Arguments:
            email: E-mail 
            nome: Nome 
            cep: CEP
            endereco: Endereço
            numero: Número
            complemento: Complemento
            cidade: Cidade
            bairro: Bairro
            uf: UF     
            dtcadastro: Data/hora do cadastro
            dtalteracao: Data/hora da alteração
        """
        self.email      = email
        self.nome       = nome
        self.cep        = cep
        self.endereco   = endereco
        self.numero     = numero
        self.complemento= complemento
        self.cidade     = cidade
        self.bairro     = bairro
        self.uf         = uf
        
        if not dtcadastro:
            self.dtcadastro = datetime.now()
        else:
            self.dtcadastro = dtcadastro
  
        if not dtalteracao:
            self.dtalteracao = datetime.now()
        else:
            self.dtalteracao = dtalteracao
            
    def to_dict(self):
        """
        Retorna dicionário do objeto usuario.
        """
        return{
            "idusuario": self.idusuario,
            "email": self.email,
            "nome": self.nome,
            "cep": self.cep,
            "endereco": self.endereco,
            "numero": self.numero,
            "complemento": self.complemento,
            "cidade": self.cidade,
            "bairro": self.bairro,
            "uf": self.uf,
            "dtcadastro": self.dtcadastro,
            "dtalteracao": self.dtalteracao
        }

    def __repr__(self):
        """
        Retorna usuario em forma de texto.
        """
        return f"Usuario(idusuario={self.idusuario}, email={self.email}, nome={self.nome},\
                         cep={self.cep},  endereco={self.endereco},numero={self.numero},\
                         complemento={self.complemento}, cidade={self.cidade}, bairro={self.bairro},\
                         uf={self.uf},dtcadastro={self.dtcadastro}, dtalteracao={self.dtalteracao})"     
                                
    