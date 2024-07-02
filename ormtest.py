from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload
import Entity
import DataHandler as DH

# 適切なDB接続情報を指定してエンジンを作成します。
engine = create_engine('mysql+pymysql://root:AdminAdmin@localhost/scdb')

# セッションを作成します。
engine.dispose()
Session = sessionmaker(bind=engine)
session = Session()

list = session.query(Entity.Support).all()
all_supports = []
support_entities = DH.session.query(Entity.Support).filter_by(created_by='admin').all().copy()
username = 'test'
if username != 'admin':
    support_entities += DH.session.query(Entity.Support).filter_by(created_by=username).all().copy()
    
for support in support_entities:
    print(support.passive_relations)
    if support.pweapons:
        for weapon in support.pweapons:
            print(weapon.name)

Pcards = DH.session.query(Entity.ProduceCard).all()

for Pcard in Pcards:
    for pweapon in Pcard.pweapons:
        print(pweapon.name)
    
# セッションを閉じます。
session.close()