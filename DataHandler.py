from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
import Entity
from dotenv import load_dotenv
import os

# .envファイルの環境変数を読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得する
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# SQLAlchemyの接続文字列を構築する
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

# 適切なDB接続情報を指定してエンジンを作成します。
engine = create_engine(connection_string,echo=False)

# ベースクラスの作成
Base = declarative_base()

# セッションの作成
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

def push2DB(entity,FlaskSession):
    try:
        # セッションを利用したデータベース操作
        if not FlaskSession.get('logged_in', False):
            return "ログインしてください"

        # エンティティの種類に応じて重複チェックと追加を行う
        if isinstance(entity, Entity.Support):
            existing_record = session.query(Entity.Support).filter_by(name=entity.name, totu=entity.totu).first()
        elif isinstance(entity, Entity.PWeapon):
            existing_record = session.query(Entity.PWeapon).filter_by(name=entity.name).first()
        elif isinstance(entity, Entity.ProduceCard):
            existing_record = session.query(Entity.ProduceCard).filter_by(card_name=entity.card_name).first()
        else:
            return "サポート, PWeapon, またはProduceCardを入力してください"

        entity.created_by = FlaskSession['username']
        # print(existing_record)

        if not existing_record:
            session.add(entity)
        else:
            if FlaskSession.get("oath_lv", 0) > 4:
                # マージで更新する
                session.delete(existing_record)
                session.commit()
                session.add(entity)
            else:
                return "このデータはすでに存在します。重複追加を避けました。"

        session.commit()  # トランザクションをコミット

        return "登録完了"

    except Exception as e:
        session.rollback()  # エラー発生時にはロールバックしてセッションをクリーンアップ
        return f"エラーが発生しました: {str(e)}"

def pushPassive2DB(input,session):
    entity = Entity.Passive()
    entity.cardname = input['card_name']
    entity.passive_type = input['passive_type']
    entity.short_name = input['icon']
    entity.times = input["times"]
    entity.rate = input["p"]
    entity.request = input['request']
    entity.args = input['args']
    for buff in input['buff']:
        passive_contents = Entity.PassiveRate(
        color=buff[0],
        rate=buff[1],
        created_by = session['username'],
    )
    entity.passiverate_relations.append(passive_contents)
    supportEnt = session.query(Entity.Support).filter_by(name=input['card_name']).first()
    if supportEnt:
        entity.support.append(supportEnt)
    return push2DB(entity,session)

def set_passive_from_entity(entity_list):
    from transfer_class import Passive
    passive_list = []
    for entity in entity_list:
        buff = []
        for contents in entity.passiverate_relations:
            buff.append([contents.color, contents.rate])
        func = Passive.condition_name_dict[entity.request]
        val = entity.args.split(',')
        passive_list.append(
        Passive.passive(
            entity.cardname,
            entity.passive_type,
            entity.short_name,
            entity.times,
            entity.rate,
            func,
            buff,
            val
        )
        )
    return passive_list

def pushDeck(settings, Flasksession):
    if len(Flasksession) == 0:
        return 'ログインしてください'

    entity = Entity.Deck()
    entity.name = settings['deck_name']
    entity.created_by = Flasksession['username']

    entity.produce_card = session.query(Entity.ProduceCard).filter_by(idol=settings['produce_idol'], card_name=settings['produce_card']).first()
    if not entity.produce_card:
        return 'プロデュースカードが見つかりません'

    entity.supports = []
    for support in settings['support_list']:
        support_entity = session.query(Entity.Support).filter_by(idol=support['idol_name'], name=support['card_name'], totu=support['totu']).first()
        if not support_entity:
            return f"サポートカードが見つかりません: {support['idol_name']}, {support['card_name']}, {support['totu']}"
        entity.supports.append(support_entity)

    if len(entity.supports) != 4:
        return 'サポートカードの数が間違っています'

    entity.pweapons = []
    for Pweapon in settings['pweapon_list']:
        Pweapon_entity = session.query(Entity.PWeapon).filter_by(name=Pweapon['card_name']).first()
        if not Pweapon_entity:
            return f"取得札が見つかりません: {Pweapon['card_name']}"
        entity.pweapons.append(Pweapon_entity)

    if len(entity.pweapons) != 4:
        return '取得札の数が間違っています'

    entity.passives = []
    for passive in settings['aquired_passive']:
        passive_entity = session.query(Entity.Passive).filter_by(cardname=passive['card_name'], passive_type=passive['type']).first()
        if not passive_entity:
            return f"パッシブが見つかりません: {passive['card_name']}, {passive['type']}"
        entity.passives.append(passive_entity)

    session.add(entity)
    session.commit()

    return '登録完了'

def setDeck(id):
    from transfer_class import Passive
    entity = session.query(Entity.Deck).filter_by(id=id).first()
    deck = {}
    passive_list = []
    produce_card = entity.produce_card
    passives = entity.passives
    deck['produce_idol'] = produce_card.idol
    deck['produce_card'] = produce_card.card_name
    deck['support_list'] = []
    for support in entity.supports:
        sup_dict = {
            'card_type':'S','idol_name':support.idol,'card_name':support.name,
            'totu':str(support.totu)+'凸','status':{'Vo':support.Vo,'Da':support.Da,'Vi':support.Vi},
            'appeal':{'Vo':support.Vo_rate,'Da':support.Da_rate,'Vi':support.Vi_rate,'Ex':support.Ex_rate},
            'ATKtype':'single','buff':[],'key':support.idol+support.name+str(support.totu)+'凸'
        }
        for buff in support.buff_relations:
            sup_dict['buff'].append( {
                'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                'val':None,'name':support.name + '(S)'
            })
        deck['support_list'].append(sup_dict)

    deck['pweapon_list'] = []
    for p in entity.pweapons:
        p_dict = {
            'idol_name':entity.produce_card.idol,'card_name':p.name,'ATKtype':p.ATK_type,
            'weapon_rate':{'Vo':p.Vo,'Da':p.Da,'Vi':p.Vi,'Ex':p.Ex},'card_type':'P',
            'buff':[],'link_type':p.link_type,'isLink':False
        }
        for buff in p.buff_relations:
            p_dict['buff'].append( {
                'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                'val':None,'name':support.name + '(P)'
            })
        if p.link_type == 'ATK':
            p_dict['link_contents'] = {'Vo':p.link_Vo,'Da':p.link_Da,'Vi':p.link_Vi}
        elif p.link_type == 'buff':
            p_dict['link_contents'] = []
            for buff in p.link_buff:
                p_dict['link_contents'].append( {
                    'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                    'val':None,'name':support.name + '(link)'
                })
        elif p.link_type == 'no_link':p_dict['link_contents'] = 'no_link'
        else:return 'error'
        deck['pweapon_list'].append(p_dict)

    deck['aquired_passive']=[]
    for pa in entity.passives:
        buffrate = [[b.color,b.rate] for b in pa.passiverate_relations]
        p = Passive.passive(
            name=pa.cardname,type=pa.passive_type,short_name=pa.short_name,
            times=pa.times,p=pa.rate,request=Passive.get_request_fanc(pa.request),
            buffs=buffrate,args=pa.args.split(',')
        )
        deck['aquired_passive'].append(p.get_dict())
        passive_list.append(
            {'name':p._name,'rest':p._times,'isActive':False,'text':p.get_text(),'short_name':p._short_name}
            )

    return deck,passive_list

def fetchPweaponPassive(deck):
    from Entity import PWeapon
    # print(deck)
    all_pweapon = []
    all_passive = []
    for idol,name in deck:
        pweapons = session.query(PWeapon).filter(PWeapon.name.like(name + '%')).all()
        for p in pweapons:
            p_dict = {
                'idol_name':idol,'card_name':p.name,'ATKtype':p.ATK_type,
                'weapon_rate':{'Vo':p.Vo,'Da':p.Da,'Vi':p.Vi,'Ex':p.Ex},'card_type':'P',
                'buff':[],'link_type':p.link_type,'isLink':False
            }
            for buff in p.buff_relations:
                p_dict['buff'].append( {
                'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                'val':None,'name':name + '(P)'
            })
            if p.link_type == 'ATK':
                p_dict['link_contents'] = {'Vo':p.link_Vo,'Da':p.link_Da,'Vi':p.link_Vi}
            elif p.link_type == 'buff':
                p_dict['link_contents'] = []
                for buff in p.link_buff:
                    p_dict['link_contents'].append( {
                        'color':buff.color,'buff':buff.rate,'turn':buff.turn,
                        'val':None,'name':name + '(link)'
                    })
            elif p.link_type == 'no_link':p_dict['link_contents'] = 'no_link'
            else:return 'error'
            all_pweapon.append(p_dict)
    for idol,card_name in deck:
        all_passive += session.query(Entity.Passive).filter_by(cardname=card_name).all().copy()
    all_passive = set_passive_from_entity(all_passive)
    all_passive = [passive.get_dict() for passive in all_passive]
    return {'all_passive':all_passive,'all_pweapon':all_pweapon}



def readAll(Entity):
    return session.query(Entity).all()


