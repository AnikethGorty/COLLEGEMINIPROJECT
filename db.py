# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Item, Inventory, Transaction
import uuid

engine = create_engine("sqlite:///tradezone.db")
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    seed_items()

def seed_items():
    if not session.query(Item).first():
        items = [
            {"name": "Gold Coin", "price": 100},
            {"name": "Silver Sword", "price": 200},
            {"name": "Health Potion", "price": 50}
        ]
        for item in items:
            new_item = Item(id=str(uuid.uuid4()), name=item["name"], price=item["price"])
            session.add(new_item)
        session.commit()

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def create_user(user_id, tenant_id, email, password):
    user = User(id=user_id, tenant_id=tenant_id, email=email, password=password, coins=1000)
    session.add(user)
    session.commit()

def get_items():
    return session.query(Item).all()

def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

def get_inventory(user_id, item_id):
    return session.query(Inventory).filter_by(user_id=user_id, item_id=item_id).first()

def update_inventory(user_id, item_id, quantity_change):
    inv = get_inventory(user_id, item_id)
    if inv:
        inv.quantity += quantity_change
        if inv.quantity <= 0:
            session.delete(inv)
        session.commit()
    else:
        new_inv = Inventory(id=str(uuid.uuid4()), user_id=user_id, item_id=item_id, quantity=quantity_change)
        session.add(new_inv)
        session.commit()

def record_transaction(user_id, item_id, action, quantity, total_price):
    txn = Transaction(
        id=str(uuid.uuid4()), user_id=user_id,
        item_id=item_id, action=action,
        quantity=quantity, total_price=total_price
    )
    session.add(txn)
    session.commit()
