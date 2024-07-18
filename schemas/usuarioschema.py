from datetime               import datetime
from pydantic               import BaseModel
from typing                 import List
from models.tabelas.usuario import Usuario

class UsuarioBodySchema(BaseModel):
    """ Representação da forma do usuário para inserção e edição.
    """
    email: str = "usuario@gmail.com"
    nome: str = "PAULO SOARES"
    cep: str = "20030021"
    endereco: str = "RUA DA AJUDA"
    numero: str = "S/N"
    complemento: str = "CASA 1"
    cidade: str = "RIO DE JANEIRO"
    bairro: str = "CENTRO"
    uf: str = "RJ"

class UsuarioInsereBodySchema(UsuarioBodySchema):
    """ Representação da forma que um novo usuário será inserido.
    """
    senhapwd: str = "12345"

class UsuarioBodyEditarSchema(UsuarioBodySchema):
    """ Representação da forma que um usuário será editado.
    """
    idusuario:int = 1
   
class UsuarioVisualizaSchema(UsuarioBodySchema):
    """ Representação da forma que um usuário será retornado.
    """
    idusuario:int = 1
    dtcadastro:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dtalteracao:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class UsuarioIdBuscaSchema(BaseModel):
    """ Representação da estrutura para busca de um determinado usuário conforme id informado.
    """
    idusuario: int

class UsuarioDeleteSchema(BaseModel):
    """ Representação da estrutura do dado retornado após uma requisição de exclusão de um usuário.
    """
    mensagem: str

class ListaUsuario(BaseModel):
    """ Define uma lista de usuários que deverão ser retornados.
    """
    usuarios:List[UsuarioVisualizaSchema]

def retorna_usuario(usuario: Usuario):
    """ Retorna uma representação de um usuário, seguindo o schema definido em UsuarioVisualizaSchema.
    """
    return {
       "idusuario": usuario.idusuario,
       "email": usuario.email,
       "nome": usuario.nome,
       "cep": usuario.cep,
       "endereco": usuario.endereco,
       "numero": usuario.numero,
       "complemento": usuario.complemento,
       "cidade": usuario.cidade,
       "bairro": usuario.bairro,
       "uf": usuario.uf,
       "dtcadastro": usuario.dtcadastro.strftime("%Y-%m-%d %H:%M:%S"),
       "dtalteracao": usuario.dtalteracao.strftime("%Y-%m-%d %H:%M:%S")
    }
    
def retorna_usuario_atualizado(booladicionar, bodyatu, usuario_original:Usuario = None):
    """ Retorna objeto usuário atualizado, seguindo o schema definido em UsuarioBodySchema ou UsuarioBodyEditarSchema.
    """
    
    # atualiza body 
    if booladicionar:
        usuario_original = Usuario(  email=bodyatu.email,               nome=bodyatu.nome,                  cep=bodyatu.cep,
                                     endereco=bodyatu.endereco,         numero=bodyatu.numero,              complemento=bodyatu.complemento,    
                                     cidade=bodyatu.cidade,             bairro=bodyatu.bairro,              uf=bodyatu.uf   )
    else:        
        usuario_original.email = bodyatu.email
        usuario_original.nome=bodyatu.nome
        usuario_original.cep=bodyatu.cep
        usuario_original.endereco=bodyatu.endereco
        usuario_original.numero=bodyatu.numero
        usuario_original.complemento=bodyatu.complemento
        usuario_original.cidade=bodyatu.cidade
        usuario_original.bairro=bodyatu.bairro
        usuario_original.uf=bodyatu.uf
        usuario_original.dtalteracao = datetime.now()
        
    return usuario_original
