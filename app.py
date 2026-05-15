import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import tempfile

# ✅ TITLE
st.title("📦 Distributor Inventory Submission")

# ✅ INPUTS
company = st.text_input("Company Name *", key="company_input")
email = st.text_input("Email ID *", key="email_input")

# ✅ MONTH LOGIC
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month

if current_month == 1:
    previous_month = "Dec"
else:
    previous_month = months[current_month - 2]

st.info(f"📅 Enter Inventory for: {previous_month}")

# ✅ SKU MASTER (sample)
sku_master = pd.DataFrame({
    "Segment": [
        "MD_AGA ACCESSORIES",
        "MD_AGA ACCESSORIES",
        "MD_CONGENITAL ASD"
    ],
    "SKU": [
        "9-ATV07F45/80",
        "9-ATV08F45/80",
        "9-ASD-010"
    ]
})

# ✅ BUILD TABLE
df_table = pd.DataFrame({
    "SKU": sku_master["SKU"],
    "Segment": sku_master["Segment"],
    "Previous Month": [0, 0, 0],
    "Enter Now": [0, 0, 0]
})

st.subheader("📊 Enter Inventory")

# ✅ IMPORTANT → always visible
edited_df = st.data_editor(df_table, num_rows="fixed")

# ✅ SUBMIT
if st.button("Submit"):

    # ✅ FIXED VALIDATION (THIS WAS YOUR ISSUE)
    if company is None or email is None or company.strip() == "" or email.strip() == "":
        st.error("❌ Please fill all mandatory fields")

    else:
        try:
            # ✅ PREPARE DATA
            save_data = []

            for _, row in edited_df.iterrows():
                save_data.append({
                    "Company": company.strip(),
                    "Email": email.strip(),
                    "Month": previous_month,
                    "SKU": row["SKU"],
