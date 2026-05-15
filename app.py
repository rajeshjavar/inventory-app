import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File path (temporary for cloud)
FILE_PATH = "Inventory_Master.xlsx"

st.title("📦 Distributor Inventory Submission")

# Inputs
company = st.text_input("Company Name *")
email = st.text_input("Email ID *")

# Month logic
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month

if current_month == 1:
    previous_month = "Dec"
else:
    previous_month = months[current_month - 2]

st.info(f"📅 Enter Inventory for: {previous_month}")

# Create empty file if not exists
if not os.path.exists(FILE_PATH):
    df_empty = pd.DataFrame(columns=["Company", "Email", "Month", "SKU", "Quantity", "Segment"])
    df_empty.to_excel(FILE_PATH, index=False)

# Load existing data
df_existing = pd.read_excel(FILE_PATH)

# Sample SKU list
sku_master = pd.DataFrame({
    "Segment": ["MD_AGA ACCESSORIES", "MD_AGA ACCESSORIES", "MD_CONGENITAL ASD"],
    "SKU": ["9-ATV07F45/80", "9-ATV08F45/80", "9-ASD-010"]
})

# Previous month function
def get_previous_data(company, sku):
    prev_month_index = months.index(previous_month) - 1
    if prev_month_index < 0:
        return 0
    prev_month_name = months[prev_month_index]

    df_prev = df_existing[
        (df_existing["Company"] == company) &
        (df_existing["Month"] == prev_month_name) &
        (df_existing["SKU"] == sku)
    ]

    if not df_prev.empty:
        return int(df_prev["Quantity"].values[0])
    return 0

# Build table
table_data = []

for _, row in sku_master.iterrows():
    prev_val = get_previous_data(company, row["SKU"]) if company else 0
    
    table_data.append({
        "SKU": row["SKU"],
        "Segment": row["Segment"],
        "Previous Month": prev_val,
        "Enter Now": 0
    })

df_table = pd.DataFrame(table_data)

st.subheader("📊 Enter Inventory")

edited_df = st.data_editor(df_table, num_rows="fixed")

# Submit
if st.button("Submit"):

    if not company or not email:
        st.error("❌ Please fill all mandatory fields")
    
    else:
        existing_check = df_existing[
            (df_existing["Company"] == company) &
            (df_existing["Month"] == previous_month)
        ]

        if not existing_check.empty:
            st.error("❌ Already submitted for this month")
        
        else:
            save_data = []

            for _, row in edited_df.iterrows():
                save_data.append({
                    "Company": company,
                    "Email": email,
                    "Month": previous_month,
                    "SKU": row["SKU"],
                    "Quantity": row["Enter Now"],
                    "Segment": row["Segment"]
                })

            df_new = pd.DataFrame(save_data)
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
            df_final.to_excel(FILE_PATH, index=False)

            st.success("✅ Data submitted successfully!")

# Admin view
if st.checkbox("🔍 View All Data"):
    st.dataframe(df_existing)
