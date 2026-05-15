import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import tempfile

# TITLE
st.title("📦 Distributor Inventory Submission")

# INPUTS
company = st.text_input("Company Name")
email = st.text_input("Email ID")

# MONTH LOGIC
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

current_month = datetime.now().month
previous_month = months[current_month - 2] if current_month > 1 else "Dec"

st.info(f"Enter Inventory for: {previous_month}")

# SAMPLE SKU MASTER
sku_master = pd.DataFrame({
    "SKU": ["9-ATV07F45/80", "9-ATV08F45/80", "9-ASD-010"],
    "Segment": ["MD_AGA ACCESSORIES", "MD_AGA ACCESSORIES", "MD_CONGENITAL ASD"]
})

# TABLE
df = sku_master.copy()
df["Previous Month"] = [10, 20, 30]
df["Enter Now"] = [0, 0, 0]

st.subheader("Enter Inventory")

edited_df = st.data_editor(df, num_rows="fixed")

# SUBMIT BUTTON
if st.button("Submit"):

    # ✅ VERY SIMPLE VALIDATION (NO BUG)
    if company.strip() == "" or email.strip() == "":
        st.warning("Enter Company and Email properly")
    else:
        try:
            # CREATE DATA
            df_new = edited_df.copy()
            df_new["Company"] = company
            df_new["Email"] = email
            df_new["Month"] = previous_month

            # SAVE CSV TEMP
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            df_new.to_csv(temp.name, index=False)

            # LOAD SECRETS
            sender = st.secrets["email"]
            password = st.secrets["password"]

            # CREATE MAIL
            msg = EmailMessage()
            msg["Subject"] = f"Inventory Submission - {company}"
            msg["From"] = sender
            msg["To"] = f"{email},{sender}"

            msg.set_content("Inventory submitted. File attached.")

            # ATTACH FILE
            with open(temp.name, "rb") as f:
                msg.add_attachment(f.read(), maintype="text",
                                   subtype="csv", filename="Inventory.csv")

            # SEND MAIL
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)

            st.success("✅ Submitted & Email Sent")

        except Exception as e:
            st.error(f"Error: {e}")
