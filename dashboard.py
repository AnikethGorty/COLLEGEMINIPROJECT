import streamlit as st
from db import (
    get_user_by_id, get_all_items, buy_item, sell_item,
    get_user_items, create_item, make_admin, get_all_users,
    clear_database
)

def show_dashboard():
    user_id = st.session_state["user_id"]
    user = get_user_by_id(user_id)

    st.sidebar.title("Account")
    st.sidebar.write(f"Logged in as: `{user.email}`")
    st.sidebar.write(f"Balance: 💰 {user.balance} coins")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("🛒 TradeZone Marketplace")
    st.subheader("Available Items")
    items = get_all_items()

    for item in items:
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"**{item.name}**")
        col2.write(f"💰 Price: {item.price}")
        col3.write(f"📦 Stock: {item.quantity}")
        if col4.button("Buy", key=f"buy_{item.id}"):
            buy_item(user.id, item.id)

    st.subheader("📦 Your Inventory")
    inventory = get_user_items(user.id)
    for entry in inventory:
        item = entry.item
        col1, col2, col3 = st.columns(3)
        col1.write(f"**{item.name}**")
        col2.write(f"Qty: {entry.quantity}")
        if col3.button("Sell", key=f"sell_{entry.id}"):
            sell_item(user.id, item.id)

    if user.is_admin:
        st.subheader("🛠 Admin Panel")

        st.markdown("### ➕ Add New Item")
        name = st.text_input("Item Name")
        price = st.number_input("Item Price", min_value=1)
        quantity = st.number_input("Item Quantity", min_value=1)
        if st.button("Create Item"):
            create_item(name, price, quantity)
            st.success("Item created!")
            st.rerun()

        st.markdown("### 👑 Promote User to Admin")
        users = get_all_users()
        target = st.selectbox("Select User", [u.email for u in users if not u.is_admin])
        if st.button("Make Admin"):
            user_obj = next((u for u in users if u.email == target), None)
            if user_obj:
                make_admin(user_obj.id)
                st.success(f"{target} is now an admin.")
                st.rerun()

        st.markdown("### ❌ Danger Zone")
        if st.button("Clear Database"):
            clear_database()
            st.success("Database cleared!")
            st.rerun()
