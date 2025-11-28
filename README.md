# Hiring Automation Bot 🤖

AI-powered hiring automation tool for screening candidates, matching resumes to job descriptions, and managing the recruitment process.

## ✨ Features

- 📄 **Resume Parsing** - Extract information from PDF and DOCX resumes
- 🔍 **OCR Support** - Parse scanned/image-based PDFs using hybrid local + cloud OCR
- 🎯 **Smart Matching** - AI-powered candidate-JD matching with fit scores
- 📊 **Google Sheets Integration** - Automatic candidate tracking
- 🏢 **Multi-Role Support** - Manage 30+ job positions simultaneously
- 💻 **Web Interface** - User-friendly Streamlit UI
- 📧 **Notifications** - Email and WhatsApp support (optional)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud account (for Sheets API)
- Tesseract OCR (optional, for faster local OCR)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nehaprinto/hiring-bot.git
cd hiring-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Sheets API:
   - Place your `service-account.json` in `credentials/` folder
   - See `GOOGLE_SETUP_GUIDE.md` for detailed instructions

4. Launch the web UI:
```bash
# Windows
RUN_WEB_UI.bat

# Linux/Mac
streamlit run app.py
```

5. Open browser at `http://localhost:8501`

## 📋 Managing Multiple Job Roles

### Simple Setup:

1. Create `.txt` files in the `jd_library/` folder:
```
jd_library/
├── senior_python_developer.txt
├── data_analyst.txt
├── product_manager.txt
└── ... (add as many as you need)
```

2. When screening:
   - Select role from dropdown
   - Upload resumes
   - Process!

The system automatically:
- Detects all JD files
- Generates role IDs
- Tags candidates by role

See [MULTI_ROLE_GUIDE.md](MULTI_ROLE_GUIDE.md) for details.

## 🎯 Workflow

```
1. Add Job Descriptions → jd_library/*.txt files
2. Upload Resumes → PDF/DOCX files
3. Select Role → Choose which position
4. Process → AI matching + OCR
5. Review → Google Sheets
6. Approve → Mark candidates
7. Notify → Send emails/WhatsApp
```

## 📊 OCR Support

**Hybrid OCR System:**
- **Local Tesseract** - Fast (3-5 sec/page), offline
- **Cloud API** - Fallback, works anywhere, 25k free requests/month

**Supports:**
- ✅ Text-based PDFs (instant)
- ✅ Scanned PDFs (OCR)
- ✅ DOCX files

See [OCR_SETUP.md](OCR_SETUP.md) for setup details.

## 🔧 Configuration

### Google Sheets

1. Create Google Cloud project
2. Enable Google Sheets API
3. Create service account
4. Download `service-account.json`
5. Place in `credentials/` folder

See [GOOGLE_SETUP_GUIDE.md](GOOGLE_SETUP_GUIDE.md)

### Email/WhatsApp (Optional)

- Gmail API for email notifications
- Twilio for WhatsApp messages

See documentation for setup.

## 📁 Project Structure

```
hiring-automation-phase1/
├── app.py                      # Main Streamlit web UI
├── src/
│   ├── resume_parser.py        # Resume parsing + OCR
│   ├── jd_matcher.py           # AI matching logic
│   ├── google_sheets_manager.py # Sheets integration
│   ├── email_sender.py         # Email notifications
│   └── whatsapp_sender.py      # WhatsApp notifications
├── jd_library/                 # Job descriptions
├── credentials/                # API credentials (gitignored)
├── resumes/                    # Uploaded resumes (gitignored)
└── docs/                       # Documentation
```

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free):

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets (service account JSON)
5. Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full instructions.

## 📖 Documentation

- [QUICK_START.md](QUICK_START.md) - Get started quickly
- [MULTI_ROLE_GUIDE.md](MULTI_ROLE_GUIDE.md) - Managing multiple positions
- [OCR_SETUP.md](OCR_SETUP.md) - OCR configuration
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Cloud deployment
- [GOOGLE_SETUP_GUIDE.md](GOOGLE_SETUP_GUIDE.md) - Google Sheets setup

## 💡 Use Cases

- **Recruitment Agencies** - Screen hundreds of candidates daily
- **HR Teams** - Manage multiple open positions
- **Startups** - Automate early-stage screening
- **Enterprises** - Scale hiring across departments

## 🔒 Security

- Credentials stored locally (gitignored)
- HTTPS for all API calls
- OCR files deleted after processing
- GDPR compliant

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📄 License

MIT License - see LICENSE file

## 🙏 Credits

Built with:
- Streamlit (Web UI)
- Google Sheets API
- Tesseract OCR
- OCR.space API
- Python

---

**Made with ❤️ for streamlining hiring**
