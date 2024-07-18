from datetime import datetime

import re

class Util: 
    def __init__(self) -> None:
        pass

    # Função de validação string nula ou sem valor
    @staticmethod
    def get_str_nulo_sem_valor(strvalor:str):
    
        valorok       =  False

        if not strvalor:
            valorok = True
        elif strvalor.strip() == "":
            valorok = True

        return valorok            

    # Função de validação de e-mails
    @staticmethod
    def get_email_valido(email:str):
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_regex, email):
            return True
        else:
            return False
    
    # Função de validação string nula ou sem valor e tamanho de string válida
    @staticmethod
    def get_str_tamanho_valido(strvalor:str, minimovalor:int, maximovalor:int):
    
        tamanhovalido       =  False
        
        if not Util.get_str_nulo_sem_valor(strvalor):
            if len(strvalor) >= minimovalor and len(strvalor) <= maximovalor:
                tamanhovalido = True

        return tamanhovalido            

    # Função de retorno conversão string data para data no formato (YYYY-MM-DD)
    @staticmethod
    def get_converte_str_data_fmt_yyyy_mm_dd(strdata:str):
    
        return datetime.strptime(strdata,"%Y-%m-%d") 
