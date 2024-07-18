from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Define como a mensagem de erro será representada
    """
    mesage: str
    
class ReturnErrorMesage:
    def __init__(self, mesage, error_msg):
        self.__mesage  = mesage
        self.__error_msg = error_msg
        
    @property
    def mesage(self):
        return self.__mesage
    
    @property
    def error_msg(self):
        return self.__error_msg
    
