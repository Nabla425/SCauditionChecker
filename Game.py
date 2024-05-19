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
        for col in ['Vo','Da','Vi']:
            self.situation.judge_dict[col].info['HP'] -=min(self.situation.judge_dict[col].info['HP'],appeal_dict[col])