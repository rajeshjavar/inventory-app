import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import tempfile

# ✅ APP TITLE
st.title("📦 Distributor Inventory Submission")

# ✅ INPUTS
company = st.text_input("Company Name *")
email = st.text_input("Email ID *")

# ✅ MONTH LOGIC
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month

if current_month == 1:
    previous_month = "Dec"
else:
    previous_month = months[current_month - 2]

st.info(f"📅 Enter Inventory for: {previous_month}")

# ✅ SKU MASTER (sample — we will load real later)
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

# ✅ BUILD TABLE (THIS WAS MISSING IN YOUR APP)
df_table = pd.DataFrame({
    "SKU": sku_master["SKU"],
    "Segment": sku_master["Segment"],
    "Previous Month": [0, 0, 0],
    "Enter Now": [0, 0, 0]
})

st.subheader("📊 Enter Inventory")

# ✅ VERY IMPORTANT — ALWAYS VISIBLE
edited_df = st.data_editor(df_table, num_rows="fixed")

# ✅ SUBMIT BUTTON
if st.button("Submit"):

    if not company or not email:
        st.error("❌ Please fill all mandatory fields")

    else:
        try:
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

            # ✅ Create CSV file (safe for cloud)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            df_new.to_csv(temp_file.name, index=False)

            # ✅ READ SECRETS
            SENDER_EMAIL = st.secrets["email"]
            PASSWORD = st.secrets["password"]

            RECEIVERS = [email, SENDER_EMAIL]

            # ✅ CREATE EMAIL
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

            # ✅ Attach CSV
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

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")
``
