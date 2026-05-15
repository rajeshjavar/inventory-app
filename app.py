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

