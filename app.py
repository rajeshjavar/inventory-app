import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import tempfile

st.title("📦 Distributor Inventory Submission")

# ✅ Inputs
company = st.text_input("Company Name *")
email = st.text_input("Email ID *")

# ✅ Month logic
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month

if current_month == 1:
    previous_month = "Dec"
else:
    previous_month = months[current_month - 2]

st.info(f"📅 Enter Inventory for: {previous_month}")

# ✅ SKU Master (sample)
sku_master = pd.DataFrame({
    "Segment": ["MD_AGA ACCESSORIES", "MD_AGA ACCESSORIES", "MD_CONGENITAL ASD"],
    "SKU": ["9-ATV07F45/80", "9-ATV08F45/80", "9-ASD-010"]
})

# ✅ Build table
table_data = []

for _, row in sku_master.iterrows():
    table_data.append({
        "SKU": row["SKU"],
        "Segment": row["Segment"],
        "Previous Month": 0,
        "Enter Now": 0
    })

df_table = pd.DataFrame(table_data)

st.subheader("📊 Enter Inventory")

edited_df = st.data_editor(df_table, num_rows="fixed")

# ✅ Submit button
if st.button("Submit"):

    if not company or not email:
        st.error("❌ Please fill all mandatory fields")

    else:
        # ✅ Prepare data
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

        # ✅ Create temp Excel file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        df_new.to_excel(temp_file.name, index=False)

        try:
            # ✅ Read secrets
            SENDER_EMAIL = st.secrets["email"]
            PASSWORD = st.secrets["password"]

            RECEIVERS = [email, SENDER_EMAIL]

            # ✅ Create email
            msg = EmailMessage()
            msg["Subject"] = f"Inventory Submission - {company} - {previous_month}"
            msg["From"] = SENDER_EMAIL
            msg["To"] = ", ".join(RECEIVERS)

            msg.set_content(f"""
Hello,

Inventory submitted successfully.

Company: {company}
Month: {previous_month}

Please find attached Excel file.

Regards,
Inventory System
""")

            # ✅ Attach Excel
            with open(temp_file.name, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename="Inventory_Data.xlsx"
                )

            # ✅ Send mail
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, PASSWORD)
                server.send_message(msg)

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Email failed: {e}")
