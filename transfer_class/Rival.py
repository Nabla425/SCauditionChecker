import random,json
class rival():
    info:dict
    '''
    name:str
    HP:int
    baseATK:int
    memATK:int
    color:str
    choice_type:str
    choice_order:list
    star:int 
    aim:str
    mem_turn:int
    '''
    def __init__(self,info):
        self.info=info
        
    def __str__(self):
        out = ""
        out += ("名前:" + self.info['name']+"\n")
        out += ("HP:" + str(self.info['HP'])+"\n")
        out += ("基礎攻撃力:" + str(self.info['baseATK'])+"\n")
        out += ("思い出火力:" + str(self.info['memATK'])+"\n")
        out += ("得意属性:" + self.info['color']+"\n")
        out += ("遷移タイプ:" + ('スピア' if self.info['choice_type'] == 's' else 'ループ')+"\n")
        out += ("遷移順:" + ",".join(map(str, self.info['choice_order']))+"\n")
        return out
    
    def get_critical_str(self):
        fix_dict = {'p':'Perfect','g':'Good','n':'Normal','b':'Bad','m':'Memory','':'未初期化'}
        return fix_dict[self.info['critical']]
    
    def set_aim(self,trend,turn,judge_alive_dict):
        # print(self.info['name'],self.info['choice_order'],self.info['choice_type'])
        #                        [3, 1, 2]
        #judge_arive_dict {'Vo':true,'Da':true,'Vi':false}
        #trend = {'Vo':1,'Da':2,'Vi':3}->['Vo','Da','Vi']
        trend_list = ['','','']
        for k,v in trend.items():
            trend_list[v-1]=k
        # print(trend,trend_list)
        # print(judge_alive_dict)

        if self.info["choice_type"] == "s":
            for i in range(3):
                #スピア先の流行順位
                aim_trend = self.info['choice_order'][i]
                #スピア先の属性
                aim_color = trend_list[aim_trend-1]
                if judge_alive_dict[aim_color]:
                    self.info['aim'] = aim_color
                    print('aim:'+aim_color)
                    break
                
        if self.info["choice_type"] == "t":
            for i in range(3):
                #ATK先の流行順位
                aim_trend = self.info['choice_order'][(turn-1+i)%3]
                #ATK先の属性
                aim_color = trend_list[aim_trend-1]
                if judge_alive_dict[aim_color]:
                    self.info['aim'] = aim_color
                    print('aim:'+aim_color)
                    break
        
    
    
    
        
    
    