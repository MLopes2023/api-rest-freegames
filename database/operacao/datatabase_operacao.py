class DatabaseOperacao():
    def __init__(self): 
        self.__operacao_lista = ["alterar", "excluir", "incluir"]
    
    # Propriedades de identificação do tipo de operação no banco de dados
    @property
    def alterar(self):
        return self.__operacao_lista[0]

    @property
    def excluir(self):
        return self.__operacao_lista[1]

    @property
    def incluir(self):
        return self.__operacao_lista[2]
    
    def is_alteracao(self, operacao):
        if operacao == self.alterar:
            return True
        else:
            return False
        
    def is_exclusao(self, operacao):
        if operacao == self.excluir:
            return True
        else:
            return False
                
    def is_inclusao(self, operacao):
        if operacao == self.incluir:
            return True
        else:
            return False        