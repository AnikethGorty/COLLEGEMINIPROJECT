#db.py
from models import *

def create_user(email, password):
    if get_user_by_email(email):
        return None, None
    user = User(id=str(uuid.uuid4()), tenant_id=str(uuid.uuid4()), email=email, password=password)
    session.add(user)
    session.commit()
    return user.id, user.tenant_id

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

def get_inventory(user_id):
    return session.query(Inventory).filter_by(user_id=user_id).all()

def update_inventory(user_id, item_id, quantity):
    inv = session.query(Inventory).filter_by(user_id=user_id, item_id=item_id).first()
    if inv:
        inv.quantity += quantity
    else:
        inv = Inventory(id=str(uuid.uuid4()), user_id=user_id, item_id=item_id, quantity=quantity)
        session.add(inv)
    session.commit()

def promote_user_to_admin(email):
    user = get_user_by_email(email)
    if user:
        user.is_admin = 1
        session.commit()
        return True
    return False

def create_item(name, price):
    item = Item(id=str(uuid.uuid4()), name=name, price=price)
    session.add(item)
    session.commit()

def list_item_for_sale(seller_id, item_id, quantity, price):
    listing = Listing(id=str(uuid.uuid4()), seller_id=seller_id, item_id=item_id, quantity=quantity, price=price)
    session.add(listing)
    session.commit()

def get_listings():
    return session.query(Listing).all()

def get_listing_by_id(listing_id):
    return session.query(Listing).filter_by(id=listing_id).first()

def delete_listing(listing):
    session.delete(listing)
    session.commit()

def ensure_default_admin():
    admin = get_user_by_email("admin")
    if not admin:
        admin_user = User(
            id=str(uuid.uuid4()),
            tenant_id=str(uuid.uuid4()),
            email="admin",
            password="admin",
            coins=1000,
            is_admin=1
        )
        session.add(admin_user)
        session.commit()
