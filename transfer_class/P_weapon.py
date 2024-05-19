import sqlite3
from transfer_class import Settings,Situation
class pweapon():
    info:dict
    '''
    info_dict = {
        'idol':'櫻木真乃',
        'card_name':'花風smiley+'
        'card_type':'P'
        'ATKtype' = 'single'or 'whole'
        weapon_rate = {'Vo':x,'Da':x,'Vi':x}
        buff = [{"color":color,"buff":10,"turn":3,"name":"櫻木真乃花風smiley0凸","fanc":None}
                ]
        link = ['ATK',{'Vo':x,'Da':x,'Vi':x}](追撃)
        link = ['buff',[{"color":color,"buff":10,"turn":3,"name":"櫻木真乃花風smiley0凸","fanc":None}
                ]]}
    '''
    def __init__(self,info):
        self.info=info
        
    def get_appeal_str(self):
            l = ''
            for col in ['Vo','Da','Vi']:
                rate=self.info['weapon_rate'][col]
                if rate>0:
                    l += (col+str(rate)+'倍')
            l+='アピール'
            return l
        
    def getATK(self,settings:Settings.settings,situation:Situation.situation,input)->dict:
        color_list = ['Vo','Da','Vi','Ex']
        aim = input['aim']
        critical = float(input['critical'])
        ATK_dict = {}
        for col in color_list:
            color = aim if col == 'Ex' else col 
            buff = 1
            # サポステの合計
            S_status = settings.sumSstatus(color)
            #アピール倍率
            weapon_rate = self.info['weapon_rate'][col]
            iP = situation.Pstatus[color]
            ATK =int(int(int(iP*2 + S_status*0.2*(1+0.1*settings.week))*buff*critical) * weapon_rate)
            ATK_dict[col]=ATK
        return ATK_dict
        
    def push_DB(self):
        c = sqlite3.connect('datas/data.db')
        cur = c.cursor()
        sql_list = []
        sql_list.append(self.idol)
        sql_list.append(self.info['type'])
        sql_list.append(self.info['weapon_rate']['Vo'])
        sql_list.append(self.info['weapon_rate']['Da'])
        sql_list.append(self.info['weapon_rate']['Vi'])
        sql_list.append()
        
        c.commit()
        c.close()