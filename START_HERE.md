# 🚀 START HERE - Hiring Automation Phase 1

**Welcome! This is your starting point.**

---

## ✅ What You Have

A complete **Hiring Automation Tool (Phase 1)** that:

1. ✅ Parses resumes (PDF/DOCX)
2. ✅ Extracts candidate info (name, email, phone, location)
3. ✅ Matches candidates to job description
4. ✅ Saves everything to Google Sheets
5. ✅ Sends emails (Gmail API)
6. ✅ Sends WhatsApp messages (Twilio)

**All code is clean, commented, and beginner-friendly!**

---

## 📖 Read This First (5 Minutes)

### New to the project? Start here:

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ← Read this to understand what's been built
2. **[QUICK_START.md](QUICK_START.md)** ← Fast setup guide (5-minute setup)
3. **[README.md](README.md)** ← Complete documentation (detailed setup)

### Already familiar? Jump to:

- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** ← Follow step-by-step setup
- **[WORKFLOW.md](WORKFLOW.md)** ← Understand how it works
- **[TEST_DATA_GUIDE.md](TEST_DATA_GUIDE.md)** ← Test before going live

---

## 🎯 Quick Setup (15 Minutes)

### Step 1: Install Python Dependencies (2 min)

```bash
cd hiring-automation-phase1
pip install -r requirements.txt
```

### Step 2: Set Up Google Sheets API (5 min)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable "Google Sheets API" and "Google Drive API"
3. Create Service Account → Download credentials
4. Save as `credentials/service-account.json`

**Detailed instructions:** [README.md - Step 3](README.md#step-3-set-up-google-sheets-api)

### Step 3: Prepare Your Data (3 min)

```bash
# Add your resume files (PDF or DOCX)
# Place them in: resumes/

# Edit your job description
# File: jd_files/job_description.txt
```

### Step 4: Run It! (1 min)

```bash
python ingest_resumes.py
```

**Output:** Google Sheet URL with all candidates!

### Step 5: Approve Candidates (Manual)

1. Open the Google Sheet (URL from Step 4)
2. Change `hr_approved` from "No" to "Yes" for candidates you want to contact

### Step 6: Set Up Email/WhatsApp (Optional - 5 min)

**For Email:**
- [README.md - Step 4](README.md#step-4-set-up-gmail-api-for-email-sending)

**For WhatsApp:**
- [README.md - Step 5](README.md#step-5-set-up-twilio-for-whatsapp)

### Step 7: Send Notifications (1 min)

```bash
python send_notifications.py
```

**Done!** Emails and WhatsApp messages sent!

---

## 📁 Project Structure (Simple View)

```
hiring-automation-phase1/
│
├── 📖 START_HERE.md              ← You are here!
├── 📖 README.md                   ← Full documentation
├── 📖 QUICK_START.md              ← Fast setup
│
├── 🐍 ingest_resumes.py          ← RUN THIS: Process resumes
├── 🐍 send_notifications.py      ← RUN THIS: Send emails/WhatsApp
│
├── src/                          ← Core code (don't touch)
│   ├── resume_parser.py
│   ├── jd_matcher.py
│   ├── google_sheets_manager.py
│   ├── email_sender.py
│   └── whatsapp_sender.py
│
├── resumes/                      ← PUT RESUMES HERE
├── jd_files/
│   └── job_description.txt       ← EDIT THIS: Your JD
│
├── templates/
│   ├── email_template.html       ← EDIT THIS: Email content
│   └── whatsapp_template.txt     ← EDIT THIS: WhatsApp content
│
├── credentials/                  ← PUT API CREDENTIALS HERE
│   ├── service-account.json      (Google Sheets)
│   ├── gmail-credentials.json    (Gmail API)
│   └── token.json                (Auto-generated)
│
└── .env                          ← EDIT THIS: Twilio credentials
```

---

## 🎓 Learning Path

### Total Beginner?

1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) to understand the system
2. Follow [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) step by step
3. Use [TEST_DATA_GUIDE.md](TEST_DATA_GUIDE.md) to test with sample data
4. Then use real resumes!

### Some Experience?

1. Skim [QUICK_START.md](QUICK_START.md)
2. Set up Google Sheets API
3. Run `python ingest_resumes.py`
4. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if issues arise

### Advanced User?

1. Check [FILES_OVERVIEW.md](FILES_OVERVIEW.md) to understand structure
2. Review code in `src/` folder
3. Customize as needed!

---

## 🆘 Having Issues?

### Common Problems:

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| "Credentials not found" | Check files in `credentials/` folder |
| "No resumes found" | Add PDF/DOCX files to `resumes/` |
| "Cannot parse resume" | Make sure PDF has selectable text |
| Gmail auth fails | Re-download OAuth credentials |
| Twilio auth fails | Check `.env` file credentials |

**Full troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 All Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [START_HERE.md](START_HERE.md) | Quick orientation | First time (now!) |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | What's been built | Understanding scope |
| [QUICK_START.md](QUICK_START.md) | Fast setup | Quick start |
| [README.md](README.md) | Complete guide | Detailed setup |
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | Step-by-step | Systematic setup |
| [WORKFLOW.md](WORKFLOW.md) | How it works | Understanding flow |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Fix issues | When stuck |
| [TEST_DATA_GUIDE.md](TEST_DATA_GUIDE.md) | Testing | Before going live |
| [FILES_OVERVIEW.md](FILES_OVERVIEW.md) | File reference | Understanding structure |

---

## ✅ Phase 1 Checklist

Use this to track your progress:

- [ ] Read START_HERE.md (you're doing it!)
- [ ] Read PROJECT_SUMMARY.md
- [ ] Install Python dependencies
- [ ] Set up Google Sheets API
- [ ] Add test resumes
- [ ] Edit job description
- [ ] Run `python ingest_resumes.py`
- [ ] Check Google Sheet
- [ ] Approve test candidates
- [ ] Set up Gmail API (optional)
- [ ] Set up Twilio (optional)
- [ ] Run `python send_notifications.py`
- [ ] Test with real data
- [ ] Customize templates
- [ ] Ready for production!

---

## 🎯 Two Ways to Get Started

### Option A: Minimum Setup (Just Resume Processing)

**Time:** 10 minutes

**What you get:**
- Resume parsing
- JD matching
- Google Sheets with candidate data

**What you need:**
1. Python dependencies (`pip install -r requirements.txt`)
2. Google Sheets credentials
3. Resumes
4. Job description

**Then run:** `python ingest_resumes.py`

**Good for:** Testing, understanding the system, HR review workflow

---

### Option B: Full Setup (Including Notifications)

**Time:** 20 minutes

**What you get:**
- Everything from Option A
- Email notifications
- WhatsApp notifications

**What you need:**
1. Everything from Option A
2. Gmail API credentials
3. Twilio account and credentials

**Then run:** `python send_notifications.py`

**Good for:** Complete automated workflow

---

## 🚀 Ready to Start?

### Your First Run (Test Mode):

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Sheets API** (see README.md Step 3)

3. **Create a test resume** (see TEST_DATA_GUIDE.md)

4. **Run the script:**
   ```bash
   python ingest_resumes.py
   ```

5. **Check the Google Sheet!**

### Next Steps:

- [ ] Test with more resumes
- [ ] Set up email notifications
- [ ] Set up WhatsApp notifications
- [ ] Customize templates
- [ ] Use with real candidates

---

## 💡 Tips for Success

1. **Test first!** Use sample data before real candidates
2. **Read error messages** - they usually explain what's wrong
3. **Check file paths** - most issues are wrong file locations
4. **Verify credentials** - API setup is critical
5. **Start simple** - Get resume processing working first, then add notifications

---

## 🎉 What's Next After Phase 1?

Phase 1 is complete and working! Future phases could include:

- **Phase 2:** Web UI (Streamlit), recruiter portal, portal integrations
- **Phase 3:** Analytics, reporting, candidate status tracking, interview scheduling

**But Phase 1 is fully functional and ready to use now!**

---

## 📧 Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Process resumes
python ingest_resumes.py

# Send notifications to approved candidates
python send_notifications.py

# Test a module individually
cd src
python resume_parser.py
```

---

## 🎓 Understanding the System in 3 Minutes

1. **You add resumes** → Folder: `resumes/`
2. **Script processes them** → Run: `ingest_resumes.py`
3. **Data goes to Google Sheet** → Automatic
4. **HR reviews and approves** → Manual (change "No" to "Yes")
5. **Script sends notifications** → Run: `send_notifications.py`
6. **Candidates receive emails/WhatsApp** → Automatic

**That's it!** Simple, clean, and effective.

---

## 🌟 You're All Set!

You now have:
✅ Complete working system
✅ Comprehensive documentation
✅ Test data guide
✅ Troubleshooting help
✅ Everything you need for Phase 1

**Next step:** Follow [QUICK_START.md](QUICK_START.md) or [README.md](README.md) to begin setup!

---

**Questions? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [README.md](README.md)**

**Ready to code?** Start with: `python ingest_resumes.py`

Good luck! 🚀
