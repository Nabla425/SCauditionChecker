class situation:
    hand_weapon:list
    buff_list:list #今鳴いているバフ
    passive_list:list #今鳴いているパッシブ
    skill_history:list #今まで打った札(アイドル)の履歴
    weapon_hist:list#今まで打った札名の履歴
    LA_dict:dict #誰がLAをとったかの情報
    judge_dict:dict
    Pstatus:dict
    turn:int
    
    def __init__(self,judge_dict,status):
        self.hand_weapon = []
        self.buff_list = []
        self.passive_list = []
        self.skill_history = []
        self.weapon_hist = []
        self.LA_dict = {}
        self.judge_dict = judge_dict
        self.Pstatus = status
        self.turn = 1;
        
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
    
    
        