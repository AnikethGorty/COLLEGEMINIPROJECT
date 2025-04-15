#models.py
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    tenant_id = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    coins = Column(Integer, default=1000)
    is_admin = Column(Integer, default=0)

class Item(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    item_id = Column(String, ForeignKey('items.id'))
    quantity = Column(Integer)

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(String, primary_key=True)
    seller_id = Column(String, ForeignKey('users.id'))
    item_id = Column(String, ForeignKey('items.id'))
    quantity = Column(Integer)
    price = Column(Integer)

engine = create_engine('sqlite:///tradezone.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
