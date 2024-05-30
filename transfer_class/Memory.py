from transfer_class import Settings,Situation
class memory():
    info:dict
    '''
    lv:int
    '''
 
    def __init__(self,lv=1,idol_name='櫻木真乃',link=[]):
        self.info = {
            'lv':lv,'ATKtype':'whole','card_type':'M','idol_name':idol_name,'isLink':False,
            'link':link
        }
    
    
    def getATK(self,settings:Settings,situation:Situation,input):
        critical = float(input['critical'])
        aim = input['aim']
        rate_list = [0,0.8,1.0,1.2,1.4,2.0]
        put_buff=[]
        print(self.info['lv'])
        rate = rate_list[self.info['lv']]
        ATK_dict={}
        buff_dict = situation.get_buff()
        color_list = ['Vo','Da','Vi']
        for color in color_list:
            buff = buff_dict[color]
            #サポートのステ合計の算出
            S_status = settings.sumSstatus(color)
            #攻撃力計算
            iP = situation.Pstatus[color]
            if self.info['isLink'] and len(self.info['link'])>0:
                if self.info['link'][0] == 'ATK':
                    rate += self.info['link'][1][col]
                elif self.info['link'][0] == 'buff':
                    put_buff += self.info['link'][1]
            ATK = int(int(int(iP*2 + S_status * 0.2 * (1 + 0.1*settings.week)) * buff*critical )*rate)
            ATK_dict[color]=ATK
        return ATK_dict,put_buff