from transfer_class import Rival,Judge,Support,P_weapon
import pandas as pd

init_support_list = [
{'card_type': 'S', 'key': '櫻木真乃駅線上の日常4凸', 'idol_name': '櫻木真乃', 'card_name': '駅線上の日常', 'totu': '4凸', 'status': {'Vo': 150, 'Da': 225, 'Vi': 225}, 'appeal': {'Vo': 0.0, 'Da': 2.0, 'Vi': 2.0, 'Ex': 0.0}, 'buff': [], 'ATKtype': 'single'},
{'card_type': 'S', 'key': '風野灯織水面を仰いで海の底4凸', 'idol_name': '風野灯織', 'card_name': '水面を仰いで海の底', 'totu': '4凸', 'status': {'Vo': 150, 'Da': 225, 'Vi': 225}, 'appeal': {'Vo': 0.0, 'Da': 3.0, 'Vi': 0.0, 'Ex': 0.0}, 'buff': [{'color': 'Da', 'buff': 25, 'turn': 3, 'name': '水面を仰いで海の底(S)', 'val': None}, {'color': 'Vi', 'buff': 25, 'turn': 3, 'name': '水面を仰いで海の底(S)', 'val': None}], 'ATKtype': 'single'},
{'card_type': 'S', 'key': '小宮果穂反撃の狼煙をあげよ！4凸', 'idol_name': '小宮果穂', 'card_name': '反撃の狼煙をあげよ！', 'totu': '4凸', 'status': {'Vo': 218, 'Da': 218, 'Vi': 218}, 'appeal': {'Vo': 0.0, 'Da': 0.0, 'Vi': 0.0, 'Ex': 3.5}, 'buff': [], 'ATKtype': 'single'},
{'card_type': 'S', 'key': '園田智代子kimagure全力ビート！4凸', 'idol_name': '園田智代子', 'card_name': 'kimagure全力ビート！', 'totu': '4凸', 'status': {'Vo': 218, 'Da': 218, 'Vi': 218}, 'appeal': {'Vo': 0.0, 'Da': 0.0, 'Vi': 0.0, 'Ex': 3.5}, 'buff': [], 'ATKtype': 'single'}
]

def init_audition(audition_name):
    df = pd.read_csv('datas/Audition.csv',encoding='shift-jis',index_col=0).T
    rival_list = []
    judge_dict = {}
    info = df[audition_name]
    for col in ["Vo","Da","Vi"]:
        info_dict = {}
        info_dict['color']=col
        info_dict['HP']=info['興味値']
        info_dict['Max_HP']=info['興味値']
        info_dict['ATK']=info['メンタルダメージ']
        info_dict['DEF']=1
        info_dict['buff']=[]
        judge_dict[col]=Judge.judge(info_dict)
    for name in ['A','B','C','D','E']:
        if info[f'{name}属性']!='NONE':
            info_dict = {}
            info_dict['name']=name
            info_dict['HP']=500
            info_dict['baseATK']=info['基礎攻撃力']
            info_dict['memATK']=info['思い出火力']
            info_dict['color']=info[f'{name}属性']
            info_dict['choice_type']=info[f'{name}変遷種']
            info_dict['choice_order']=[int(od) for od in info[f'{name}変遷順'].split(',')]
            info_dict['star']=0
            info_dict['critical'] = ''
            info_dict['aim'] = ''
            info_dict['mem_turn'] = 0
            r = Rival.rival(info_dict)
            rival_list.append(r)
    return rival_list,judge_dict

def set_support():
    support_list = []
    for info_dict in init_support_list:
        support_list.append(Support.support(info_dict))
    return support_list

def set_pweapon():
    pweapon_list = []
    #花風4凸
    info = {
        'idol_name':'八宮めぐる',
        'card_name':'花風smiley+',
        'card_type':'P',
        'ATKtype':'whole',
        'weapon_rate':{'Vo':1.0,'Da':4.0,'Vi':1.0,'Ex':0.0},
        'buff':[
            {"color":'Vo',"buff":30,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Da',"buff":30,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Vi',"buff":30,"turn":3,"name":"花風smiley+","fanc":None}
        ],
        'link_type':'ATK',
        'link_contents':{'Vo':1.0,'Da':1.0,'Vi':1.0},
        'isLink':False
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol_name':'八宮めぐる',
        'card_name':'花風smiley',
        'card_type':'P',
        'ATKtype':'whole',
        'weapon_rate':{'Vo':0.5,'Da':2.5,'Vi':0.5,'Ex':0.0},
        'buff':[
            {"color":'Vo',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Da',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Vi',"buff":10,"turn":3,"name":"花風smiley+","fanc":None}
        ],
        'link_type':'ATK',
        'link_contents':{'Vo':1.0,'Da':1.0,'Vi':1.0},
        'isLink':False
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol_name':'八宮めぐる',
        'card_name':'水面仰いで海の底',
        'card_type':'P',
        'ATKtype':'single',
        'weapon_rate':{'Vo':0,'Da':3.0,'Vi':1.5,'Ex':0.0},
        'buff':[
            {"color":'Da',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},
            {"color":'Vi',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},
        ],
        'link_type':"no_link",
        'link_contents':"no_link",
        'isLink':False
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol_name':'八宮めぐる',
        'card_name':'駅線上の日常',
        'card_type':'P',
        'ATKtype':'single',
        'weapon_rate':{'Vo':0,'Da':2.0,'Vi':2.0,'Ex':0.0},
        'buff':[
            {"color":'Da',"buff":20,"turn":3,"name":"駅線上の日常","fanc":None},
            {"color":'Vi',"buff":20,"turn":3,"name":"駅線上の日常","fanc":None},
        ],
        'link_type':"no_link",
        'link_contents':"no_link",
        'isLink':False
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    return pweapon_list