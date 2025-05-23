import streamlit as st
import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import time
import random
from email_validator import validate_email, EmailNotValidError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BASMAH_PASSWORD = "BASMAH@786"  # Replace with your actual password

# Initialize Gemini Model
model = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05")

# Email Summarization Prompt Template
email_summary_template = PromptTemplate(
    template="Summarize this email body: {email_body}",
    input_variables=["email_body"]
)

# Helpers
def add_signature(body, signature):
    return body + "\n\nWarm Regards,\n" + signature

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def authenticate_email(sender_email, sender_password):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        return True
    except:
        return False

def send_emails(sender_email, sender_password, subject, body, signature, file, attachments):
    failed_emails = []
    successful_emails = []

    if file is not None:
        df = pd.read_excel(file, engine='openpyxl') if file.name.endswith('.xlsx') else pd.read_csv(file)

        df.columns = [col.upper() for col in df.columns]
        df = df[['EMAIL', 'NAME']]

        if 'EMAIL' not in df.columns or 'NAME' not in df.columns:
            st.error("Error: The file must contain 'EMAIL' and 'NAME' columns.")
            return [], []

        st.session_state["send_button_disabled"] = True

        for _, row in df.iterrows():
            email = row['EMAIL']
            name_parts = row['NAME'].split()
            last_name = name_parts[-1] if name_parts else ""

            if not is_valid_email(email):
                st.write(f"❌ Failed to send email to {row['NAME']}: Invalid email.")
                failed_emails.append(row)
                continue

            final_body = f"Hello {last_name},\n\n" + add_signature(body, signature)
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(final_body, "plain"))

            for file in attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.getvalue())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={file.name}")
                msg.attach(part)

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
                server.quit()
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.write(f"✅ Email sent to {row['NAME']} at {timestamp}")
                successful_emails.append(row['EMAIL'])
                time.sleep(random.randint(3, 7))
            except Exception as e:
                st.write(f"❌ Failed to send email to {row['NAME']}: {str(e)}")
                failed_emails.append(row)

        st.session_state["send_button_disabled"] = False

    return failed_emails, successful_emails

# Streamlit App
st.title("BASMAH Email Sender")

# Session State
if "authenticated_basmah" not in st.session_state:
    st.session_state["authenticated_basmah"] = False
if "authenticated_email" not in st.session_state:
    st.session_state["authenticated_email"] = False
if "send_emails_triggered" not in st.session_state:
    st.session_state["send_emails_triggered"] = False
if "send_button_disabled" not in st.session_state:
    st.session_state["send_button_disabled"] = False
if "sender_email" not in st.session_state:
    st.session_state["sender_email"] = ""
if "sender_password" not in st.session_state:
    st.session_state["sender_password"] = ""

# Step 1: BASMAH authentication
if not st.session_state["authenticated_basmah"]:
    basmah_pass = st.text_input("Enter BASMAH Password", type="password")
    if st.button("Verify BASMAH Access"):
        if basmah_pass == BASMAH_PASSWORD:
            st.session_state["authenticated_basmah"] = True
            st.success("BASMAH access granted. Proceed to Gmail authentication.")
            st.rerun()
        else:
            st.error("Incorrect BASMAH password.")
    st.stop()

# Step 2: Gmail authentication
if not st.session_state["authenticated_email"]:
    sender_email = st.text_input("Enter your Gmail address")
    sender_password = st.text_input("Enter your App Password", type="password")
    if st.button("Verify Gmail"):
        if authenticate_email(sender_email, sender_password):
            st.session_state["authenticated_email"] = True
            st.session_state["sender_email"] = sender_email
            st.session_state["sender_password"] = sender_password
            st.success("Gmail verified successfully.")
            st.rerun()
        else:
            st.error("Invalid Gmail or App Password.")
    st.stop()

# Step 3: Email Sending Interface
file = st.file_uploader("Upload Excel/CSV file with emails", type=["csv", "xlsx", "ods"], help="Required")
subject = st.text_input("Subject", help="Required")
body = st.text_area("Email Body", help="Required")
with st.expander("📋 Summarize Email Body", expanded=False):
    if st.button("Summarize Email Body"):
        if not body.strip():
            st.warning("Please write something in the body first.")
        else:
            with st.spinner("Summarizing email body..."):
                summary_prompt = "Please paraphrase professionally this email body (Please don't share Dear [name], and signature message like warm regards. Focus only on paraphasing the email body: " + body
                summary_response = model.invoke(summary_prompt)
                st.success("Summary generated below")
                st.markdown(f"**Summary:**\n\n{summary_response.content}")

signature = st.text_area("Signature", help="Required")
attachments = st.file_uploader("Attach files (Max: 25MB total)", accept_multiple_files=True)

# Email Summarizer Feature


if st.button("Send Emails", disabled=st.session_state["send_button_disabled"]):
    if not file or not subject or not body or not signature:
        st.error("Please fill in all required fields.")
    else:
        st.session_state["send_button_disabled"] = True
        st.session_state["send_emails_triggered"] = True
        st.rerun()

if st.session_state["send_emails_triggered"]:
    failed_emails, successful_emails = send_emails(
        st.session_state["sender_email"],
        st.session_state["sender_password"],
        subject,
        body,
        signature,
        file,
        attachments
    )

    if failed_emails:
        failed_df = pd.DataFrame(failed_emails)
        failed_df.to_excel("failed_report.xlsx", index=False)
        with open("failed_report.xlsx", "rb") as f:
            st.download_button("Download Failed Report", f, "failed_report.xlsx")
    else:
        st.success("✅ All emails sent successfully!")

    st.session_state["send_emails_triggered"] = False
    st.session_state["send_button_disabled"] = False
