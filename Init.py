import sqlite3
from transfer_class import Rival,Judge,Support,P_weapon
import json

def init_audition(audition_name):
    db_name = "datas/data.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    rival_list = []
    judge_dict = {}
    sql = "SELECT 興味値,メンタルダメージ FROM audition WHERE オーディション名 = %s" % audition_name
    c.execute(sql)
    fetch = list(c.fetchone())
    for col in ["Vo","Da","Vi"]:
        info_dict = {}
        info_dict['color']=col
        info_dict['HP']=fetch[0]
        info_dict['Max_HP']=fetch[0]
        info_dict['ATK']=fetch[1]
        info_dict['DEF']=1
        info_dict['buff']=[]
        judge_dict[col]=Judge.judge(info_dict)
    for name in ['A','B','C','D','E']:
        sql = "SELECT 興味値,基礎攻撃力,思い出火力,%s属性,%s変遷種,%s変遷順 FROM audition WHERE オーディション名 = %s" % (name,name,name,audition_name)
        c.execute(sql)
        fetch = list(c.fetchone())
        info_dict = {}
        info_dict['name']=name
        info_dict['HP']=fetch[0]
        info_dict['baseATK']=fetch[1]
        info_dict['memATK']=fetch[2]
        info_dict['color']=fetch[3]
        info_dict['choice_type']=fetch[4]
        info_dict['choice_order']=[int(od) for od in fetch[5].split(',')]
        info_dict['star']=0
        info_dict['critical'] = ''
        info_dict['aim'] = ''
        info_dict['mem_turn'] = 0
        
        r = Rival.rival(info_dict)
        rival_list.append(r)
    return rival_list,judge_dict

def set_support(key):
    # key="櫻木真乃駅線上の日常0凸"としてSupport型を準備して返す
    db_name = "datas/support.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "SELECT * FROM support WHERE 検索キー = %s" % key
    c.execute(sql)
    fetch = list(list(c.fetchone()))
    info_dict ={'card_type':'S'}
    info_dict['key']=fetch[1]
    info_dict['idol_name']=fetch[2]
    info_dict['card_name']=fetch[3]
    info_dict['totu']=fetch[4]
    info_dict['status']={'Vo':(int)(fetch[5]),'Da':(int)(fetch[6]),'Vi':(int)(fetch[7])}
    info_dict['appeal']={'Vo':(float)(fetch[8]),'Da':(float)(fetch[9]),'Vi':(float)(fetch[10]),'Ex':(float)(fetch[11])}
    buff = {
        'Vo_buff':fetch[12].split(','),
        'Da_buff':fetch[13].split(','),
        'Vi_buff':fetch[14].split(','),
        'Vo_buff_coT':fetch[15].split(','),
        'Vo_buff_coT':fetch[16].split(','),
        'Da_buff_coT':fetch[16].split(','),
        'Vi_buff_coT':fetch[17].split(','),
        'size':len(fetch[12].split(','))
    }
    info_dict['buff']=[]
    for i in range(buff['size']):
        for color in ['Vo','Da','Vi']:
            if int(buff['%s_buff'%color][i])>0:
                ret = {'color':color,
                        'buff':int(buff['%s_buff'%color][i]),
                        'turn':int(buff['%s_buff_coT'%color][i]),
                        'name':fetch[3]+'(S)',
                        'fanc':None
                        }
                info_dict['buff'].append(ret)
    #(4, '櫻木真乃駅線上の日常4凸', '櫻木真乃', '駅線上の日常', '4凸', '150', '225', '225', '0', '2', '2', '0', '0', '0', '0', '0', '0', '0')
    info_dict['ATKtype']='single'
    s = Support.support(info_dict)
    return s

def set_pweapon():
    pweapon_list = []
    #花風4凸
    info = {
        'idol':'櫻木真乃',
        'card_name':'花風smiley+',
        'card_type':'P',
        'ATKtype':'whole',
        'weapon_rate':{'Vo':1.0,'Da':4.0,'Vi':1.0,'Ex':0.0},
        'buff':[
            {"color":'Vo',"buff":30,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Da',"buff":30,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Vi',"buff":30,"turn":3,"name":"花風smiley+","fanc":None}
        ],
        'link':['ATK',{'Vo':1.0,'Da':1.0,'Vi':1.0}]
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol':'櫻木真乃',
        'card_name':'花風smiley',
        'card_type':'P',
        'ATKtype':'whole',
        'weapon_rate':{'Vo':0.5,'Da':2.5,'Vi':0.5,'Ex':0.0},
        'buff':[
            {"color":'Vo',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Da',"buff":10,"turn":3,"name":"花風smiley+","fanc":None},
            {"color":'Vi',"buff":10,"turn":3,"name":"花風smiley+","fanc":None}
        ],
        'link':['ATK',{'Vo':1.0,'Da':1.0,'Vi':1.0}]
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol':'櫻木真乃',
        'card_name':'水面仰いで海の底',
        'card_type':'P',
        'ATKtype':'single',
        'weapon_rate':{'Vo':0,'Da':3.0,'Vi':1.5,'Ex':0.0},
        'buff':[
            {"color":'Da',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},
            {"color":'Vi',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},
        ],
        'link':[None]
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    info = {
        'idol':'櫻木真乃',
        'card_name':'駅線上の日常',
        'card_type':'P',
        'ATKtype':'single',    
        'weapon_rate':{'Vo':0,'Da':2.0,'Vi':2.0,'Ex':0.0},
        'buff':[
            {"color":'Da',"buff":20,"turn":3,"name":"駅線上の日常","fanc":None},
            {"color":'Vi',"buff":20,"turn":3,"name":"駅線上の日常","fanc":None},
        ],
        'link':[None]
    }
    p = P_weapon.pweapon(info)
    pweapon_list.append(p)
    return pweapon_list