import random

class passive:
    #name:パッシブ名,times:鳴く回数(最大),p:条件を満たしたときに鳴く確率,request:バフ条件(function)
    #situation:盤面条件dict{"status","support_df","buff_list","score_df","judge_dict","rival_list"}
    #buffs:鳴くバフ キュンコメ[["Vi",120],["Da",80],["Vo",80]]みたいに2次元配列を渡す
    def __init__(self,name='',type='',short_name='',times=0,p=0,request=None,buffs=[],args=None):
        self._name = name
        self._type=type
        self._short_name=short_name
        self._times = times
        self._p = p
        self._request = request
        self._buffs = buffs
        self._args = args

    def is_passive_active(self,situation):
        Pup = 0
        for buff in situation.buff_list:
            if buff["color"] == "PASSIVEpr":
                Pup += buff["buff"]
        if self._request(situation,self._args) and random.random()<((self._p + Pup)/100):
            return True
        else:return False
    
    def get_dict(self):
        return       {
            'card_name':self._name,
            'type':self._type,
            'times':self._times,
            'p':self._p,
            'buff':self._buffs,
            'request':condition_func_dict[self._request],
            'args':self._args,
            'text':self.get_text(),
            'icon':self._short_name
        }
        
    def set_from_json(self,in_dict):
        self._name = in_dict['card_name']
        self._type = in_dict['type']
        self._short_name=in_dict['icon']
        self._times = in_dict['times']
        self._p = in_dict['p']
        self._request = condition_name_dict[in_dict['request']]
        self._buffs = in_dict['buff']
        self._args = in_dict['args']
        
        
    def get_text(self):
        txt = self._name +self._type+ '\n'
        for buff in self._buffs:
            txt += buff_icon_dict[buff[0]]
            txt += str(buff[1])
            txt += "%UP/"
        txt += '\n'
        txt += f'[条件:{get_condition_name(self._request,self._args)}]'
        txt += f'[確率:{self._p}%]'
        txt += f'[最大:{self._times}回]'
        return txt
    
    def push2DB(self,FlaskSession):
        from Entity import Support,ProduceCard,Passive,PassiveRate
        import DataHandler as DH
        action = ""
        existing_record = DH.session.query(Passive).filter_by(cardname=self._name,passive_type=self._type).first()
        if len(FlaskSession) == 0:
            return "ログインしてください"
        if not existing_record:
            action ='create'
        else:
            if FlaskSession.get("oath_lv", 0) > 4:
                action = 'update'
            else:
                return "既に登録されています。内容が間違っている場合は管理人までお知らせください。"
        
        if action == 'create':
            entity = Passive()
        elif action == 'update':
            entity = existing_record
            
        entity.cardname = self._name
        entity.passive_type = self._type
        entity.short_name = self._short_name
        entity.times = self._times
        entity.rate = self._p
        if type(self._request) == str:
            entity.request = self._request
        else:
            entity.request = condition_func_dict[self._request]
        entity.args = str(self._args)
        entity.created_by= FlaskSession['username']
        
        for buff in self._buffs:
            RateEntity = PassiveRate(
                color=buff[0],
                rate=buff[1],
                created_by = FlaskSession['username']
            )
            entity.passiverate_relations.append(RateEntity)
        entity.support = DH.session.query(Support).filter_by(name=entity.cardname).first()
        entity.produce_card = DH.session.query(ProduceCard).filter_by(card_name=entity.cardname).first()
        if action == 'create':
            DH.session.add(entity)
        DH.session.commit()  # トランザクションをコミット
        return "登録完了"
    
def get_condition_name(func,val):
  if func == no_requirement:
        return '無条件'
  elif func == three_color_requirement:
        return 'VoDaViUPすべてが付与されている場合'
  elif func == buff_requirement:
        return f'{buff_icon_dict[val[0]]}UPが付与されている場合'
  elif func == after_turn_requirement:
        return f'{val[0]}ターン以降'
  elif func == before_turn_requirement:
        return f'{val[0]}ターン以前'
  elif func == history_requirement:
        return '履歴に'+",".join(val[0])+'がある場合'
  elif func == possibility_requirement:
    return f'{val[0]}の確率で発動'


#無条件バフ
def no_requirement(situation,val):                
  return True

#3色バフ条件
def three_color_requirement(situation,val):
  buff_list = situation.buff_list
  color_list =[]
  for buff in buff_list:
    color_list.append(buff["color"])
  return {"Vo","Da","Vi"} <= set(color_list)

#1色バフ条件
def buff_requirement(situation,val):
  buff_list = situation.buff_list
  flg = False
  for buff in buff_list:
    if val == buff["color"]:
      flg = True
  return flg

#TESTOK
#ターン以降条件
def after_turn_requirement(situation,val):
    return situation.turn >= int(val[0])

#TESTOK
#ターン以前条件
def before_turn_requirement(situation,val):

    return situation.turn <= int(val[0])

#確率近似条件
def possibility_requirement(situation,val):
    r = random.random()
    turn_num = situation.turn
    return r < val[0][turn_num]

#TESTOK
#履歴条件
def history_requirement(situation,val):
    if type(val[0]) == str:
        val[0] = val[0].split(',')
    return set(val[0]) <= set(situation.skill_history)

condition_name_dict = {
    '無条件':no_requirement,
    '3色バフ条件':three_color_requirement,
    '(属性)UPが付与されている場合':buff_requirement,
    '(N)ターン以前':before_turn_requirement,
    '(N)ターン以後':after_turn_requirement,
    '履歴に(アイドル)がある場合':history_requirement,
    'それ以外':possibility_requirement
}

def get_request_fanc(txt):
    return condition_name_dict[txt]

condition_func_dict = {k:v for v,k in condition_name_dict.items()}

buff_icon_dict ={
    'Vo':'Vocal',
    'Da':'Dance',
    'Vi':'Visual',
    'At':'注目度',
    'Av':'回避率',
    'Pa':'パッシブ発動率アップ'
}

all_passive_dict = {"花風Smiley金1":passive("花風金1",3,30,no_requirement,[["Da",75]]),
            "花風Smiley白":passive("花風白1",3,30,three_color_requirement,[["Vo",50],["Da",50],["Vi",50]]),
            "花風Smiley金2":passive("花風金2",3,30,three_color_requirement,[["Vo",100],["Da",100],["Vi",100]]),
            "水面を仰いで海の底金":passive("海金",3,10,after_turn_requirement,[["Da",60],["Vi",30]],3),
            "水面を仰いで海の底白":passive("海白1",3,10,no_requirement,[["Da",40],["Vi",20]]),
            "反撃の狼煙をあげよ！金":passive("狼煙金",3,20,after_turn_requirement,[["Vo",50],["Da",50],["Vi",50]],3),
            "反撃の狼煙をあげよ！白":passive("狼煙白",3,20,before_turn_requirement,[["Vo",30],["Da",30],["Vi",30]],3),
            "駅線上の日常金":passive("駅金",3,10,after_turn_requirement,[["Da",65],["Vi",65]],3),
            "駅線上の日常白":passive("駅白",3,10,before_turn_requirement,[["Da",30],["Vi",30]],6),
            "kimagure全力ビート！金":passive("バンド金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "kimagure全力ビート！白":passive("バンド白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "スプリング・フィッシュ金":passive("釣り金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "スプリング・フィッシュ白":passive("釣り白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "祝唄-hogiuta-金":passive("ホギウタ金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "祝唄-hogiuta-白":passive("ホギウタ白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "ワン・デー金":passive("ワンデー金",2,20,before_turn_requirement,[["Vo",30],["Da",50],["Vi",30]],3),
            "ワン・デー白":passive("ワンデー白",1,5,no_requirement,[["Da",15]]),
            "チョコレー党白":passive("チョコレー党白",2,20,before_turn_requirement,[["Da",50]],3),
            "チョコレー党金":passive("チョコレー党白",2,20,before_turn_requirement,[["Da",80]],3),
            "ピトス・エルピス白":passive("ピトス白",2,35,before_turn_requirement,[["Vi",30],["Av",30]],2),
            "LATE白":passive("LATE白",1,20,before_turn_requirement,[["Vi",50]],3),
            "LATE金1":passive("LATE金1",1,20,no_requirement,[["Vi",120]]),
            "LATE金2":passive("LATE金2",2,20,possibility_requirement,[["Vi",100]],[0,0,10/32,58/512,0,0]),
            "ちょー早い金":passive("ちょー早い金",3,30,no_requirement,[["Vi",60]]),
            "ちょー早い白":passive("ちょー早い金",2,20,no_requirement,[["Vi",50]]),
            "シャッターチャンス金":passive("シャッター金",3,30,buff_requirement,[["Vo",75]],"Vo"),
            "永遠の方程式金":passive("方程式金",1,30,possibility_requirement,[["Vo",80],["Da",80],["Vi",80]],[0,0.7,1,1,0]),
            "きゅんコメ金":passive("きゅんコメ",3,40,history_requirement,[["Vi",75]],["櫻木真乃","風野灯織"])
            }