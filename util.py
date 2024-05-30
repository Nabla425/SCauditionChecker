from transfer_class.Rival import rival
from transfer_class.Settings import settings
import json

unit_dict = {"イルミネーションスターズ":["櫻木真乃","風野灯織","八宮めぐる"],
             "アンティーカ":["月岡恋鐘","田中摩美々","白瀬咲耶","三峰結華","幽谷霧子"],
             "放課後クライマックスガールズ":["小宮果穂","園田智代子","西城樹里","杜野凛世","有栖川夏葉"],
             "アルストロメリア":["大崎甘奈","大崎甜花","桑山千雪"],
             "ストレイライト":["芹沢あさひ","黛冬優子","和泉愛依"],
             "ノクチル":["浅倉透","樋口円香","市川雛菜","福丸小糸"],
             "シーズ":["七草にちか","緋田美琴"],
             "コメティック":["斑鳩ルカ","鈴木羽那","郁田はるき"]
             }

belongs_dict = {}
idol_list=[]
for unit,idols in unit_dict.items():
    for idol in idols:
        belongs_dict[idol] = unit
        idol_list.append(idol)


def chk_link(idol,skill_history):
    unit = set(unit_dict[belongs_dict[idol]])
    chk_link_list = set(skill_history + [idol])
    return chk_link_list >= unit

def test_rival_critical(rival,turn):
    result = {'p':0,'g':0,'n':0,'b':0,'m':0}
    itr = 10000
    for i in range(itr):
        rival.set_critical(turn)
        result[rival.info['critical']] += 1
        with open('datas/rival_move.json',mode="rt", encoding="utf-8") as f:
            rival_move = json.load(f)
    turn = '{0}T'.format(turn)
    for k,v in result.items():
        v = v/itr
    print('raval_critical_test')
    print(rival_move[rival.info['name']][turn])  
    print(result)
    
def test_rival_mem_turn(settings:settings):
    itr=100
    result = {'A':[0,0,0,0,0],
              'B':[0,0,0,0,0],
              'C':[0,0,0,0,0],
              'D':[0,0,0,0,0],
              'E':[0,0,0,0,0]
              }
    for i in range(itr):
        for rival in settings.rival_list:
            rival.info['mem_turn'] = 0
        settings.set_rival_mem_turn()
        for rival in settings.rival_list:
            result[rival.info['name']][rival.info['mem_turn']-1]+=1
    print(result)
    #%%