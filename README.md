# 📧 Bulk Email Sender

A secure and user-friendly Streamlit web app for authenticated bulk email sending via Gmail. This tool includes support for attachments, personalized greetings, AI-powered email summarization using Google Gemini, and robust email validation.

---

## 🚀 Features

- **Secure Multi-Step Authentication** (App-level and Gmail App Password)
- **Bulk Email Support** via CSV or Excel uploads
- **Personalized Greetings** using recipient names
- **File Attachments** (up to 25MB total)
- **AI-Powered Email Summarizer** with Google Gemini
- **Email Validation** before sending
- **Progress Tracking** with real-time feedback
- **Downloadable Failure Report**

---

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) — Interactive UI
- [LangChain + Google Gemini](https://python.langchain.com/docs/integrations/chat/google_generative_ai/) — AI-powered summarization
- [smtplib, email, pandas] — Email handling and data processing
- [dotenv] — Secure environment variable management
- [email-validator] — Email format validation

---

## 🔐 Security Notice

This app uses:
- A hardcoded **BASMAH app password** (`BASMAH@786`) for access (should be stored securely in a production setting).
- **Gmail App Passwords** for sending emails (regular Gmail passwords won't work).

> ⚠️ Do NOT expose your Gmail or app credentials publicly.

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/basmah-email-sender.git
cd basmah-email-sender
```

2. **Create a virtual environment and activate it**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up your `.env` file**

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## 🧪 Usage

1. Run the app:

```bash
streamlit run app.py
```

2. Follow the UI to:
   - Authenticate using the BASMAH password
   - Enter Gmail & App Password
   - Upload a CSV/XLSX file with columns: `EMAIL`, `NAME`
   - Compose email and add optional attachments
   - Click "Send Emails"

---

## 📁 Example Input File

| EMAIL              | NAME        |
|--------------------|-------------|
| john@example.com   | John Doe    |
| jane@example.com   | Jane Smith  |

---

## 🤖 AI Summarizer

Use the "Summarize Email Body" button to get a professionally rewritten version of your message body using **Google Gemini**.

---

## 📤 Screenshots



![email_3](https://github.com/user-attachments/assets/0649654b-635b-431d-ad32-e177d7ad59a9)

![email_4](https://github.com/user-attachments/assets/c83af1c6-2070-40d3-9024-50b0a6f43057)

![email_5](https://github.com/user-attachments/assets/5c71a206-aacc-4ffd-b4c4-273b31f21130)

![email_6](https://github.com/user-attachments/assets/bbc4211b-bf72-4f20-85e1-f57abb06048f)

![summary_1](https://github.com/user-attachments/assets/eca2db7d-8729-4b70-a2a9-640a29fb7109)

![summary_2](https://github.com/user-attachments/assets/9e10a05c-f520-49ad-acd4-8832a2de29fa)




---


---

## 🙋‍♀️ Contributions

Feel free to fork and submit pull requests. Suggestions and bug reports are welcome via issues.

---

## 📬 Contact

For issues or enhancements, please open an [Issue](https://github.com/yourusername/basmah-email-sender/issues) or contact the maintainer.
