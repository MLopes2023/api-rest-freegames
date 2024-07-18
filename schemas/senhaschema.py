from datetime               import datetime
from pydantic               import BaseModel
from typing                 import Optional, List
from models.tabelas.senha   import Senha

   
class SenhaInputAuthSchema(BaseModel):
    """ Representação da estrutura para autenticação senha do usuário.
    """
    emailpwd:str  = "exemplo@gmail.com"
    senhapwd: str = "12345"
    
class SenhaAuthVisualizaSchema(BaseModel):
    """ Representação da forma que a autenticação da senha do usuário será retornada.
    """
    idusuario:int           = 1
    situacaoauth:bool       = True
    mensagemauth:str        = "Usuário autenticado com sucesso."
    
def retorna_senha_autenticacao(idusuarioauth:int, situacaoauth:bool, mensagemauth:str  ):
    """ Retorna uma representação de auteticação da senha do usuário, seguindo o schema definido em SenhaCriacaoVisualizaSchema.
    """
    return {
       "idusuarioauth": idusuarioauth,
       "situacaoauth":  situacaoauth,
       "mensagemauth":  mensagemauth
    }
    