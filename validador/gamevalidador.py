from util.util                              import Util
from schemas.gameschema                     import *
from database.operacao.datatabase_operacao  import DatabaseOperacao

# Classe responsável pela validação das informações de entrada de chamadas das api's do game.
class GameValidador:
    def __init__(self, queryvalid):
        
        # Inicializa variaveis 
        self.__body      = queryvalid;
        self.__mensagem   = ""
        
        # Efetua validação
        self.__validar()
        
    @property
    def mensagemvalidador(self):
        return self.__mensagem
    
    def __validar(self):
        
        # valida campos independente da operação    
        if self.__body.idusuariogame <= 0 or self.__body.idusuariogame == None:
            self.__mensagem = "id do usuário não informado ou menor ou igual a zero."    
            return 
        elif self.__body.idgame <= 0 or self.__body.idgame == None:
            self.__mensagem = "id do game igual a zero ou não informado."    
            return 

            
        
       