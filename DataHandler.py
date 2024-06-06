from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 適切なDB接続情報を指定してエンジンを作成します。
engine = create_engine('mysql+pymysql://root:AdminAdmin@localhost/scdb')

# ベースクラスの作成
Base = declarative_base()

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

def push2DB(entity):
    # データベース内に同じ内容のレコードが存在しないか確認
    existing_record = session.query(type(entity)).filter_by(**{col.name: getattr(entity, col.name) for col in entity.__table__.columns}).first()

    # 存在しない場合のみ追加操作を行う
    if not existing_record:
        # セッションに追加
        session.add(entity)
        # コミットしてデータベースに保存
        session.commit()
    else:
        print("このデータはすでに存在します。重複追加を避けました。")
    
def readAll(Entity):
    return session.query(Entity).all()