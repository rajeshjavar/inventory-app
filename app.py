import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ TITLE
st.title("📦 Distributor Inventory Submission")

# ✅ INPUTS
company = st.text_input("Company Name")
email = st.text_input("Email ID")

# ✅ MONTH LOGIC
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month
previous_month = months[current_month - 2] if current_month > 1 else "Dec"

st.info(f"Enter Inventory for: {previous_month}")

# ✅ SAMPLE SKU MASTER (replace later with your actual file)
sku_master = pd.DataFrame({
    "SKU": ["9-ATV07F45/80", "9-ATV08F45/80", "9-ASD-010"],
    "Segment": ["MD_AGA ACCESSORIES", "MD_AGA ACCESSORIES", "MD_CONGENITAL ASD"]
})

# ✅ BUILD TABLE
df = sku_master.copy()
df["Previous Month"] = [10, 20, 30]   # sample data
df["Enter Now"] = [0, 0, 0]

st.subheader("Enter Inventory")

# ✅ EDITABLE TABLE
edited_df = st.data_editor(df, num_rows="fixed")

# ✅ SUBMIT BUTTON
if st.button("Submit"):

    # ✅ SIMPLE VALIDATION (NO BUGS)
    if company.strip() == "" or email.strip() == "":
        st.warning("⚠ Please enter Company and Email properly")

    else:
        # ✅ PREPARE DATA
        df_final = edited_df.copy()
        df_final["Company"] = company.strip()
        df_final["Email"] = email.strip()
        df_final["Month"] = previous_month

        # ✅ CONVERT TO CSV (EXCEL COMPATIBLE)
        csv_data = df_final.to_csv(index=False).encode("utf-8")

        st.success("✅ Data ready. Please download and share.")

        # ✅ DOWNLOAD BUTTON
        st.download_button(
            label="📥 Download Inventory File",
            data=csv_data,
            file_name=f"Inventory_{company}_{previous_month}.csv",
            mime="text/csv"
        )
