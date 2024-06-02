import json
from transfer_class import Judge

class situation:
    hand_weapon:list
    buff_list:list #今鳴いているバフ
    passive_list:list #各パッシブが泣いているかどうかと残り鳴き数をまとめたリスト
    skill_history:list #今まで打った札(アイドル)の履歴
    judge_dict:dict
    Pstatus:dict
    turn:int
    log:list
    # score_dict:dict
    
    def __init__(self,judge_dict={},status={},passive_list=[]):
        self.hand_weapon = []
        self.buff_list = []
        self.passive_list = []
        self.skill_history = []
        self.judge_dict = judge_dict
        self.Pstatus = status
        self.turn = 1;
        self.passive_list = []
        self.log = ['']
        for passive in passive_list:
            self.passive_list.append({'name':passive._name,'rest':passive._times,'isActieve':False,'text':passive.get_text(),'short_name':passive._short_name})
        
    def get_dict(self):
        ret_dict = self.__dict__
        ret_dict['judge_dict'] = {k:v.info for (k,v) in self.judge_dict.items()}
        # ret_dict['hand_weapon'] =self.hand_weapon
        # ret_dict['buff_list'] = self.buff_list
        # ret_dict['skill_history'] = self.skill_history
        # ret_dict['Pstatus'] = self.Pstatus
        # ret_dict['turn'] = self.turn
        return ret_dict
    
    def set_from_json(self,in_dict):
        self.hand_weapon = in_dict['hand_weapon']
        self.buff_list = in_dict['buff_list']
        self.passive_list = in_dict['passive_list']
        self.skill_history = in_dict['skill_history']
        self.Pstatus = in_dict['Pstatus']
        self.log = in_dict['log']
        self.turn = in_dict['turn']
        for col in ['Vo','Da','Vi']:
            self.judge_dict[col] = Judge.judge(in_dict['judge_dict'][col])
        
    def passive_process(self,settings):
        isActiveList = [p.is_passive_active(self) for p in settings.aquired_passive]
        for passive_dict,isActive in zip(self.passive_list,isActiveList):
            if passive_dict['rest']>0 and isActive:
                passive_dict['rest'] -= 1
                passive_dict['isActive'] = True
            else: passive_dict['isActive'] = False
    
    #buff_listの中の各バフを集計する 倍率(30%→1.3)として返す  ↓Sasmple
    # [{"color":'Vo',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
    # {"color":'Da',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},]
    def get_buff(self)->dict:
        buff_dict = {"Vo":0,"Da":0,"Vi":0}
        for buff in self.buff_list:
            if buff['color'] not in buff_dict.keys():
                buff_dict[buff['color']] = buff['buff']
            else:
                buff_dict[buff['color']] += buff['buff']
        return buff_dict
    
    def get_passive(self,aquired_passive):
        ret_dict ={'Vo':0,'Da':0,'Vi':0}
        for p_situ,passive_info in zip(self.passive_list,aquired_passive):
            if p_situ['isActive']:
                for col,rate in passive_info._buffs:
                    if col not in ret_dict.keys():
                        ret_dict[col] = rate
                    else:ret_dict[col] += rate
        return ret_dict
    
    def get_judge_alive_dict(self):
        ret = {}
        for col,judge in self.judge_dict.items():
            ret[col] = (judge.info['HP']>0)
        return ret
    
    
        