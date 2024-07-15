from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, ForeignKey, CheckConstraint, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

# .envファイルの環境変数を読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得する
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

engine = create_engine(connection_string, echo=False,pool_recycle=280)
# セッションを作成します。
Session = sessionmaker(bind=engine)
session = Session()


# ベースクラスの作成
Base = declarative_base()
Base.metadata.create_all(engine)

# 中間テーブルの定義
deck_passive = Table('deck_passive', Base.metadata,
    Column('deck_id', Integer, ForeignKey('deck.id')),
    Column('passive_id', Integer, ForeignKey('passive.id'))
)

deck_support = Table('deck_support', Base.metadata,
    Column('deck_id', Integer, ForeignKey('deck.id')),
    Column('support_id', Integer, ForeignKey('support.id'))
)

deck_pweapon = Table('deck_pweapon', Base.metadata,
    Column('deck_id', Integer, ForeignKey('deck.id')),
    Column('pweapon_id', Integer, ForeignKey('pweapon.id'))
)

class Support(Base):
    __tablename__ = 'support'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    idol = Column(String(10), nullable=False)
    totu = Column(Integer, nullable=False)
    Vo = Column(Integer, nullable=False)
    Da = Column(Integer, nullable=False)
    Vi = Column(Integer, nullable=False)
    Vo_rate = Column(Float, nullable=False, default=0.0)
    Da_rate = Column(Float, nullable=False, default=0.0)
    Vi_rate = Column(Float, nullable=False, default=0.0)
    Ex_rate = Column(Float, nullable=False, default=0.0)
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), nullable=False, default='admin')
    buff_relations = relationship('Buff', back_populates='support_relation', cascade='all, delete-orphan')
    passive_relations = relationship('Passive', back_populates='support', cascade='all, delete-orphan')
    decks = relationship("Deck", secondary=deck_support, back_populates="supports")
    pweapons = relationship("PWeapon", back_populates="support")

class Buff(Base):
    __tablename__ = 'buff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(5), nullable=False)
    rate = Column(Integer, nullable=False)
    turn = Column(Integer, nullable=False)
    val = Column(String(100))
    support_id = Column(Integer, ForeignKey('support.id'))
    pweapon_id = Column(Integer, ForeignKey('pweapon.id'))
    link_id = Column(Integer, ForeignKey('pweapon.id'))
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    support_relation = relationship('Support', back_populates='buff_relations')
    pweapon_relation = relationship('PWeapon', foreign_keys=[pweapon_id], back_populates='buff_relations')
    link_pweapon = relationship('PWeapon', back_populates='link_buff', foreign_keys=[link_id])

class PWeapon(Base):
    __tablename__ = 'pweapon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    ATK_type = Column(String(6), nullable=False)
    Vo = Column(Float, default=0.0)
    Da = Column(Float, default=0.0)
    Vi = Column(Float, default=0.0)
    Ex = Column(Float, default=0.0)
    link_type = Column(String(10), nullable=False)
    link_Vo = Column(Float,default=0.0)
    link_Da = Column(Float,default=0.0)
    link_Vi = Column(Float,default=0.0)
    support_id = Column(Integer, ForeignKey('support.id'))
    support = relationship("Support", back_populates="pweapons")
    produce_card_id = Column(Integer, ForeignKey('produce_card.id'))
    produce_card = relationship("ProduceCard", back_populates="pweapons")
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    CHECK_ATK_type = CheckConstraint("ATK_type IN ('single', 'whole')")
    CHECK_link_type = CheckConstraint("link_type IN ('ATK', 'buff','no_link','Plus')")
    buff_relations = relationship('Buff', back_populates='pweapon_relation', cascade='all, delete-orphan', foreign_keys='Buff.pweapon_id')
    link_buff = relationship('Buff', back_populates='link_pweapon', cascade='all, delete-orphan', foreign_keys='Buff.link_id')
    decks = relationship("Deck", secondary=deck_pweapon, back_populates="pweapons")

class Passive(Base):
    __tablename__ = 'passive'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cardname = Column(String(20), nullable=False)
    passive_type = Column(String(10), nullable=False)
    short_name = Column(String(10), nullable=False)
    times = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    request = Column(String(20), nullable=False)
    args = Column(String(100))
    produce_card_id = Column(Integer, ForeignKey('produce_card.id'))
    support_id = Column(Integer, ForeignKey('support.id'))
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    produce_card = relationship('ProduceCard', back_populates='passives', overlaps="passive_relations")
    support = relationship('Support', back_populates='passive_relations', overlaps="passive_relations")
    passiverate_relations = relationship('PassiveRate', back_populates='passive', cascade='all, delete-orphan')
    decks = relationship("Deck", secondary=deck_passive, back_populates="passives")

class PassiveRate(Base):
    __tablename__ = 'passive_rate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    passive_id = Column(Integer, ForeignKey('passive.id'))
    color = Column(String(5), nullable=False)
    rate = Column(Integer, nullable=False)
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    passive = relationship('Passive', back_populates='passiverate_relations')

class ProduceCard(Base):
    __tablename__ = 'produce_card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idol = Column(String(10), nullable=False)
    card_name =  Column(String(30), nullable=False, unique=True)
    created_at =  Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    passives = relationship('Passive', back_populates='produce_card')
    decks = relationship("Deck", back_populates="produce_card")
    pweapons = relationship("PWeapon", back_populates="produce_card")

class Deck(Base):
    __tablename__ = 'deck'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(String(10), default='admin')
    produce_card_id = Column(Integer, ForeignKey('produce_card.id'))
    produce_card = relationship("ProduceCard", back_populates="decks")
    passives = relationship("Passive", secondary=deck_passive, back_populates="decks", cascade="save-update, merge, refresh-expire, expunge")
    supports = relationship("Support", secondary=deck_support, back_populates="decks", cascade="save-update, merge, refresh-expire, expunge")
    pweapons = relationship("PWeapon", secondary=deck_pweapon, back_populates="decks", cascade="save-update, merge, refresh-expire, expunge")

class Users(Base):
    __tablename__ = 'users'
    username = Column(String(20), primary_key=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    oath_lv = Column(Integer, nullable=False, default=0)
    created = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())



# セッションを閉じます。
session.close()

try:
    # エンジンを作成して接続を試みる
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        # 接続が成功した場合、メッセージを表示する
        print("Database connection successful!")

except Exception as e:
    # エラーが発生した場合、エラーメッセージを表示する
    print(f"Database connection error: {str(e)}")
print("Done Database Prepare")


