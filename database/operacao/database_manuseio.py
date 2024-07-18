import functools
from datetime           import datetime, timedelta 
from sqlalchemy         import func
from operator           import and_, or_
from models             import Session
from database.operacao.datatabase_operacao import DatabaseOperacao

# Classe reponsável pelo acesso ao banco de dados
class DatabaseManuseio():

    def __init__(self):
        
        # Cria objeto da classe de identificação do tipo de operação no banco de dados
        self.__dboperacao = DatabaseOperacao()
        
        # Cria conexão com a base de dados no construtor da classe
        self.__session  = Session()    

    def __del__(self):
        # Conexão encerrada no destrutor da classe
        if self.__session:
            self.__session.close()
    
    # Propriedades e funções de identificação do tipo de operação no banco de dados
    @property
    def operacao_alterar(self):
        return self.__dboperacao.alterar

    @property
    def operacao_excluir(self):
        return self.__dboperacao.excluir

    @property
    def operacao_incluir(self):
        return self.__dboperacao.incluir
    
    @property
    def is_operacao_alteacao(self, operacao):
        return self.__dboperacao.is_alteracao(operacao)
    
    @property
    def is_operacao_exclusao(self, operacao):
        return self.__dboperacao.is_exclusao(operacao)
    
    @property
    def is_operacao_inclusao(self, operacao):
        return self.__dboperacao.is_inclusao(operacao)
    
    # Propiedade de acesso ao objeto Session
    @property
    def session(self):
        return self.__session
    
    # Função para formatar datas no Filter
    def get_formata_data_filter(self, datafilter:datetime  ):
        return datafilter.strftime("%Y-%m-%d") 
    
    def get_formata_data_hora_filter(self, datafilter:datetime  ):
        return datafilter.strftime('%Y-%m-%d %H:%M:%S') 
    
    # Função de retorno do objeto da seleção de todos os registros de uma tabela
    def get_select_all(self, tabela, filtro):
        if filtro is not None: 
            return  self.__session.query(tabela).filter(filtro).all()
        else: 
            return  self.__session.query(tabela).all()
        
    # Função de retorno seleção da primeira linha de uma tabaela conforme filtro
    def get_select_first(self, tabela, filtro):
        return self.__session.query(tabela).filter(filtro).first()
    
    # Função de retorno count numérico de uma tabela
    def get_select_count_number(self, tabelacoluna, filtro):
        
        resultcount = 0
        
        if filtro is not None: 
            resultcount = self.__session.query(tabelacoluna).filter(filtro).count()
        else: 
            resultcount = self.__session.query(tabelacoluna).count()
            
        return resultcount

    # Função de retorno maior valor numérico de uma tabela
    def get_select_max_value(self, tabelacoluna, filtro):
        
        retresultmaxcoluna = None
        retresultmaxquery  = None
        
        if filtro is not None: 
            retresultmaxquery = self.__session.query(func.max(tabelacoluna)).filter(filtro)
        else:         
            retresultmaxquery = self.__session.query(func.max(tabelacoluna))
        
        # visuzaliza resultado
        for recordquery in retresultmaxquery: 
            retresultmaxquery = recordquery
            for recordcoluna in retresultmaxquery: 
                retresultmaxcoluna = recordcoluna

        return retresultmaxcoluna
    
    # Método para adcionar registro em uma tabela na base de dados
    def add_tabela(self, tabela, autocommit=True):
        
        try:
            self.__session.add(tabela)
        except:
            if autocommit == True:
                self.rollback_sessao()
                raise
        else:
            if autocommit == True:
                self.commit_sessao()        

    # Função para editar registros de uma tabela da base de dados 
    def update_tabela(self, tabela, filtro, values, autocommit=True):
    
        try:
            self.__session.query(tabela).filter(filtro).update(values, synchronize_session =False)
        except:
            if autocommit == True:
                self.rollback_sessao()
                raise
        else:
            if autocommit == True:
                self.commit_sessao()        
            
    # Função para remover linha(s) de uma tabela da base de dados conforme único indice de uma tabela
    def del_tabela(self, tabela, filtro, autocommit=True):
    
        try:
            count = self.__session.query(tabela).filter(filtro).delete()
        except:
            if autocommit == True:
                self.rollback_sessao()
                raise
        else:
            if autocommit == True:
                self.commit_sessao()        
            
        # Retorna contador de linhas atingidas
        return count
    
    # Métodos para realização commit e roolback
    def commit_sessao(self):
        if self.__session:
            self.__session.commit()
    
    def rollback_sessao(self):
        if self.__session:
            self.__session.rollback()    