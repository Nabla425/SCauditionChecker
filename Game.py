from transfer_class import Settings,Situation,Rival,Judge,P_weapon,Support
import random

class play():
    settings:Settings
    situation:Situation
    isFinish:bool
    
    def __init__(self,settings,situation):
        self.settings=settings
        self.situation=situation
        self.isFinish = False
    
    '''
    input:dict GETで送られてくる情報
    [('weapon', 'P3'), ('aim', 'Vi'), ('critical', 'Perfect')]
    '''
    # 終了条件を満たしていればTrueを返す
    def oneTurnProcess(self,input:dict)->bool:
        print('exe_turn')
        weapon = self.json_to_weapon(input)
        sequences = self.get_sequence(weapon,float(input['critical']))
        #行動順位並べ替えて、メイフェーズ処理
        for action in sequences:
            if type(action) == Rival.rival:
                self.rival_move(action)
            elif type(action) == Judge.judge:
                self.judge_move(action)
            elif type(action) == P_weapon.pweapon or type(action) ==Support.support:
                self.myunit_move(weapon,input)
            else:
                print('error!!!!')
            
        if self.chk_end():
            return True
        #ターン終了
        self.situation.turn += 1
        if self.situation.turn > 6:
            return True

        #次ターン開始処理
        self.start_step()
        return False

    def chk_end(self):
        isDead = True
        for  col,judge in self.situation.judge_dict.items():
            isDead =isDead and judge.info['HP'] <=0
        return isDead

    # ターン開始処理
    def start_step(self):
        #対面の判定と狙い先のセット
        turn = self.situation.turn
        trend = self.settings.trend
        self.settings.set_rival_critical(turn)
        isAlive = self.situation.get_judge_alive_dict()
        self.settings.set_rival_aim(trend,turn,isAlive)
        
        #泣いていたパッシブを消去し、残り発動回数をデクリメント
        
        #このターンに鳴くパッシブを決めてpassive_listに追加
        
        #バフの残りターンをデクリメント
        # print(self.situation.buff_list)
        for contents in self.situation.buff_list:
            if contents['turn']>1:
                contents['turn'] -=1
            elif contents['turn'] == 0:
                self.situation.buff_list.remove(contents)

    def rival_move(self,rival):
        critical_rate_dict = {'p':1.5,'g':1.1,'n':1.0,'b':0.5}
        rival.set_aim(self.settings.trend,self.situation.turn,self.situation.get_judge_alive_dict())
        aim = rival.info['aim']
        critical = rival.info['critical']
        if critical == 'm':
            for col in['Vo','Da','Vi']:
                damage = int(rival.info['memATK'])
                self.situation.judge_dict[col].info['HP'] -= int(damage)
                if self.situation.judge_dict[col].info['HP']<0:
                    #LA処理(未実装)
                    self.situation.judge_dict[col].info['HP']=0
                print(rival.info['name'],critical,damage,col)
        else:
            damage = rival.info['baseATK']
            critical_rate = critical_rate_dict[critical]
            if aim == rival.info['color']:
                damage *= 2
            self.situation.judge_dict[aim].info['HP']-= int(damage*critical_rate)
            if self.situation.judge_dict[aim].info['HP']<0:
                #LA処理(未実装)
                self.situation.judge_dict[aim].info['HP']=0
            print(rival.info['name'],critical,int(damage*critical_rate),aim)
    
    def json_to_weapon(self,input):
        card_type,idx = list(input['weapon'])
        idx = int(idx)
        # print(card_type,idx)
        aim = input['aim']
        if card_type=='S':
            weapon = self.settings.support_list[idx]
        elif card_type == 'P':
            weapon = self.settings.pweapon_list[idx]
        return weapon
           
    def myunit_move(self,weapon,input):
        #攻撃力計算　各属性の基礎攻撃力(属性一致かどうかは次で計算)
        ATK_dict,put_buff = weapon.getATK(self.settings,self.situation,input)
        appeal_dict={'Vo':0,'Da':0,'Vi':0}
        # print(ATK_dict)
        aim = input['aim']
        if weapon.info['ATKtype']=='single':
            appeal_dict[aim] += sum(ATK_dict.values())
            #Excellent処理(aimと一致した属性の攻撃は2倍)
            appeal_dict[aim] += ATK_dict[aim]
        elif weapon.info['ATKtype']=='whole':
            for col in appeal_dict.keys():
                appeal_dict[col] += sum(ATK_dict.values())
                #Excellent処理(aimと一致した属性の攻撃は2倍)
                appeal_dict[col] += ATK_dict[col]  
        # print(appeal_dict)
        self.situation.buff_list += put_buff
        for col in ['Vo','Da','Vi']:
            if appeal_dict[col]>0:
                self.situation.judge_dict[col].info['HP'] -= appeal_dict[col]
                print(weapon.info['card_name'],appeal_dict[col],col)
                if self.situation.judge_dict[col].info['HP'] <= 0:
                    #LA処理(未実装)
                    self.situation.judge_dict[col].info['HP'] = 0
    
    def judge_move(self,judge:Judge.judge):
        if judge.info['HP']>0:
            idols = [x for x in self.settings.rival_list]
            idols.append('Me')
            # 各アイドルの注目度リスト
            attention_list = [1 for idol in idols]
            #注目度に従って3名攻撃対象を選ぶ
            selected = self.choice_idol_damaged(idols,attention_list)
            print(judge.info['color'],'judge->',end = '')
            for idol in selected:
                if idol == 'Me':
                    print('Myunit',end = ' ')
                    self.situation.Pstatus['Me'] -= judge.info['ATK']
                else:
                    print(idol.info['name'],end=' ')
                    idol.info['HP'] -= judge.info['ATK']
            print('')
    
    def choice_idol_damaged(self,idols,attention):
        target_list = []
        flg = 0
        while(flg<3):
            target = random.choices(idols, weights = attention)
            if target[0] not in target_list:
                target_list.extend(target)
                flg += 1
        return target_list
    
    def get_sequence(self,weapon,self_critical):
        point_dict = {'m':1.5,'p':1.5,'g':1.1,'n':1.0,'b':0.5}
        sequence_point = {rival:point_dict[rival.info['critical']]+(ord(rival.info['name'])-65)/100 for rival in self.settings.rival_list}
        sequence_point[weapon] = self_critical+0.09
        sequence_point[self.situation.judge_dict['Vo']] = 1.07
        sequence_point[self.situation.judge_dict['Da']] = 1.08
        sequence_point[self.situation.judge_dict['Vi']] = 1.09
        # print({k:v for k,v in point_dict.items()})
        # print(sorted(sequence_point.items(), key=lambda x:x[1],reverse=True))
        return [x[0] for x in sorted(sequence_point.items(), key=lambda x:x[1],reverse=True)]
        
        #%%