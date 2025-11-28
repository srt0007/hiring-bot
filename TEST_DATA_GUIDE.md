# Test Data Guide - Quick Testing

Want to test the system without real resumes? Here's how to create test data.

---

## 🧪 Quick Test Setup (5 Minutes)

### Option 1: Use Sample Text Resume

Create a simple test resume in DOCX format:

1. Open Microsoft Word or Google Docs
2. Copy this sample content:

```
JOHN DOE
john.doe@example.com | +1-555-123-4567 | New York, NY

PROFESSIONAL SUMMARY
Senior Python Developer with 5+ years of experience in building scalable web applications.
Strong background in Django, Flask, and RESTful API development.

SKILLS
- Programming: Python, JavaScript, SQL
- Frameworks: Django, Flask, FastAPI, React
- Databases: PostgreSQL, MySQL, MongoDB
- Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
- Tools: Git, Jenkins, CI/CD
- Other: REST API, Microservices, Agile, Scrum

EXPERIENCE
Senior Python Developer | Tech Company | 2020 - Present
- Developed RESTful APIs using Django and Flask
- Implemented microservices architecture with Docker
- Deployed applications on AWS cloud platform
- Collaborated with cross-functional teams using Agile methodology

Python Developer | Another Company | 2018 - 2020
- Built web applications using Django framework
- Worked with PostgreSQL databases
- Participated in code reviews and unit testing
- Strong problem-solving and communication skills

EDUCATION
Bachelor of Science in Computer Science | University Name | 2018
```

3. Save as `resumes/john_doe.docx`

4. Create 2-3 more similar files with different names and emails

---

### Option 2: Create Multiple Test Resumes Quickly

Use this Python script to generate test DOCX files:

```python
# create_test_resumes.py
from docx import Document

test_candidates = [
    {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1-555-123-4567',
        'location': 'New York, NY',
        'skills': 'Python, Django, Flask, PostgreSQL, AWS, Docker, Git, REST API'
    },
    {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'phone': '+1-555-234-5678',
        'location': 'San Francisco, CA',
        'skills': 'Python, FastAPI, MongoDB, React, Kubernetes, CI/CD, Microservices'
    },
    {
        'name': 'Bob Johnson',
        'email': 'bob.johnson@example.com',
        'phone': '+1-555-345-6789',
        'location': 'Austin, TX',
        'skills': 'Python, Flask, MySQL, JavaScript, Agile, Problem Solving'
    }
]

for candidate in test_candidates:
    doc = Document()
    doc.add_heading(candidate['name'], 0)
    doc.add_paragraph(f"{candidate['email']} | {candidate['phone']} | {candidate['location']}")
    doc.add_heading('Skills', level=1)
    doc.add_paragraph(candidate['skills'])
    doc.add_heading('Experience', level=1)
    doc.add_paragraph(f"Python Developer with expertise in {candidate['skills'].split(',')[0]}")

    filename = f"resumes/{candidate['name'].lower().replace(' ', '_')}.docx"
    doc.save(filename)
    print(f"Created: {filename}")

print("\n✓ Test resumes created!")
```

Run it:
```bash
python create_test_resumes.py
```

---

## 📝 Sample Job Description

Already created at `jd_files/job_description.txt`, but you can customize it:

```
Python Developer - Job Description

We are seeking a talented Python Developer to join our team.

REQUIRED SKILLS:
- Python (3+ years experience)
- Django or Flask framework
- PostgreSQL or MySQL database
- REST API development
- Git version control
- Problem-solving skills
- Team collaboration

PREFERRED SKILLS:
- AWS cloud experience
- Docker containerization
- CI/CD pipelines
- Microservices architecture
- React or JavaScript
- Agile/Scrum methodology

RESPONSIBILITIES:
- Develop web applications using Python
- Design and implement RESTful APIs
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Participate in code reviews
```

---

## 🧪 Complete Test Workflow

### Step 1: Prepare Test Data (2 min)

```bash
# Make sure you're in the project folder
cd hiring-automation-phase1

# Check test resumes exist
ls resumes/

# Should see: john_doe.docx, jane_smith.docx, etc.
```

### Step 2: Run Resume Ingestion (1 min)

```bash
python ingest_resumes.py
```

**Expected Output:**
```
============================================================
HIRING AUTOMATION - PHASE 1: RESUME INGESTION
============================================================

Step 1: Validating setup...
------------------------------------------------------------
✓ Found 3 resume(s) to process
✓ JD file found: jd_files/job_description.txt
✓ Credentials file found: credentials/service-account.json

Step 2: Initializing components...
------------------------------------------------------------
✓ Resume parser initialized
✓ JD matcher initialized (15 keywords extracted)
✓ Google Sheets manager initialized

Step 3: Parsing resumes...
------------------------------------------------------------
Processing: john_doe.docx
✓ Extracted: John Doe
Processing: jane_smith.docx
✓ Extracted: Jane Smith
Processing: bob_johnson.docx
✓ Extracted: Bob Johnson

✓ Total resumes processed: 3

Step 4: Evaluating candidates against JD...
------------------------------------------------------------
✓ Evaluated John Doe: 75% (Strong Fit)
✓ Evaluated Jane Smith: 68% (Good Fit)
✓ Evaluated Bob Johnson: 52% (Good Fit)

Step 5: Saving to Google Sheets...
------------------------------------------------------------
✓ Added 3 candidates to the sheet

============================================================
✓ SUCCESS: Resume ingestion completed!
============================================================
Total candidates processed: 3
Google Sheet URL: https://docs.google.com/spreadsheets/d/xxx
```

### Step 3: Check Google Sheet (1 min)

1. Open the URL shown above
2. You should see 3 candidates with all details
3. Check the columns are populated correctly

### Step 4: Approve Test Candidates (30 sec)

1. In Google Sheet, change `hr_approved` to "Yes" for John Doe
2. Sheet auto-saves

### Step 5: Test Notifications (1 min)

**Note:** For full test, you need Gmail and Twilio set up. For now, just run to see the flow:

```bash
python send_notifications.py
```

**Expected Output (without credentials):**
```
============================================================
HIRING AUTOMATION - PHASE 1: SEND NOTIFICATIONS
============================================================

Step 1: Validating setup...
------------------------------------------------------------
✗ Error: Gmail credentials file not found
# (This is expected if you haven't set up Gmail yet)
```

**Expected Output (with credentials):**
```
Step 3: Retrieving approved candidates...
------------------------------------------------------------
✓ Found 1 approved candidate(s)

Step 4: Sending notifications...
------------------------------------------------------------
[1/1] Processing: John Doe
----------------------------------------
✓ Email sent to john.doe@example.com
✓ WhatsApp message sent to whatsapp:+15551234567

============================================================
✓ NOTIFICATION PROCESS COMPLETED
============================================================
Total approved candidates: 1
Emails sent successfully: 1
WhatsApp messages sent successfully: 1
```

---

## 🎯 What to Test

### ✅ Basic Functionality Tests

- [ ] Resume parsing works for PDF
- [ ] Resume parsing works for DOCX
- [ ] Email extraction works
- [ ] Phone extraction works
- [ ] Name extraction works
- [ ] Google Sheet is created
- [ ] Candidates are added to sheet
- [ ] Fit scores are calculated
- [ ] Approved candidates are retrieved
- [ ] Email sending works (if configured)
- [ ] WhatsApp sending works (if configured)

### ✅ Edge Cases to Test

- [ ] Resume with no email → Email column should be empty
- [ ] Resume with no phone → Phone column should be empty
- [ ] Resume with different phone format → Should be normalized
- [ ] Empty resumes folder → Should show error
- [ ] Missing JD file → Should show error
- [ ] No approved candidates → Should show warning
- [ ] Re-running ingestion → Should append (not replace)

---

## 📊 Expected Test Results

### Good Match (70-100%):
- Resume has most skills from JD
- `auto_fit_label` = "Strong Fit"
- `auto_screen_comment` includes many matched skills

### Moderate Match (30-69%):
- Resume has some skills from JD
- `auto_fit_label` = "Good Fit" or "Moderate Fit"
- `auto_screen_comment` shows some matched, some missing

### Low Match (0-29%):
- Resume has few skills from JD
- `auto_fit_label` = "Weak Fit"
- `auto_screen_comment` shows mostly missing skills

---

## 🔄 Cleanup After Testing

### Delete Test Data from Google Sheet

1. Open Google Sheet
2. Select rows with test candidates
3. Right-click → Delete rows

### Or Clear Entire Sheet

1. Open Google Sheet
2. Select all rows except header (row 1)
3. Delete all selected rows

### Keep Test Resumes for Future Testing

Test resumes in `resumes/` folder can stay there for future tests.

---

## 🎓 Learning Exercise: Modify Test Data

### Exercise 1: Test Different Skills

1. Create a resume with NO matching skills
2. Run ingestion
3. Check if it gets "Weak Fit" label

### Exercise 2: Test Different Formats

1. Create a PDF resume (print DOCX to PDF)
2. Run ingestion
3. Verify both PDF and DOCX work

### Exercise 3: Test Phone Number Formats

Create resumes with different phone formats:
- `+1-555-123-4567`
- `(555) 123-4567`
- `555.123.4567`
- `+91-98765-43210` (India)

Check if all are extracted correctly.

### Exercise 4: Test Missing Information

Create a resume with:
- No email
- No phone
- No location

Check how the system handles missing data.

---

## 🚀 Ready for Real Data?

Once testing is complete:

1. Delete test candidates from Google Sheet
2. Remove test resumes from `resumes/` folder
3. Add real resumes
4. Update JD with real job description
5. Run the actual workflow!

---

**Test first, then go live!** This ensures everything works before processing real candidate data.
