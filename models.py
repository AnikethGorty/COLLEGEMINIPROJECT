# models.py
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    tenant_id = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    coins = Column(Integer, default=1000)

class Item(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)  # Price per unit

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    item_id = Column(String, ForeignKey('items.id'))
    quantity = Column(Integer)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(String, primary_key=True)
    user_id = Column(String)
    item_id = Column(String)
    action = Column(String)  # 'buy' or 'sell'
    quantity = Column(Integer)
    total_price = Column(Integer)
