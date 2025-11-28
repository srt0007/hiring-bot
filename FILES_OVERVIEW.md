# Complete File Overview - Hiring Automation Phase 1

A comprehensive guide to every file in the project.

---

## 📂 Project Structure

```
hiring-automation-phase1/
├── 📜 Documentation Files (9 files)
├── 🐍 Python Scripts (2 main + 5 modules)
├── 📧 Templates (2 files)
├── 🔑 Credentials (folder)
├── 📁 Data Folders (2 folders)
└── ⚙️ Configuration Files (3 files)
```

---

## 📜 Documentation Files

### [README.md](README.md)
**Purpose:** Main documentation and setup guide
**When to use:** First time setup, comprehensive reference
**Size:** ~400 lines
**Covers:**
- Complete setup instructions for all APIs
- How to use the system
- Google Sheets structure
- Troubleshooting basics
- Customization tips

### [QUICK_START.md](QUICK_START.md)
**Purpose:** Fast setup guide for experienced users
**When to use:** When you want to get started quickly
**Size:** ~150 lines
**Covers:**
- 5-minute setup steps
- Minimum viable setup
- Quick checklist
- Fast troubleshooting

### [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
**Purpose:** Project overview and features list
**When to use:** Understanding what's been built
**Size:** ~400 lines
**Covers:**
- Complete feature list
- File structure explanation
- Code quality highlights
- Phase 1 scope and limitations

### [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
**Purpose:** Step-by-step setup checklist
**When to use:** Following setup process systematically
**Size:** ~300 lines
**Covers:**
- Checkbox-based setup guide
- Verification steps
- Optional vs required setup
- Common issue quick fixes

### [WORKFLOW.md](WORKFLOW.md)
**Purpose:** Visual workflow and data flow diagrams
**When to use:** Understanding how the system works
**Size:** ~250 lines
**Covers:**
- ASCII workflow diagrams
- Detailed step breakdown
- Data flow charts
- Decision points

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
**Purpose:** Comprehensive troubleshooting guide
**When to use:** When something goes wrong
**Size:** ~500 lines
**Covers:**
- Installation issues
- API authentication problems
- Resume parsing errors
- Network issues
- Debugging techniques

### [TEST_DATA_GUIDE.md](TEST_DATA_GUIDE.md)
**Purpose:** Guide for testing with sample data
**When to use:** Before using real candidate data
**Size:** ~300 lines
**Covers:**
- Creating test resumes
- Sample job descriptions
- Expected test results
- Learning exercises

### [FILES_OVERVIEW.md](FILES_OVERVIEW.md)
**Purpose:** This file - complete file reference
**When to use:** Understanding project structure

### [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) *(to be created)*
**Purpose:** Real-world usage scenarios and examples

---

## 🐍 Main Python Scripts

### [ingest_resumes.py](ingest_resumes.py)
**Purpose:** Main script for resume processing
**When to run:** When you have new resumes to process
**What it does:**
1. Validates setup (files, folders, credentials)
2. Parses all resumes in `resumes/` folder
3. Extracts candidate information
4. Matches against JD keywords
5. Calculates fit scores
6. Saves to Google Sheets

**Command:**
```bash
python ingest_resumes.py
```

**Input:**
- Resumes in `resumes/` folder
- JD in `jd_files/job_description.txt`
- Google Sheets credentials

**Output:**
- Google Sheet with candidates
- Console summary
- Sheet URL

**Time:** 2-5 minutes

---

### [send_notifications.py](send_notifications.py)
**Purpose:** Send emails and WhatsApp to approved candidates
**When to run:** After HR approves candidates in Google Sheet
**What it does:**
1. Reads Google Sheet
2. Filters for `hr_approved = 'Yes'`
3. Sends personalized email to each
4. Sends personalized WhatsApp to each
5. Shows success/failure summary

**Command:**
```bash
python send_notifications.py
```

**Input:**
- Google Sheet with approved candidates
- Email template
- WhatsApp template
- Gmail and Twilio credentials

**Output:**
- Sent emails
- Sent WhatsApp messages
- Console summary

**Time:** 1-3 minutes

---

## 🔧 Python Modules (src/ folder)

### [src/google_sheets_manager.py](src/google_sheets_manager.py)
**Purpose:** Google Sheets API integration
**Size:** ~250 lines
**Main class:** `GoogleSheetsManager`

**Key methods:**
- `get_or_create_sheet()` - Create/open spreadsheet
- `setup_candidates_master_sheet()` - Setup worksheet with headers
- `add_candidate()` - Add single candidate
- `add_multiple_candidates()` - Batch add (more efficient)
- `get_approved_candidates()` - Retrieve approved candidates
- `get_sheet_url()` - Get sheet URL

**Used by:** Both main scripts

---

### [src/resume_parser.py](src/resume_parser.py)
**Purpose:** Extract information from resume files
**Size:** ~280 lines
**Main class:** `ResumeParser`

**Key methods:**
- `extract_text_from_pdf()` - Read PDF files
- `extract_text_from_docx()` - Read DOCX files
- `extract_email()` - Find email with regex
- `extract_phone()` - Find and format phone
- `extract_name()` - Guess candidate name
- `extract_location()` - Find location (best effort)
- `parse_resume()` - Main parsing method
- `parse_multiple_resumes()` - Batch process

**Used by:** `ingest_resumes.py`

**Supports:**
- PDF files (via PyPDF2)
- DOCX files (via python-docx)
- International phone numbers

---

### [src/jd_matcher.py](src/jd_matcher.py)
**Purpose:** Match candidates against job description
**Size:** ~300 lines
**Main class:** `JDMatcher`

**Key methods:**
- `load_jd()` - Read JD text file
- `extract_keywords()` - Find skills in JD
- `calculate_match_score()` - Compare resume vs JD
- `get_fit_label()` - Convert score to label
- `generate_screening_comment()` - Create summary
- `evaluate_candidate()` - Complete evaluation

**Used by:** `ingest_resumes.py`

**Features:**
- 70+ built-in technical skills
- Extensible keyword list
- Percentage scoring (0-100%)
- Fit labels (Strong/Good/Moderate/Weak)

---

### [src/email_sender.py](src/email_sender.py)
**Purpose:** Send emails via Gmail API
**Size:** ~180 lines
**Main class:** `EmailSender`

**Key methods:**
- `_authenticate()` - OAuth2 authentication
- `create_message()` - Build email message
- `send_email()` - Send to recipient
- `send_candidate_email()` - Send with template

**Used by:** `send_notifications.py`

**Features:**
- HTML email support
- Template variables
- Token management
- Auto-refresh authentication

---

### [src/whatsapp_sender.py](src/whatsapp_sender.py)
**Purpose:** Send WhatsApp messages via Twilio
**Size:** ~120 lines
**Main class:** `WhatsAppSender`

**Key methods:**
- `send_message()` - Send WhatsApp message
- `send_candidate_message()` - Send with template

**Used by:** `send_notifications.py`

**Features:**
- Twilio API integration
- Template support
- International phone format handling

---

### [src/__init__.py](src/__init__.py)
**Purpose:** Make src a Python package
**Size:** ~20 lines
**Exports:** All main classes for easy import

---

## 📧 Template Files

### [templates/email_template.html](templates/email_template.html)
**Purpose:** HTML email template
**Format:** HTML with inline CSS
**Placeholders:**
- `{candidate_name}` - Replaced with candidate's name
- `{role_name}` - Replaced with job role

**Customizable:** Yes, edit HTML/CSS as needed

**Example usage:**
```html
<p>Dear {candidate_name},</p>
<p>Your application for <strong>{role_name}</strong> has been shortlisted!</p>
```

---

### [templates/whatsapp_template.txt](templates/whatsapp_template.txt)
**Purpose:** WhatsApp message template
**Format:** Plain text
**Placeholders:**
- `{candidate_name}` - Replaced with candidate's name
- `{role_name}` - Replaced with job role

**Customizable:** Yes, but keep under 1600 characters

**Example usage:**
```
Hello {candidate_name}!
Your application for the *{role_name}* position has been shortlisted.
```

---

## 🔑 Credentials Folder

### credentials/
**Purpose:** Store API credentials (not tracked by git)

**Required files:**

#### credentials/service-account.json
**Purpose:** Google Sheets API authentication
**Format:** JSON
**How to get:** Download from Google Cloud Console
**Used by:** `google_sheets_manager.py`

#### credentials/gmail-credentials.json
**Purpose:** Gmail API OAuth2 credentials
**Format:** JSON
**How to get:** Download from Google Cloud Console
**Used by:** `email_sender.py`

#### credentials/token.json
**Purpose:** Gmail API access token (auto-generated)
**Format:** JSON
**How to get:** Created automatically on first Gmail auth
**Used by:** `email_sender.py`

**Security:** All `.json` and `token.json` files are in `.gitignore`

---

## 📁 Data Folders

### resumes/
**Purpose:** Store candidate resume files
**Accepted formats:** PDF, DOCX
**Used by:** `resume_parser.py`

**Example structure:**
```
resumes/
├── john_doe_resume.pdf
├── jane_smith_cv.docx
└── candidate_123.pdf
```

---

### jd_files/
**Purpose:** Store job description files

#### jd_files/job_description.txt
**Purpose:** Job description for current role
**Format:** Plain text
**Used by:** `jd_matcher.py`

**Content should include:**
- Role title
- Required skills
- Preferred skills
- Experience level
- Responsibilities

---

## ⚙️ Configuration Files

### [requirements.txt](requirements.txt)
**Purpose:** Python package dependencies
**Format:** pip requirements format

**Main packages:**
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- gspread (Google Sheets)
- google-auth (Authentication)
- twilio (WhatsApp)
- phonenumbers (Phone formatting)

**Usage:**
```bash
pip install -r requirements.txt
```

---

### [.env.example](.env.example)
**Purpose:** Environment variables template
**Format:** KEY=value pairs

**Variables:**
- `ROLE_ID` - Role identifier
- `ROLE_NAME` - Role name
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_WHATSAPP_FROM` - Twilio WhatsApp number

**Usage:**
1. Copy to `.env`
2. Fill in actual values
3. Never commit `.env` to git

---

### [.gitignore](.gitignore)
**Purpose:** Git ignore rules
**Protects:**
- Credentials (`credentials/*.json`)
- Environment variables (`.env`)
- Tokens (`token.json`)
- Python cache (`__pycache__/`)
- Virtual environments

**Important:** Prevents accidentally committing sensitive data

---

## 📊 File Count Summary

| Type | Count | Examples |
|------|-------|----------|
| Documentation | 9 | README.md, QUICK_START.md |
| Main Scripts | 2 | ingest_resumes.py, send_notifications.py |
| Python Modules | 6 | resume_parser.py, jd_matcher.py |
| Templates | 2 | email_template.html, whatsapp_template.txt |
| Config Files | 3 | requirements.txt, .env.example, .gitignore |
| Sample Data | 1 | job_description.txt |
| **Total** | **23** | **Complete Phase 1 project** |

---

## 🎯 Which Files to Edit?

### ✏️ You SHOULD Edit:

- `jd_files/job_description.txt` - Your actual JD
- `templates/email_template.html` - Customize email
- `templates/whatsapp_template.txt` - Customize WhatsApp
- `.env` - Your credentials (after copying from `.env.example`)

### 🔒 You SHOULD NOT Edit (unless you know what you're doing):

- `src/*.py` - Core modules
- `ingest_resumes.py` - Main script
- `send_notifications.py` - Main script
- `.gitignore` - Git rules

### 📝 You MAY Edit (advanced):

- `src/jd_matcher.py` - Add custom skills to `common_skills` list
- `src/resume_parser.py` - Add custom extraction patterns

---

## 🔍 Quick File Finder

**Need to...**

| Task | File to Check |
|------|---------------|
| Understand setup | README.md |
| Quick start guide | QUICK_START.md |
| See what's built | PROJECT_SUMMARY.md |
| Follow setup steps | SETUP_CHECKLIST.md |
| Understand workflow | WORKFLOW.md |
| Fix an issue | TROUBLESHOOTING.md |
| Test the system | TEST_DATA_GUIDE.md |
| Process resumes | Run `ingest_resumes.py` |
| Send notifications | Run `send_notifications.py` |
| Change email content | Edit `templates/email_template.html` |
| Change WhatsApp text | Edit `templates/whatsapp_template.txt` |
| Update job description | Edit `jd_files/job_description.txt` |
| Add custom skills | Edit `src/jd_matcher.py` |

---

## 📂 File Access Permissions

**Read-only (don't modify):**
- All `.py` modules
- Documentation files
- `.gitignore`

**Read-write (customize as needed):**
- Templates
- JD files
- `.env`

**Auto-generated (don't edit manually):**
- `credentials/token.json`
- `__pycache__/`

---

**Complete file reference for Phase 1!** All files are documented and ready to use.
