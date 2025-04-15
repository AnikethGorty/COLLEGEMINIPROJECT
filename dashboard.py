# dashboard.py
import streamlit as st
from db import get_items, get_user, update_inventory, record_transaction, get_inventory, session

def show_dashboard():
    st.subheader("Welcome to the Trading Zone!")
    user = get_user(st.session_state["user_id"])
    st.write(f"**Your balance:** 💰 {user.coins} coins")

    st.markdown("### Marketplace")
    items = get_items()
    for item in items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{item.name}** - {item.price} coins")
        with col2:
            quantity = st.number_input(f"Qty ({item.name})", min_value=1, step=1, key=item.id)
            if st.button(f"Buy {item.name}", key=f"buy_{item.id}"):
                total = item.price * quantity
                if user.coins >= total:
                    user.coins -= total
                    update_inventory(user.id, item.id, quantity)
                    record_transaction(user.id, item.id, "buy", quantity, total)
                    session.commit()
                    st.success(f"Bought {quantity} x {item.name}")
                    st.experimental_rerun()
                else:
                    st.error("Not enough coins!")

    st.markdown("### Your Inventory")
    for item in items:
        inv = get_inventory(user.id, item.id)
        if inv:
            st.write(f"{item.name}: {inv.quantity}")
            qty_sell = st.number_input(f"Sell Qty ({item.name})", min_value=1, max_value=inv.quantity, step=1, key=f"sell_qty_{item.id}")
            if st.button(f"Sell {item.name}", key=f"sell_{item.id}"):
                total = item.price * qty_sell
                user.coins += total
                update_inventory(user.id, item.id, -qty_sell)
                record_transaction(user.id, item.id, "sell", qty_sell, total)
                session.commit()
                st.success(f"Sold {qty_sell} x {item.name}")
                st.experimental_rerun()
