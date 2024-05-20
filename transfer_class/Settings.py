import json,random

class settings:
    support_list:list
    pweapon_list:list
    audition_name:str
    week:int
    trend:dict
    rival_list:list
    def __init__(
            self,support_list,pweapon_list,audition_name,
            week,trend,rival_list) -> None:
        self.support_list = support_list
        self.pweapon_list = pweapon_list
        self.audition_name = audition_name
        self.week = week
        self.trend = trend
        self.rival_list=rival_list
        self.set_rival_mem_turn()
        self.set_rival_critical(1)
        self.set_rival_aim(self.trend,1,{'Vo':True,'Da':True,'Vi':True})
            
    def sumSstatus(self,color):
        sum = 0
        for support in self.support_list:
            sum += support.info['status'][color]
        return sum
    
    def set_rival_critical(self,turn):
        with open('datas/rival_move.json',mode="rt", encoding="utf-8") as f:
            rival_move = json.load(f)
        for rival in self.rival_list:
            table = rival_move[rival.info['name']]
            if turn < 6:
                key = '{0}T'.format(turn)
                table = table[key]
                options = list(table.keys())
                weight = list(table.values())
                critical = random.choices(options, weights = weight)[0]
                rival.info['critical'] = critical
                if rival.info['mem_turn'] == turn:
                    rival.info['critical']='m'
            else:
                rival.info['critical'] = random.choices(['p','g','n','b'])
            
    def set_rival_mem_turn(self):
        with open('datas/rival_mem_turn.json') as f:
            table = json.load(f)
        for rival in self.rival_list:
            for i,rate in enumerate(table[rival.info['name']]):
                if rival.info['mem_turn'] == 0:
                    if random.random()<rate:
                        rival.info['mem_turn']=(i+1)
                        break
            # print(rival.info['name'],rival.info['mem_turn'])
            
    def set_rival_aim(self,trend,turn,judge_alive_dict):
        for rival in self.rival_list:
            rival.set_aim(trend,turn,judge_alive_dict)