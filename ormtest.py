from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload
from Entity import Support, Buff

# 適切なDB接続情報を指定してエンジンを作成します。
engine = create_engine('mysql+pymysql://root:AdminAdmin@localhost/scdb')

# セッションを作成します。
Session = sessionmaker(bind=engine)
session = Session()

new_support = Support(name='Support A', idol='Idol X', totu=100, Vo=50, Da=30, Vi=20)
session.add(new_support)
session.commit()

# サポートに関連付けられたバフを作成します。
new_buff = Buff(color='Red', rate=5, turn=3, val='Some value', support=new_support)
session.add(new_buff)
session.commit()

# READ (読み取り)
# サポートと関連付けられたすべてのバフを取得し、一覧表示します。
support_with_buffs = session.query(Support).options(joinedload(Support.buffs)).all()
for support in support_with_buffs:
    print(f'Support Name: {support.name}')
    print('Buffs:')
    for buff in support.buffs:
        print(f'  - Color: {buff.color}, Rate: {buff.rate}, Turn: {buff.turn}, Value: {buff.val}')

# セッションを閉じます。
session.close()