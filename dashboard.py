#dashboard.py
import streamlit as st
from db import *
from models import session, Item


def show_dashboard():
    user = get_user(st.session_state["user_id"])
    st.title(f"Welcome to TradeZone, {user.email}")
    st.write(f"You have {user.coins} coins")

    st.markdown("### Your Inventory")
    inventory = get_inventory(user.id)
    for inv in inventory:
        item = session.query(Item).filter_by(id=inv.item_id).first()
        st.write(f"{item.name}: {inv.quantity}")
        qty_sell = st.number_input(f"Sell how many of {item.name}", 0, inv.quantity, key=f"sell_{item.id}")
        price_sell = st.number_input(f"Sell price per unit", 1, key=f"price_{item.id}")
        if st.button(f"List {item.name} on marketplace", key=f"list_{item.id}"):
            list_item_for_sale(user.id, item.id, qty_sell, price_sell)
            update_inventory(user.id, item.id, -qty_sell)
            session.commit()
            st.success(f"Listed {qty_sell} x {item.name} at {price_sell} coins each")
            st.rerun()

    if user.is_admin:
        st.markdown("## 🛠️ Admin Panel")
        with st.expander("Promote User to Admin"):
            email_to_promote = st.text_input("User email")
            if st.button("Make Admin"):
                if promote_user_to_admin(email_to_promote):
                    st.success("User promoted!")
                else:
                    st.error("User not found")
        with st.expander("Create New Item"):
            new_name = st.text_input("Item name")
            new_price = st.number_input("Item price", min_value=1)
            if st.button("Add Item"):
                create_item(new_name, new_price)
                st.success(f"Created item: {new_name}")
                st.rerun()

    st.markdown("### 🌍 Public Marketplace")
    listings = get_listings()
    if listings:
        for listing in listings:
            item = session.query(Item).filter_by(id=listing.item_id).first()
            seller = get_user(listing.seller_id)
            st.write(f"**{item.name}** (Qty: {listing.quantity}, Price: {listing.price} coins each) — Seller: {seller.email}")
            qty_buy = st.number_input(f"Buy how many of {item.name}", 1, listing.quantity, key=f"mp_{listing.id}")
            if st.button(f"Buy from {seller.email}", key=f"buy_listing_{listing.id}"):
                total_price = qty_buy * listing.price
                if user.coins >= total_price:
                    user.coins -= total_price
                    seller.coins += total_price
                    update_inventory(user.id, item.id, qty_buy)
                    listing.quantity -= qty_buy
                    if listing.quantity <= 0:
                        delete_listing(listing)
                    session.commit()
                    st.success(f"Bought {qty_buy} x {item.name}")
                    st.rerun()
                else:
                    st.error("Not enough coins!")
    else:
        st.write("No public listings available.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
