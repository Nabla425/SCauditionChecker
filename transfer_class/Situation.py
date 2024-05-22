import json
from transfer_class import Judge

class situation:
    hand_weapon:list
    buff_list:list #今鳴いているバフ
    passive_list:list #今鳴いているパッシブ
    skill_history:list #今まで打った札(アイドル)の履歴
    # weapon_hist:list#今まで打った札名の履歴
    # LA_dict:dict #誰がLAをとったかの情報
    judge_dict:dict
    Pstatus:dict
    turn:int
    
    def __init__(self,judge_dict={},status={}):
        self.hand_weapon = []
        self.buff_list = []
        self.passive_list = []
        self.skill_history = []
        # self.weapon_hist = []
        # self.LA_dict = {}
        self.judge_dict = judge_dict
        self.Pstatus = status
        self.turn = 1;
        
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
        # in_dict = json.loads(in_dict)
        self.hand_weapon = in_dict['hand_weapon']
        self.buff_list = in_dict['buff_list']
        self.passive_list = in_dict['passive_list']
        self.skill_history = in_dict['skill_history']
        # self.weapon_hist = in_dict['weapon_hist']
        self.skill_history = in_dict['skill_history']
        self.Pstatus = in_dict['Pstatus']
        self.turn = in_dict['turn']
        for col in ['Vo','Da','Vi']:
            self.judge_dict[col] = Judge.judge(in_dict['judge_dict'][col])
        
        
    
    #buff_listの中の各バフを集計する 倍率(30%→1.3)として返す  ↓Sasmple
    # [{"color":'Vo',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
    # {"color":'Da',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},]
    def get_buff(self)->dict:
        buff_dict = {'Vo':0,'Da':0,'Vi':0}
        for buff in self.buff_list:
            buff_dict[buff['color']] += buff['buff']
        for k,rate in buff_dict.items():
            rate = 1+rate/100
        return buff_dict
    
    def get_judge_alive_dict(self):
        ret = {}
        for col,judge in self.judge_dict.items():
            ret[col] = (judge.info['HP']>0)
        return ret
    
    
        