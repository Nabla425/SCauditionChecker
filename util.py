from transfer_class.Rival import rival
from transfer_class.Settings import settings
import json

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