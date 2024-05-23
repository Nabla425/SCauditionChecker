from transfer_class import Settings,Situation
import inspect
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
        #自分のATK
        print('exe_turn')
        self.myunit_move(input)
        #ライバルのATK
        for rival in self.settings.rival_list:
            self.rival_move(rival)
            
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
            print(isDead)
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
        print(card_type,idx)
        aim = input['aim']
        if card_type=='S':
            weapon = self.settings.support_list[idx]
        elif card_type == 'P':
            weapon = self.settings.pweapon_list[idx]
        #攻撃力計算　各属性の基礎攻撃力(属性一致かどうかは次で計算)
        ATK_dict,put_buff = weapon.getATK(self.settings,self.situation,input)
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
        self.situation.buff_list += put_buff
        print('------------')
        for col in ['Vo','Da','Vi']:
            self.situation.judge_dict[col].info['HP'] -=min(self.situation.judge_dict[col].info['HP'],appeal_dict[col])