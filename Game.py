from transfer_class import Settings,Situation
import inspect
class play():
    settings:Settings
    situation:Situation
    
    def __init__(self,settings,situation):
        self.settings=settings
        self.situation=situation
    
    '''
    input:dict GETで送られてくる情報
    [('weapon', 'P3'), ('aim', 'Vi'), ('critical', 'Perfect')]
    '''
    def oneTurnProcess(self,input:dict):
        #自分のATK
        print('exe_turn')
        self.myunit_move(input)
        #ライバルのATK
        critical_rate_dict = {'p':1.5,'g':1.1,'n':1.0,'b':0.5}
        for rival in self.settings.rival_list:
            aim = rival.info['aim']
            critical = rival.info['critical']
            print(rival.info['name'],critical)
            if critical == 'm':
                for col in['Vo','Da','Vi']:
                    damage = rival.info['memATK']
                    self.situation.judge_dict[col].info['HP'] -= int(damage)
                    if self.situation.judge_dict[col].info['HP']<0:
                        #LA処理(未実装)
                        self.situation.judge_dict[col].info['HP']=0
                    print(damage,col)
            else:
                damage = rival.info['baseATK']
                critical_rate = critical_rate_dict[critical]
                if aim == rival.info['color']:
                    damage *= 2
                self.situation.judge_dict[aim].info['HP']-= int(damage*critical_rate)
                if self.situation.judge_dict[aim].info['HP']<0:
                    #LA処理(未実装)
                    self.situation.judge_dict[aim].info['HP']=0
                print(damage*critical_rate,aim)

            
    def myunit_move(self,input):
        card_type,idx = list(input['weapon'])
        idx = int(idx)
        aim = input['aim']
        if card_type=='S':
            weapon = self.settings.support_list[idx]
        elif card_type == 'P':
            weapon = self.settings.pweapon_list[idx]
        #攻撃力計算　各属性の基礎攻撃力(属性一致かどうかは次で計算)
        ATK_dict = weapon.getATK(self.settings,self.situation,input)
        appeal_dict={'Vo':0,'Da':0,'Vi':0}
        print('myunit')
        print(ATK_dict)
        if weapon.info['ATKtype']=='single':
            appeal_dict[aim] += sum(ATK_dict.values())
            #Excellent処理(aimと一致した属性の攻撃は2倍)
            appeal_dict[aim] += ATK_dict[aim]
        elif weapon.info['ATKtype']=='whole':
            for col in appeal_dict.keys():
                appeal_dict[col] += sum(ATK_dict.values())
                #Excellent処理(aimと一致した属性の攻撃は2倍)
                appeal_dict[col] += ATK_dict[col]  
        print(appeal_dict)
        print('------------')
        for col in ['Vo','Da','Vi']:
            self.situation.judge_dict[col].info['HP'] -=min(self.situation.judge_dict[col].info['HP'],appeal_dict[col])