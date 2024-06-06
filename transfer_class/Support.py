from transfer_class import Settings,Situation
class support() :
    info:dict
    '''
    init_dict={
        'card_type':'S'
        'key':'櫻木真乃駅線上の日常4凸',
        'idol_name':'櫻木真乃',
        'card_name':'駅線上の日常',
        'totu':'4凸',
        'status':{'Vo':0,'Da':0,'Vi':0},
        'appeal':{'Vo':0,'Da':0,'Vi':0,'Ex':0}
        'buff':[ {"color":'Da',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},
                 {"color":'Vi',"buff":30,"turn":3,"name":"水面仰いで海の底","fanc":None},]
    }
    '''
    def __init__(self,info_dict):
        self.info = info_dict
                    
    def get_appeal_str(self):
        l = ''
        for col,rate in self.info['appeal'].items():
            if rate > 0:
                l += (col+str(rate)+'倍')
        l += 'アピール'
        return l
    
    def getATK(self,settings:Settings.settings,situation:Situation.situation,input)->dict:
        color_list = ['Vo','Da','Vi','Ex']
        aim = input['aim']
        critical = float(input['critical'])
        ATK_dict = {}
        buff_dict = situation.get_buff()
        passive_dict = situation.get_passive(settings.aquired_passive)
        for col in color_list:
            color = aim if col == 'Ex' else col 
            # サポステの合計
            S_status = settings.sumSstatus(color)
            #アピール倍率
            weapon_rate = self.info['appeal'][col]
            buff = 1 + (buff_dict[color]+passive_dict[color])/100
            iS = self.info['status'][color]
            iP = situation.Pstatus[color]
            ATK =int(int(int(iP*0.5 + (S_status + 3*iS) * (1 + 0.1*settings.week) * 0.2)*buff*critical) * weapon_rate)
            ATK_dict[col]=ATK
        put_buff = self.info['buff']
        return ATK_dict,put_buff
    
    def push2DB(self):
        import Entity
        import DataHandler as DH
        entity = Entity.Support()
        entity.name = self.info['card_name']
        entity.idol = self.info['idol_name']
        entity.totu = int(self.info['totu'][0])
        entity.Vo = self.info['status']['Vo']
        entity.Da = self.info['status']['Da']
        entity.Vi = self.info['status']['Vi']
        entity.Vo_rate = self.info['appeal']['Vo']
        entity.Da_rate = self.info['appeal']['Da']
        entity.Vi_rate = self.info['appeal']['Vi']
        for buff in self.info['buff']:
            print(buff)
            buffEntity = Entity.Buff(
                color=buff['color'],
                rate=buff['buff'],
                turn=buff['turn'],
                val=str(buff['val']),
            )
            entity.buff_relations.append(buffEntity)
        DH.push2DB(entity)
            

        
                    

            