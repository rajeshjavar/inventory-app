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
                    "Quantity": row["Enter Now"],
                    "Segment": row["Segment"]
                })

            df_new = pd.DataFrame(save_data)

            # ✅ CREATE CSV (NO EXCEL ERROR)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            df_new.to_csv(temp_file.name, index=False)

            # ✅ LOAD SECRETS
            SENDER_EMAIL = st.secrets["email"]
            PASSWORD = st.secrets["password"]

            # ✅ RECEIVERS
            RECEIVERS = [email.strip(), SENDER_EMAIL]

            # ✅ EMAIL OBJECT
            msg = EmailMessage()
            msg["Subject"] = f"Inventory Submission - {company} - {previous_month}"
            msg["From"] = SENDER_EMAIL
            msg["To"] = ", ".join(RECEIVERS)

            msg.set_content(f"""
Hello,

Inventory submitted successfully.

Company: {company}
Month: {previous_month}

Please find attached file.

Regards,
Inventory System
""")

            # ✅ ATTACH FILE
            with open(temp_file.name, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="text",
                    subtype="csv",
                    filename="Inventory_Data.csv"
                )

            # ✅ SEND EMAIL
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, PASSWORD)
                server.send_message(msg)

            st.success("✅ Data submitted & email sent successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")
``
