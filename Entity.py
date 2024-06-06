from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

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
    created_at = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    created_by = Column(String(10), nullable=False, default='admin')
    buff_relations = relationship('Buff', back_populates='support_relation')
    
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
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    created_by = Column(String(10), default='admin')
    support_relation = relationship('Support', back_populates='buff_relations')
    pweapon = relationship('PWeapon', foreign_keys=[pweapon_id], backref='buffs')
    link = relationship('PWeapon', foreign_keys=[link_id])
    
class PWeapon(Base):
    __tablename__ = 'pweapon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    ATK_type = Column(String(6), nullable=False)
    Vo = Column(Float, default=0.0)
    Da = Column(Float, default=0.0)
    Vi = Column(Float, default=0.0)
    link_type = Column(String(6), nullable=False)
    link_Vo = Column(Float)
    link_Da = Column(Float)
    link_Vi = Column(Float)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    created_by = Column(String(10), default='admin')
    CHECK_ATK_type = CheckConstraint("ATK_type IN ('single', 'whole')")
    CHECK_link_type = CheckConstraint("link_type IN ('ATK', 'buff')")
    
class Passive(Base):
    __tablename__ = 'passive'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    short_name = Column(String(10), nullable=False)
    times = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    request = Column(String(20), nullable=False)
    args = Column(String(100))
    pweapon_id = Column(Integer, ForeignKey('pweapon.id'))
    support_id = Column(Integer, ForeignKey('support.id'))
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    created_by = Column(String(10), default='admin')
    pweapon = relationship('PWeapon', backref='passives')
    support = relationship('Support', backref='passives')

class PassiveRate(Base):
    __tablename__ = 'passive_rate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    passive_id = Column(Integer, ForeignKey('passive.id'))
    color = Column(String(5), nullable=False)
    rate = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    created_by = Column(String(10), default='admin')
    passive = relationship('Passive', backref='rates')