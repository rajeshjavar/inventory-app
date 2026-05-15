
mport smtplib
from email.message import EmailMessage
import tempfile
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Distributor Inventory Submission")

# ✅ User Inputs
company = st.text_input("Company Name *")
email = st.text_input("Email ID *")

# ✅ Month Logic
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month

if current_month == 1:
    previous_month = "Dec"
else:
    previous_month = months[current_month - 2]

st.info(f"📅 Enter Inventory for: {previous_month}")

# ✅ Empty Data (No Excel in Cloud)
df_existing = pd.DataFrame(columns=["Company", "Email", "Month", "SKU", "Quantity", "Segment"])

# ✅ SAMPLE SKU MASTER (we will replace later)
sku_master = pd.DataFrame({
    "Segment": ["MD_AGA ACCESSORIES", "MD_AGA ACCESSORIES", "MD_CONGENITAL ASD"],
    "SKU": ["9-ATV07F45/80", "9-ATV08F45/80", "9-ASD-010"]
})

# ✅ Previous Month Logic (placeholder)
def get_previous_data(company, sku):
    return 0  # No backend yet

# ✅ Build Table
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

# ✅ Editable Table
edited_df = st.data_editor(df_table, num_rows="fixed")

# ✅ Submit Button
if st.button("Submit"):

   if st.button("Submit"):

    if not company or not email:
        st.error("❌ Please fill all mandatory fields")

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

        # ✅ Create Excel file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        df_new.to_excel(temp_file.name, index=False)

        # ✅ Dummy email placeholders (we fix next step)
        SENDER_EMAIL = "test@email.com"
        PASSWORD = "password"
        RECEIVERS = [email, SENDER_EMAIL]
        msg = EmailMessage()
        msg["Subject"] = f"Inventory Submission - {company} - {previous_month}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECEIVERS)
        msg.set_content("Test email setup")
        st.success("✅ Email logic added (not sending yet)")

# ✅ Admin View
if st.checkbox("🔍 View All Data"):
    st.write("⚠ No permanent storage yet (cloud limitation)")
