class weapon:
    name:str
    type:str
    
    def __init__(self,name:str,type:str) -> None:
        self.name = name
        self.type = type
        
    def get_key(self):
        return self.name+self.type
    
    def get_ATK(self)->dict:
        return {'Vo':0,'Da':0,'Vi':0}
    