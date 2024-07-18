from datetime                   import datetime
from pydantic                   import BaseModel
from typing                     import List
from models.tabelas.game        import Game
from models.tabelas.freetogame  import FreeToGame


class FreeToGameBodySchema(BaseModel):
    """ Representação da forma de retorno da busca de um game da lista do usuário.
    """
    idusuariogame: int = 0
    idgame: int =  0 
    observacao: str = ""
    dtcadastrogame:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dtalteracaogame:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    titulo:str= ""
    capa:str      = ""                 
    descricao:str     = ""         
    urlgame:str = ""
    genero:str = ""                    
    plataforma:str = ""            
    urlgameperfil:str = ""
    dtlancamento:str = datetime.now().strftime("%Y-%m-%d") 

class FreeToGameIdBuscaSchema(BaseModel):
    """ Representação da estrutura para busca de um determinado game da lista do usuário conforme id's do usuário e game informado.
    """
    idusuariogame: int
    idgame: int 

class FreeToGameIdTituloBuscaSchema(BaseModel):
    """ Representação da estrutura para busca da lista de games do usuário, conforme id do usuário ou parte do título.
    """
    idusuariogame: int = 0     
    liketitulo:str = None    

class ListaFreeToGames(BaseModel):
    """ Define uma lista de games do usuário que deverão ser retornados.
    """
    freetogames:List[FreeToGameBodySchema]

def retorna_game_freeetogame_atualizado(model:Game, freetogamedict):
    return FreeToGame(  model.idusuariogame,            model.idgame,
                        model.observacao,               model.dtcadastrogame,
                        model.dtalteracaogame ,         freetogamedict['titulo'],
                        freetogamedict['capa'],         freetogamedict['descricao'],
                        freetogamedict['urlgame'],      freetogamedict['genero'],
                        freetogamedict['plataforma'],   freetogamedict['urlgameperfil'],
                        freetogamedict['dtlancamento']      )

def retorna_game_freeetogame(freeetogame: FreeToGame):
    """ Retorna uma representação de um game da lista do usuário, seguindo o schema definido em FreeToGameBodySchema.
    """
    return {
       "idusuariogame": freeetogame.idusuariogame,   
       "idgame": freeetogame.idgame,
       "observacao": freeetogame.observacao,
       "dtcadastrogame": freeetogame.dtcadastrogame.strftime("%Y-%m-%d %H:%M:%S"),
       "dtalteracaogame": freeetogame.dtalteracaogame.strftime("%Y-%m-%d %H:%M:%S"),
       "titulo": freeetogame.titulo,
       "capa": freeetogame.capa,
       "descricao": freeetogame.descricao,
       "urlgame": freeetogame.urlgame,
       "genero": freeetogame.genero,
       "plataforma": freeetogame.plataforma,
       "urlgameperfil": freeetogame.urlgameperfil,
       "dtlancamento": freeetogame.dtlancamento
    }    

def retorna_games_freeetogame(games: List[FreeToGame]):
    """ Retorna uma representação da lista de games do usuário, seguindo o schema definido em FreeToGameBodySchema.
    """
    result = []
    for game in games:
        result.append({
            "idusuariogame": game.idusuariogame,   
            "idgame": game.idgame,
            "observacao": game.observacao,
            "dtcadastrogame": game.dtcadastrogame.strftime("%Y-%m-%d %H:%M:%S"),
            "dtalteracaogame": game.dtalteracaogame.strftime("%Y-%m-%d %H:%M:%S"),
            "titulo": game.titulo,
            "capa": game.capa,
            "descricao": game.descricao,
            "urlgame": game.urlgame,
            "genero": game.genero,
            "plataforma": game.plataforma,
            "urlgameperfil": game.urlgameperfil,
            "dtlancamento": game.dtlancamento
        })

    return {"freetogames": result}
    