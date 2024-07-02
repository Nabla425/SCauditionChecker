import json,random
from transfer_class import Rival,Support,P_weapon,Memory,Passive

class settings:
    support_list:list
    pweapon_list:list
    audition_name:str
    rival_list:list
    produce_idol:str
    produce_card:StopIteration
    memory_appeal:Memory.memory
    aquired_passive:list
    week:int
    trend:dict
    #{'Vo':1,'Da':2,'Vi':3}
    
    def __init__(
            self,support_list=[],pweapon_list=[],audition_name='',
            week=0,trend={},rival_list=[],idol='櫻木真乃',produce_card='',memory=Memory.memory(),aquired_passive=[]):
        self.support_list = support_list
        self.pweapon_list = pweapon_list
        self.audition_name = audition_name
        self.week = week
        self.trend = trend
        self.rival_list=rival_list
        self.produce_idol = idol
        self.produce_card = produce_card
        self.memory_appeal = memory
        self.aquired_passive = aquired_passive
        self.set_rival_mem_turn()
        self.set_rival_critical(1)
        self.set_rival_aim(self.trend,1,{'Vo':True,'Da':True,'Vi':True})
            
    def get_dict(self):
        ret_dict = {}
        ret_dict['support_list'] = [s.info for s in self.support_list]
        ret_dict['pweapon_list'] = [p.info for p in self.pweapon_list]
        ret_dict['rival_list'] = [r.info for r in self.rival_list]
        ret_dict['audition_name'] = self.audition_name
        ret_dict['memory'] = self.memory_appeal.info
        ret_dict['produce_idol'] = self.produce_idol
        ret_dict['produce_card'] = self.produce_card
        ret_dict['aquired_passive'] = [passive.get_dict() for passive in self.aquired_passive]
        ret_dict['week'] = self.week
        ret_dict['trend']= self.trend
        return ret_dict
        
    def set_from_json(self,in_dict):
        self.support_list = [Support.support(s) for s in in_dict['support_list']]
        self.pweapon_list = [P_weapon.pweapon(p) for p in in_dict['pweapon_list']]
        self.rival_list = [Rival.rival(r) for r in in_dict['rival_list']]
        self.aquired_passive = []
        for passive_info in in_dict['aquired_passive']:
            passive = Passive.passive()
            passive.set_from_json(passive_info)
            self.aquired_passive += [passive]
        self.produce_idol = in_dict['produce_idol']
        self.produce_card = in_dict['produce_card']
        memory = Memory.memory()
        memory.info = in_dict['memory']
        self.memory_appeal = memory
        self.audition_name = in_dict['audition_name']
        self.week = in_dict['week']
        self.trend = in_dict['trend']
            

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
            
    def set_rival_aim(self,trend,turn,judge_alive_dict):
        for rival in self.rival_list:
            rival.set_aim(trend,turn,judge_alive_dict)
