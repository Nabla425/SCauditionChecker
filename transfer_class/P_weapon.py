import sqlite3
from transfer_class import Settings,Situation
class pweapon():
    info:dict
    '''
    info_dict = {
        'idol_name':'櫻木真乃',
        'card_name':'花風smiley+'
        'card_type':'P'
        'ATKtype' = 'single'or 'whole'
        weapon_rate = {'Vo':x,'Da':x,'Vi':x}
        buff = [{"color":color,"buff":10,"turn":3,"name":"櫻木真乃花風smiley0凸","fanc":None}
                ]
        link_type ='ATK'|'buff'|'no_link' 
        lnik_contents={'Vo':x,'Da':x,'Vi':x}|[{"color":color,"buff":10,"turn":3,"name":"櫻木真乃花風smiley0凸","fanc":None}]
        isLink=false
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
        
    def getATK(self,settings,situation,input):
        color_list = ['Vo','Da','Vi','Ex']
        aim = input['aim']
        critical = float(input['critical'])
        ATK_dict = {}
        buff_dict = situation.get_buff()
        passive_dict = situation.get_passive(settings.aquired_passive)
        put_buff=[]
        for col in color_list:
            color = aim if col == 'Ex' else col 
            # サポステの合計
            S_status = settings.sumSstatus(color)
            #アピール倍率
            weapon_rate = self.info['weapon_rate'][col]
            #LINK処理
            if self.info['isLink']:
                if self.info['link_type'] == 'ATK':
                    weapon_rate += self.info['link_contents'][color]
                elif self.info['link_type'] == 'buff':
                    put_buff += self.info['link_contents']      
            buff = 1 + (buff_dict[color]+passive_dict[color])/100
            # print(f'{color} b{buff_dict[color]} %UP p{passive_dict[color]} %UP →{buff}')
            iP = situation.Pstatus[color]
            ATK =int(int(int(iP*2 + S_status*0.2*(1+0.1*settings.week))*buff*critical) * weapon_rate)
            ATK_dict[col]=ATK
        put_buff += self.info['buff']
        return ATK_dict,put_buff
        
    def push2DB(self,FlaskSession):
        import Entity
        import DataHandler as DH
        action = ""
        existing_record = DH.session.query(Entity.PWeapon).filter_by(name=self.info['card_name']).first()
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
            entity = Entity.PWeapon()
        elif action == 'update':
            entity = existing_record
        
        entity.name = self.info['card_name']
        entity.ATK_type = self.info['ATKtype']
        entity.Vo = self.info['weapon_rate']["Vo"]
        entity.Da = self.info['weapon_rate']["Da"]
        entity.Vi = self.info['weapon_rate']["Vi"]
        entity.Ex = self.info['weapon_rate']["Ex"]
        entity.buff_relations = []
        entity.link_buff = []
        for buff in self.info['buff']:
            buffEntity = Entity.Buff(
                color=buff['color'],
                rate=buff['buff'],
                turn=buff['turn'],
                val=str(buff['fanc']),
                created_by = FlaskSession['username']
            )
            entity.buff_relations.append(buffEntity)
        entity.link_type = self.info['link_type']
        if self.info['link_type'] == 'ATK':
            entity.link_Vo = self.info['link_contents']['Vo']
            entity.link_Da = self.info['link_contents']['Da']
            entity.link_Vi = self.info['link_contents']['Vi']
        
        elif self.info['link_type'] == 'buff':
            for buff in self.info['link_contents']:
                buffEntity = Entity.Buff(
                color=buff['color'],
                rate=buff['buff'],
                turn=buff['turn'],
                val=str(buff['fanc']),
                created_by = FlaskSession['username']
            )
            entity.link_buff.append(buffEntity)
        entity.created_by = FlaskSession['username']
        
        entity.produce_card = DH.session.query(Entity.ProduceCard).filter(
            Entity.ProduceCard.card_name.like(f"{entity.name[:-2]}%") ).first()
        entity.support = DH.session.query(Entity.Support).filter(
            Entity.Support.name.like(f"{entity.name[:-2]}%")).first()
        if action == 'create':
            DH.session.add(entity)
        DH.session.commit() 
        return "登録完了"


        #%%