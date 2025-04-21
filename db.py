from models import Base, User, Item, InventoryEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload

engine = create_engine("sqlite:///tradezone.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def ensure_default_admin():
    session = Session()
    if not session.query(User).filter_by(email="admin").first():
        admin = User(id="admin", tenant_id="admin-tenant", email="admin", password="admin", balance=1000, is_admin=True)
        session.add(admin)
        session.commit()
    session.close()

def get_user_by_email(email):
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    return user

def get_user_by_id(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user

def create_user(user_id, tenant_id, email, password):
    session = Session()
    user = User(id=user_id, tenant_id=tenant_id, email=email, password=password, balance=1000, is_admin=False)
    session.add(user)
    session.commit()
    session.close()

def get_all_items():
    session = Session()
    items = session.query(Item).filter(Item.quantity > 0).all()
    session.close()
    return items

def create_item(name, price, quantity):
    session = Session()
    item = Item(name=name, price=price, quantity=quantity)
    session.add(item)
    session.commit()
    session.close()

def buy_item(user_id, item_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    item = session.query(Item).get(item_id)

    if not user or not item:
        session.close()
        return

    if item.quantity > 0 and user.balance >= item.price:
        user.balance -= item.price
        item.quantity -= 1

        entry = session.query(InventoryEntry).filter_by(user_id=user_id, item_id=item_id).first()
        if entry:
            entry.quantity += 1
            user.balance-=item.price
            item.quantity-=1
        else:
            session.add(InventoryEntry(user_id=user_id, item_id=item_id, quantity=1))

        session.commit()
        session.refresh(user)  # Important if checking balance after purchase
        print(f"User balance after buying: {user.balance}")


    session.close()

def sell_item(user_id, item_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    item = session.query(Item).get(item_id)

    if not user or not item:
        session.close()
        return

    entry = session.query(InventoryEntry).filter_by(user_id=user_id, item_id=item_id).first()
    if entry and entry.quantity > 0:
        entry.quantity -= 1
        user.balance += item.price
        item.quantity += 1

        if entry.quantity == 0:
            session.delete(entry)

        session.commit()
        session.refresh(user)  # Ensure updated balance is immediately accessible
        print(f"User balance after selling: {user.balance}")


    session.close()


def get_user_items(user_id):
    session = Session()
    entries = session.query(InventoryEntry).options(joinedload(InventoryEntry.item)).filter_by(user_id=user_id).all()
    session.close()
    return entries

def make_admin(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    user.is_admin = True
    session.commit()
    session.close()

def get_all_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def clear_database():
    session = Session()
    session.query(InventoryEntry).delete()
    session.query(Item).delete()
    session.query(User).filter(User.email != "admin").delete()
    admin = session.query(User).filter_by(email="admin").first()
    admin.balance = 1000
    session.commit()
    session.close()
