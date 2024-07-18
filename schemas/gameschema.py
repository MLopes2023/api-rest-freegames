from datetime               import datetime
from pydantic               import BaseModel
from typing                 import List
from models.tabelas.game    import Game

class GameBodySchema(BaseModel):
    """ Representação da forma para inserção e edição do game do usuário.
    """
    idusuariogame: int = 0
    idgame: int = 0
    observacao: str = ""
    
class GameVisualizaSchema(GameBodySchema):
    """ Representação da forma que um game do usuário cadastrado será retornado.
    """
    dtcadastrogame:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dtalteracaogame:datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
    
class GameIdBuscaSchema(BaseModel):
    """ Representação da estrutura para busca de um determinado game do usuário.
    """
    idusuariogame: int = 0     
    idgame: int =  0 

class GameDeleteIdBuscaSchema(BaseModel):
    """ Representação da estrutura para busca de um determinado game do usuário a ser excluído.
    """
    idusuariogame: int
    idgame: int

class GameDeleteSchema(BaseModel):
    """ Representação da estrutura do dado retornado após uma requisição de exclusão de um game do usuário.
    """
    mensagem: str

class ListaGame(BaseModel):
    """ Define uma lista de games que deverão ser retornados.
    """
    games:List[GameVisualizaSchema]

def retorna_game(game: Game):
    """ Retorna uma representação de um game do usuário, seguindo o schema definido em GameVisualizaSchema.
    """
    return {
       "idusuariogame": game.idusuariogame,
       "idgame": game.idgame,
       "observacao": game.observacao,
       "dtcadastro": game.dtcadastrogame.strftime("%Y-%m-%d %H:%M:%S"),
       "dtalteracao": game.dtalteracaogame.strftime("%Y-%m-%d %H:%M:%S")
    }
    
def retorna_game_atualizado(booladicionar, bodyatu, game_original:Game = None):
    """ Retorna objeto game atualizado, seguindo o schema definido em GameBodySchema ou GameBodyEditarSchema.
    """
    
    # atualiza body 
    if booladicionar:
        game_original = Game(       idusuariogame=bodyatu.idusuariogame,               idgame=bodyatu.idgame,                  
                                    observacao=bodyatu.observacao   )
    else:        
        game_original.observacao        = bodyatu.observacao
        game_original.dtalteracaogame   = datetime.now()
        
    return game_original
    
    