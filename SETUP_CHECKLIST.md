# Setup Checklist - Hiring Automation Phase 1

Use this checklist to ensure you've completed all setup steps correctly.

## ✅ Pre-Requirements

- [ ] Python 3.8 or higher installed
  - Check with: `python --version`

- [ ] pip (Python package manager) installed
  - Check with: `pip --version`

## ✅ Step 1: Install Python Dependencies

- [ ] Navigate to project folder
  ```bash
  cd hiring-automation-phase1
  ```

- [ ] Install required packages
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify installation (no errors)

## ✅ Step 2: Google Sheets API Setup

- [ ] Create Google Cloud Project
  - Go to: https://console.cloud.google.com/

- [ ] Enable APIs:
  - [ ] Google Sheets API
  - [ ] Google Drive API

- [ ] Create Service Account
  - [ ] Go to "APIs & Services" → "Credentials"
  - [ ] Click "Create Credentials" → "Service Account"
  - [ ] Fill in details and create

- [ ] Download Service Account Key
  - [ ] Click on service account
  - [ ] Go to "Keys" tab
  - [ ] Create new key (JSON format)
  - [ ] Save as: `credentials/service-account.json`

- [ ] Verify file exists:
  ```bash
  ls credentials/service-account.json
  ```

## ✅ Step 3: Prepare Resume Data

- [ ] Add resume files to `resumes/` folder
  - [ ] Supported formats: PDF, DOCX
  - [ ] At least 1 resume file added

- [ ] Edit job description
  - [ ] Open `jd_files/job_description.txt`
  - [ ] Replace with actual job description
  - [ ] Include key skills and requirements

## ✅ Step 4: Test Resume Ingestion

- [ ] Run the ingestion script:
  ```bash
  python ingest_resumes.py
  ```

- [ ] Check for success messages
  - [ ] "✓ Found X resume(s)"
  - [ ] "✓ Total resumes processed: X"
  - [ ] Google Sheet URL displayed

- [ ] Open Google Sheet URL
  - [ ] Verify Candidates_Master sheet exists
  - [ ] Check that candidate data is populated
  - [ ] Verify all columns are present

**🎉 Core functionality is working! You can stop here if you don't need email/WhatsApp.**

---

## ✅ Step 5: Gmail API Setup (Optional)

- [ ] Enable Gmail API in Google Cloud
  - [ ] Go to "APIs & Services" → "Library"
  - [ ] Search "Gmail API" and enable

- [ ] Create OAuth 2.0 Credentials
  - [ ] Go to "Credentials" → "Create Credentials"
  - [ ] Choose "OAuth client ID"
  - [ ] Application type: "Desktop app"
  - [ ] Download JSON file

- [ ] Save credentials
  - [ ] Rename downloaded file to: `gmail-credentials.json`
  - [ ] Move to: `credentials/gmail-credentials.json`

- [ ] Verify file exists:
  ```bash
  ls credentials/gmail-credentials.json
  ```

## ✅ Step 6: Twilio Setup (Optional)

- [ ] Create Twilio account
  - [ ] Go to: https://www.twilio.com/
  - [ ] Sign up (free trial available)

- [ ] Get Twilio credentials
  - [ ] Note your Account SID
  - [ ] Note your Auth Token
  - [ ] From Twilio Console dashboard

- [ ] Enable WhatsApp Sandbox
  - [ ] Go to "Messaging" → "Try it out"
  - [ ] Follow WhatsApp sandbox setup
  - [ ] Note the WhatsApp number (e.g., `whatsapp:+14155238886`)

- [ ] Create `.env` file
  - [ ] Copy `.env.example` to `.env`
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file with your credentials:
  ```
  ROLE_ID=ROLE001
  ROLE_NAME=Your Role Name
  TWILIO_ACCOUNT_SID=your_account_sid_here
  TWILIO_AUTH_TOKEN=your_auth_token_here
  TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
  ```

## ✅ Step 7: Customize Templates (Optional)

- [ ] Customize email template
  - [ ] Edit `templates/email_template.html`
  - [ ] Keep placeholders: `{candidate_name}`, `{role_name}`

- [ ] Customize WhatsApp template
  - [ ] Edit `templates/whatsapp_template.txt`
  - [ ] Keep placeholders: `{candidate_name}`, `{role_name}`
  - [ ] Keep under 1600 characters

## ✅ Step 8: HR Approval Workflow

- [ ] Open Google Sheet (URL from Step 4)

- [ ] Review candidate information
  - [ ] Check auto_fit_score
  - [ ] Check auto_fit_label
  - [ ] Read auto_screen_comment

- [ ] Approve candidates
  - [ ] Change `hr_approved` from "No" to "Yes"
  - [ ] For each candidate you want to contact

- [ ] Save the sheet (auto-saves in Google Sheets)

## ✅ Step 9: Test Notifications

- [ ] Run notification script:
  ```bash
  python send_notifications.py
  ```

- [ ] Check for success messages
  - [ ] "✓ Found X approved candidate(s)"
  - [ ] "✓ Email sent to [email]"
  - [ ] "✓ WhatsApp message sent to [phone]"

- [ ] Verify delivery
  - [ ] Check candidate email inbox
  - [ ] Check candidate WhatsApp
  - [ ] Verify template was populated correctly

## ✅ Final Verification

- [ ] Complete end-to-end test:
  1. [ ] Add a test resume
  2. [ ] Run `python ingest_resumes.py`
  3. [ ] Open Google Sheet
  4. [ ] Approve a candidate
  5. [ ] Run `python send_notifications.py`
  6. [ ] Verify email/WhatsApp received

- [ ] Clean up test data if needed

## 🎉 Setup Complete!

All checkboxes marked? You're ready to use the hiring automation tool!

---

## 🆘 Common Issues

### Issue: "pip: command not found"
**Solution:** Install pip or use `python -m pip install -r requirements.txt`

### Issue: "ModuleNotFoundError"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: "Credentials not found"
**Solution:** Check that JSON files are in the `credentials/` folder with exact names

### Issue: "No resumes found"
**Solution:** Add PDF or DOCX files to `resumes/` folder

### Issue: "Gmail authentication failed"
**Solution:**
- Make sure you created OAuth credentials (not API key)
- Delete `credentials/token.json` and try again
- Check Gmail API is enabled

### Issue: "Twilio authentication failed"
**Solution:**
- Verify credentials in `.env` file
- Make sure you joined WhatsApp sandbox
- Check phone numbers include country code with `+`

---

## 📚 Need More Help?

- **Setup Guide:** See [README.md](README.md)
- **Quick Start:** See [QUICK_START.md](QUICK_START.md)
- **Project Info:** See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**Ready to start?** Mark all checkboxes and run `python ingest_resumes.py`
