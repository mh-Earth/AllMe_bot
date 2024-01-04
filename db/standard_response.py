

class StandardResponse:

    def __init__(self,code:int,text:str,**kwargs) -> None:
        self.code = code 
        self.text = text
        self.kwargs = kwargs
    
    def __repr__(self) -> str:
        return f"<[Response code={self.code}, {self.kwargs}]>"
    def __bool__(self):
        return True if self.code == 200 else False
    
    @staticmethod
    def success(text='success',**kwargs):
        return StandardResponse(200,text,**kwargs)
    
    @staticmethod
    def duplication_error(text,**kwargs):
        return StandardResponse(500,text,**kwargs)
    
    @staticmethod
    def standard_error(text,**kwargs):
        return StandardResponse(500,text,**kwargs)
    
    @staticmethod
    def limit_reached(text,**kwargs):
        return StandardResponse(403,text,**kwargs)
    @staticmethod
    def null_error(text,**kwargs):
        return StandardResponse(404,text,**kwargs)
    @staticmethod
    def standard_info(text,**kwargs):
        return StandardResponse(200,text,**kwargs)
