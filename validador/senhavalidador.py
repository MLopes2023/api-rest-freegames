from util.util                              import Util
from schemas.senhaschema                    import *

# Classe responsável pela valiadação das informações de entrada de chamadas das api's senha.
class SenhaValidador:
    def __init__(self, bodyvalid):
        
        # Inicializa variaveis 
        self.__body         = bodyvalid;
        self.__mensagem     = ""
            
        # Efetua validação
        self.__validar()
        
    @property
    def mensagemvalidador(self):
        return self.__mensagem
    
    def __validar(self):
        # valida campos
        if not Util.get_str_tamanho_valido(self.__body.emailpwd, 5, 150):
            self.__mensagem = "E-mail não informado ou com quantidade de caracteres inválida."    
        elif not Util.get_email_valido(self.__body.emailpwd):
            self.__mensagem = "E-mail inválido."        
        elif not Util.get_str_tamanho_valido(self.__body.senhapwd, 5, 30):
            self.__mensagem = "Senha não informada ou com quantidade de caracteres menor que 5 ou maior que 10."              
       