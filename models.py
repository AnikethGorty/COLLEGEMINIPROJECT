from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    tenant_id = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    balance = Column(Integer, default=1000)
    is_admin = Column(Boolean, default=False)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)

class InventoryEntry(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer)

    item = relationship("Item")
