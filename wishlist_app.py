import streamlit as st
import pandas as pd
import os

# File to store the wishlist data
FILE_PATH = "home_wishlist.csv"

# Initialize the CSV if it doesn't exist yet
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Item", "Room", "Priority", "Estimated_Cost", "Purchased"])
    df.to_csv(FILE_PATH, index=False)

def load_data():
    return pd.read_csv(FILE_PATH)

def save_data(dataframe):
    dataframe.to_csv(FILE_PATH, index=False)

# Page configuration
st.set_page_config(page_title="Home Wishlist", page_icon="🏡", layout="wide")
st.title("🏡 Home Wishlist Dashboard")

# --- SECTION 1: Add a New Item ---
with st.expander("➕ Add a New Item", expanded=True):
    with st.form("add_item_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        item_name = col1.text_input("Item Name (e.g., Coffee Maker)")
        room = col2.selectbox("Room", ["Kitchen", "Living Room", "Master Bedroom", "Kids Room", "Bathroom", "Other"])
        priority = col1.selectbox("Priority", ["High (Need)", "Medium", "Low (Want)"])
        price = col2.number_input("Estimated Cost", min_value=0.0, step=50.0)
        
        submitted = st.form_submit_button("Add to List")
        
        if submitted and item_name:
            df = load_data()
            new_row = pd.DataFrame([{
                "Item": item_name, 
                "Room": room, 
                "Priority": priority, 
                "Estimated_Cost": price, 
                "Purchased": False
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"Added '{item_name}' to your wishlist!")
            st.rerun()

# --- SECTION 2: View and Edit Wishlist ---
st.subheader("📋 Manage Your List")
df = load_data()

if not df.empty:
    st.write("You can edit prices, check off purchased items, or delete rows directly in the table below. Remember to click **Save Changes** when you're done!")
    
    # Interactive data editor
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",  # Allows you to delete rows by selecting them and pressing delete
        use_container_width=True,
        hide_index=True,
        column_config={
            "Purchased": st.column_config.CheckboxColumn("Purchased?", default=False),
            "Estimated_Cost": st.column_config.NumberColumn("Estimated Cost", format="$%.2f")
        }
    )
    
    if st.button("💾 Save Changes", type="primary"):
        save_data(edited_df)
        st.success("Wishlist updated successfully!")
        st.rerun()
        
    # --- SECTION 3: Quick Insights ---
    st.divider()
    
    # Calculate costs only for items that haven't been purchased yet
    pending_items = edited_df[~edited_df["Purchased"]]
    total_needed = pending_items["Estimated_Cost"].sum()
    
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric("Total Pending Cost", f"${total_needed:,.2f}")
    col_metric2.metric("Items Left to Buy", len(pending_items))

else:
    st.info("Your wishlist is currently empty. Add your first item above!")