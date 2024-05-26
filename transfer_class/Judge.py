class judge:
    info:dict
    '''
    color:str 
    HP:int
    Max_HP:int
    ATK:int
    DEF:float 
    buff:list 
    '''
    def __init__(self,info):
        self.info=info
        if 'score' not in self.info.keys():
            self.info['score'] = {
                'appeal':{'My':0,'A':0,'B':0,'C':0,'D':0,'E':0},
                'three_star':'',
                'six_star':'',
                'LA':'',
                'TA':''
            }