# Hiring Automation - Phase 1 Workflow

## 🔄 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       PHASE 1: WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  STEP 1: RESUME INGESTION (Automated)                         │
│  Script: ingest_resumes.py                                     │
└────────────────────────────────────────────────────────────────┘

    📁 resumes/                     📄 jd_files/job_description.txt
    ├── resume1.pdf                       │
    ├── resume2.docx                      │
    └── resume3.pdf                       │
           │                               │
           ↓                               ↓
    ┌─────────────────┐          ┌─────────────────┐
    │ Resume Parser   │          │  JD Matcher     │
    │ (PDF/DOCX)      │          │ (Keywords)      │
    └────────┬────────┘          └────────┬────────┘
             │                            │
             │  Extract:                  │  Extract:
             │  • Name                    │  • Skills
             │  • Email                   │  • Experience
             │  • Phone                   │  • Requirements
             │  • Location                │
             │                            │
             └────────────┬───────────────┘
                          │
                          ↓
                 ┌────────────────┐
                 │ Match & Score  │
                 │ Calculate Fit  │
                 └────────┬───────┘
                          │
                          ↓
              ┌───────────────────────┐
              │  Google Sheets API    │
              │  Save to Sheet:       │
              │  "Candidates_Master"  │
              └───────────┬───────────┘
                          │
                          ↓
         ┌────────────────────────────────────────┐
         │  📊 GOOGLE SHEET CREATED               │
         │  ✓ Candidate info                      │
         │  ✓ Fit scores                          │
         │  ✓ Match comments                      │
         │  ✓ hr_approved = "No" (default)        │
         └────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  STEP 2: HR MANUAL APPROVAL (Manual)                          │
│  Tool: Google Sheets (Browser)                                │
└────────────────────────────────────────────────────────────────┘

         📊 Open Google Sheet
              │
              ↓
         ┌─────────────────────────────────┐
         │  Review Candidates               │
         │  • Check auto_fit_score          │
         │  • Read auto_screen_comment      │
         │  • Review candidate details      │
         └─────────────────────────────────┘
              │
              ↓
         ┌─────────────────────────────────┐
         │  Make Decision                   │
         │  Change "hr_approved":           │
         │  • "No" → "Yes" (approve)        │
         │  • Keep "No" (reject)            │
         └─────────────────────────────────┘
              │
              ↓
         ┌─────────────────────────────────┐
         │  Save Sheet                      │
         │  (Auto-saves in Google Sheets)   │
         └─────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  STEP 3: SEND NOTIFICATIONS (Automated)                       │
│  Script: send_notifications.py                                │
└────────────────────────────────────────────────────────────────┘

         📊 Google Sheet
         (hr_approved = "Yes")
              │
              ↓
    ┌──────────────────────┐
    │  Filter Approved     │
    │  Candidates          │
    └──────────┬───────────┘
               │
               ↓
    ┌─────────────────────────────────┐
    │  For each approved candidate:   │
    └─────────────────────────────────┘
               │
               ├─────────────────┬─────────────────┐
               ↓                 ↓                 ↓
    ┌──────────────────┐  ┌────────────────┐  ┌──────────────┐
    │  Load Templates  │  │  Gmail API     │  │  Twilio API  │
    │  • email.html    │  │  Send Email    │  │  Send        │
    │  • whatsapp.txt  │  │                │  │  WhatsApp    │
    └──────────────────┘  └────────────────┘  └──────────────┘
               │                 │                      │
               └─────────────────┴──────────────────────┘
                                 │
                                 ↓
                    ┌────────────────────────┐
                    │  Candidate Receives:   │
                    │  📧 Email              │
                    │  📱 WhatsApp Message   │
                    └────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  ✅ PROCESS COMPLETE                                           │
│  All approved candidates have been notified!                   │
└────────────────────────────────────────────────────────────────┘
```

---

## 📝 Detailed Step Breakdown

### Step 1: Resume Ingestion (Automated)

**Input:**
- Multiple resume files (PDF/DOCX) in `resumes/` folder
- Job description text file in `jd_files/`

**Process:**
1. `ResumeParser` reads each resume file
2. Extracts candidate information using regex patterns
3. `JDMatcher` loads job description
4. Extracts keywords from JD
5. Matches resume text against JD keywords
6. Calculates fit score (0-100%)
7. Generates fit label and screening comment
8. `GoogleSheetsManager` creates/opens Google Sheet
9. Adds all candidates to "Candidates_Master" sheet

**Output:**
- Google Sheet with candidate data
- All candidates have `hr_approved = "No"` by default
- Console shows summary and Google Sheet URL

**Time:** ~2-5 minutes (depending on number of resumes)

---

### Step 2: HR Manual Approval (Manual)

**Input:**
- Google Sheet URL (from Step 1)
- HR judgment and decision-making

**Process:**
1. HR opens Google Sheet in browser
2. Reviews candidate information:
   - Reads `auto_fit_score` (percentage match)
   - Reads `auto_fit_label` (Strong/Good/Moderate/Weak Fit)
   - Reads `auto_screen_comment` (matched/missing skills)
   - Checks candidate contact info
3. Makes approval decision for each candidate
4. Changes `hr_approved` column:
   - From "No" to "Yes" for approved candidates
   - Keeps "No" for rejected candidates
5. Sheet auto-saves

**Output:**
- Updated Google Sheet with approved candidates marked "Yes"

**Time:** Varies (5-30 minutes depending on number of candidates)

---

### Step 3: Send Notifications (Automated)

**Input:**
- Google Sheet with approved candidates (`hr_approved = "Yes"`)
- Email template (`templates/email_template.html`)
- WhatsApp template (`templates/whatsapp_template.txt`)

**Process:**
1. `GoogleSheetsManager` retrieves all records
2. Filters for `hr_approved = "Yes"`
3. For each approved candidate:
   - `EmailSender` loads email template
   - Replaces placeholders with candidate data
   - Sends email via Gmail API
   - `WhatsAppSender` loads WhatsApp template
   - Replaces placeholders with candidate data
   - Sends message via Twilio API
4. Logs success/failure for each notification

**Output:**
- Emails sent to approved candidates
- WhatsApp messages sent to approved candidates
- Console shows summary of sent notifications

**Time:** ~1-3 minutes (depending on number of approved candidates)

---

## 🔁 Iterative Workflow (Multiple Batches)

You can run this workflow multiple times for different batches:

```
Batch 1:
  Add resumes → Run ingest_resumes.py → Approve → Send notifications

Batch 2 (different role):
  Update JD → Add new resumes → Run ingest_resumes.py → Approve → Send notifications

Batch 3 (same role):
  Add more resumes → Run ingest_resumes.py → Approve → Send notifications
```

**Note:** All batches append to the same Google Sheet (Candidates_Master)

---

## 📊 Data Flow

```
Resume Files (PDF/DOCX)
    ↓
Text Extraction
    ↓
Information Parsing (name, email, phone, location)
    ↓
JD Keyword Matching
    ↓
Fit Score Calculation
    ↓
Google Sheets Storage
    ↓
HR Review & Approval (Manual)
    ↓
Notification Trigger
    ↓
Email + WhatsApp Delivery
```

---

## 🎯 Key Decision Points

### 1. Which resumes to process?
**Decision Maker:** You (before running script)
**Action:** Place selected resumes in `resumes/` folder

### 2. What job description to use?
**Decision Maker:** You (before running script)
**Action:** Edit `jd_files/job_description.txt`

### 3. Which candidates to approve?
**Decision Maker:** HR (manual review)
**Action:** Change `hr_approved` to "Yes" in Google Sheet

### 4. What message to send?
**Decision Maker:** You (before running script)
**Action:** Edit templates in `templates/` folder

---

## ⚡ Quick Reference

| Stage | Script | Duration | Manual/Auto |
|-------|--------|----------|-------------|
| Resume Processing | `ingest_resumes.py` | 2-5 min | Automated |
| HR Approval | Google Sheets | 5-30 min | Manual |
| Send Notifications | `send_notifications.py` | 1-3 min | Automated |

---

## 🔄 Phase 1 Limitations

**What's NOT automated:**
- HR approval decision (by design - requires human judgment)
- Interview scheduling
- Follow-up communications
- Status tracking after notification

**Coming in Phase 2 & 3!**

---

**Need help?** See [README.md](README.md) for detailed instructions.
