from util.util                              import Util
from schemas.usuarioschema                  import *
from database.operacao.datatabase_operacao  import DatabaseOperacao

# Classe responsável pela valiadação das informações de entrada de chamadas das api's do usuário.
class UsuarioValidador:
    def __init__(self, operacao:str, bodyvalid):
        
        # Inicializa variaveis 
        self.__idusuario = 0;
        self.__body      = bodyvalid;
        self.__mensagem   = ""
        
        # Recupera identificação do tipo de operação
        dboperacao      = DatabaseOperacao()
        self.__inclusao = dboperacao.is_inclusao(operacao)
        self.__alteracao= dboperacao.is_alteracao(operacao)
        self.__exclusao = dboperacao.is_exclusao(operacao)

        # recupera id do usuário na alteração ou exclusão
        if self.__alteracao or self.__exclusao:
            self.__idusuario = self.__body.idusuario
            
        # Efetua validação
        self.__validar()
        
    @property
    def mensagemvalidador(self):
        return self.__mensagem
    
    def __validar(self):
        
        # valida id do usuário somente na alteração  e exclusão
        if not self.__inclusao:
            if self.__idusuario <= 0 or self.__idusuario == None:
                self.__mensagem = "id do usuário não informado ou menor ou igual a zero."    
                return 
        
        # valida senha do usuário somente na inclusão
        if  self.__inclusao:
            if (not self.__exclusao  and (Util.get_str_nulo_sem_valor(self.__body.senhapwd))):
                self.__mensagem = "Senha não informada."    
                return 
            elif not Util.get_str_tamanho_valido(self.__body.senhapwd, 5, 10):
                self.__mensagem = "Senha deve ter no minimo 5 e no máximo 10 caracteres."    
                return 
       
        # valida campos independente da operação    
        if (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.email, 5, 150))):
            self.__mensagem = "E-mail não informado ou com quantidade de caracteres menor que 5 ou maior que 150."    
        elif not Util.get_email_valido(self.__body.email):
            self.__mensagem = "E-mail inválido."            
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.nome, 3, 100))):
            self.__mensagem = "Nome não informado ou com quantidade de caracteres menor que 3 ou maior que 100."    
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.cep, 8, 8))):
            self.__mensagem = "CEP não informado  ou com quantidade de caracteres diferente de 8."    
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.endereco, 2, 80))):
            self.__mensagem = "Endereço não informado ou com quantidade de caracteres menor que 2 ou maior que 80."    
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.numero, 1, 15))):
            self.__mensagem = "Número do endereço não informado ou com quantidade de caracteres menor que 1 ou maior que 15."    
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.cidade, 2, 50))):
            self.__mensagem = "Cidade não informada ou com quantidade de caracteres menor que 2 ou maior que 50."                
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.bairro, 2, 50))):
            self.__mensagem = "Bairro do endereço não informado ou com quantidade de caracteres menor que 2 ou maior que 50."    
        elif (not self.__exclusao  and (not Util.get_str_tamanho_valido(self.__body.uf, 2, 2))):
            self.__mensagem = "UF não informada ou com quantidade de caracteres diferente de 2."    
            
        
       