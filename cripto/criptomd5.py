import hashlib

class CriptoMD5():

    def __init__(self, strvalor):
        self.__valor = strvalor
    
    # retorna valor criptografado
    def get_cripto_md5(self):
        criptovalue = hashlib.md5(self.__valor.encode())
        criptovalue = criptovalue.hexdigest()
        return criptovalue
        
        
        