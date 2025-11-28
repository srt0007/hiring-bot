# Troubleshooting Guide - Hiring Automation Phase 1

Common issues and their solutions.

---

## 🐛 Installation Issues

### Issue: "python: command not found"

**Symptoms:**
```bash
python --version
# bash: python: command not found
```

**Solutions:**
1. Try `python3` instead:
   ```bash
   python3 --version
   python3 ingest_resumes.py
   ```

2. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)

3. On Windows, make sure Python is added to PATH during installation

---

### Issue: "pip: command not found"

**Symptoms:**
```bash
pip install -r requirements.txt
# bash: pip: command not found
```

**Solutions:**
1. Try `pip3`:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Use Python module:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Install pip:
   ```bash
   python -m ensurepip --upgrade
   ```

---

### Issue: "ModuleNotFoundError: No module named 'XXX'"

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'gspread'
ModuleNotFoundError: No module named 'PyPDF2'
```

**Solutions:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. If using virtual environment, make sure it's activated:
   ```bash
   # On Windows
   venv\Scripts\activate

   # On Mac/Linux
   source venv/bin/activate
   ```

3. Try installing specific module:
   ```bash
   pip install gspread
   pip install PyPDF2
   ```

---

## 🔑 Google Sheets API Issues

### Issue: "Credentials file not found"

**Symptoms:**
```
✗ Error: Google credentials file 'credentials/service-account.json' not found
```

**Solutions:**
1. Check file exists:
   ```bash
   ls credentials/service-account.json
   ```

2. Download service account credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to "APIs & Services" → "Credentials"
   - Create service account
   - Download JSON key
   - Save as `credentials/service-account.json`

3. Check file path is correct (exact name and location)

---

### Issue: "gspread.exceptions.APIError: PERMISSION_DENIED"

**Symptoms:**
```
gspread.exceptions.APIError: {
  "error": {
    "code": 403,
    "message": "PERMISSION_DENIED"
  }
}
```

**Solutions:**
1. Enable required APIs in Google Cloud:
   - Google Sheets API
   - Google Drive API

2. Wait 1-2 minutes after enabling APIs

3. Make sure you're using service account credentials (not OAuth)

4. Check that the service account has permissions

---

### Issue: "Cannot create/access Google Sheet"

**Symptoms:**
```
✗ Error: SpreadsheetNotFound
```

**Solutions:**
1. First time running: Script will create a new sheet automatically

2. If you want to use existing sheet:
   - Share the sheet with the service account email
   - Service account email format: `xxx@xxx.iam.gserviceaccount.com`
   - Find it in your `service-account.json` file

3. Check internet connection

---

## 📧 Gmail API Issues

### Issue: "Gmail credentials not found"

**Symptoms:**
```
✗ Error: Gmail credentials file 'credentials/gmail-credentials.json' not found
```

**Solutions:**
1. Download OAuth 2.0 credentials:
   - Go to Google Cloud Console
   - "APIs & Services" → "Credentials"
   - Create "OAuth client ID" (Desktop app)
   - Download JSON
   - Save as `credentials/gmail-credentials.json`

2. Do NOT use service account for Gmail (use OAuth 2.0)

---

### Issue: "Gmail authentication browser doesn't open"

**Symptoms:**
- Script hangs at authentication step
- No browser window opens

**Solutions:**
1. Manually open the URL shown in terminal

2. If running on remote server:
   - Run locally first to generate token
   - Copy `token.json` to server

3. Check firewall settings

---

### Issue: "Access blocked: Authorization Error"

**Symptoms:**
```
Error 403: access_denied
The OAuth client was not found.
```

**Solutions:**
1. Make sure OAuth consent screen is configured:
   - Go to "APIs & Services" → "OAuth consent screen"
   - Add your email as test user

2. Publishing status should be "Testing" or "Published"

3. Re-download OAuth credentials

---

### Issue: "Email not sending"

**Symptoms:**
```
✗ Error sending email to xxx@example.com
```

**Solutions:**
1. Check Gmail API is enabled

2. Verify token.json exists and is valid:
   ```bash
   ls credentials/token.json
   ```

3. Delete token.json and re-authenticate:
   ```bash
   rm credentials/token.json
   python send_notifications.py
   ```

4. Check recipient email is valid

5. Check Gmail sending limits (500 emails/day for free)

---

## 📱 Twilio/WhatsApp Issues

### Issue: "Twilio credentials not found in .env"

**Symptoms:**
```
⚠ Warning: Twilio credentials not found in .env file
WhatsApp messages will be skipped
```

**Solutions:**
1. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```

3. Get credentials from [Twilio Console](https://console.twilio.com/)

---

### Issue: "Twilio authentication failed"

**Symptoms:**
```
✗ Error: Unable to create record: Authenticate
```

**Solutions:**
1. Verify Account SID and Auth Token are correct

2. Check for extra spaces in `.env` file

3. Don't include quotes around values in `.env`:
   ```
   # Wrong
   TWILIO_ACCOUNT_SID="ACxxxx"

   # Correct
   TWILIO_ACCOUNT_SID=ACxxxx
   ```

---

### Issue: "WhatsApp message not sending"

**Symptoms:**
```
✗ Error sending WhatsApp to +1234567890
```

**Solutions:**
1. Join WhatsApp Sandbox:
   - Go to Twilio Console → Messaging → Try it out
   - Send join message from recipient's phone

2. Check phone number format:
   - Include country code with `+`
   - Example: `+14155238886` (not `4155238886`)

3. Verify Twilio WhatsApp number is correct in `.env`

4. Check Twilio account balance (free trial has credits)

---

## 📄 Resume Parsing Issues

### Issue: "No resume files found"

**Symptoms:**
```
✗ Error: No resume files found in 'resumes/'
Please add PDF or DOCX resume files
```

**Solutions:**
1. Add resume files to `resumes/` folder

2. Check file extensions are `.pdf` or `.docx` (lowercase)

3. List files to verify:
   ```bash
   ls resumes/
   ```

---

### Issue: "Cannot extract text from PDF"

**Symptoms:**
```
✗ Could not extract sufficient text from resume.pdf
```

**Solutions:**
1. **Scanned PDFs (images):** Use OCR tools to convert to text:
   - Adobe Acrobat OCR
   - Online OCR tools
   - Tesseract OCR

2. **Password-protected PDFs:** Remove password first

3. **Corrupted PDFs:** Re-save or re-download the file

4. Try converting to DOCX format

---

### Issue: "Email/Phone not extracted"

**Symptoms:**
- Candidate added but email is blank
- Phone number is blank

**Solutions:**
1. Check if resume actually contains email/phone

2. Format might not be recognized - try standardizing:
   - Email: `john@example.com` format
   - Phone: `+1-234-567-8900` or `(234) 567-8900`

3. Manually add to Google Sheet after ingestion

---

### Issue: "Candidate name is filename"

**Symptoms:**
- Name shows as "john_doe_resume" instead of "John Doe"

**Solutions:**
1. This is fallback behavior when name can't be extracted

2. Check if resume has name in first few lines

3. Make sure name isn't in header/footer (may not be extracted)

4. Manually fix in Google Sheet

---

## 🔍 JD Matching Issues

### Issue: "All candidates show low fit scores"

**Symptoms:**
- Every candidate has score < 30%
- auto_fit_label = "Weak Fit" for all

**Solutions:**
1. Check JD file has actual content:
   ```bash
   cat jd_files/job_description.txt
   ```

2. Add more skills and keywords to JD

3. Edit `src/jd_matcher.py` to add domain-specific keywords:
   ```python
   common_skills = [
       'python', 'java', ...
       'your_skill_1', 'your_skill_2'
   ]
   ```

4. JD should include technical skills explicitly

---

### Issue: "JD file not found"

**Symptoms:**
```
✗ Error: Job description file 'jd_files/job_description.txt' not found
```

**Solutions:**
1. Check file exists:
   ```bash
   ls jd_files/job_description.txt
   ```

2. Create the file if missing:
   ```bash
   nano jd_files/job_description.txt
   # Add job description content
   ```

---

## 📊 Google Sheets Data Issues

### Issue: "No approved candidates found"

**Symptoms:**
```
⚠ No approved candidates found (hr_approved = 'Yes')
```

**Solutions:**
1. Open Google Sheet and check `hr_approved` column

2. Make sure you typed "Yes" (not "yes" or "YES"):
   - Correct: `Yes`
   - Wrong: `yes`, `YES`, `Y`

3. No extra spaces: "Yes" not " Yes " or "Yes "

4. Save the sheet (should auto-save)

---

### Issue: "Duplicate candidates in sheet"

**Symptoms:**
- Same candidate appears multiple times

**Solutions:**
1. This is expected if you run `ingest_resumes.py` multiple times

2. Script appends new data (doesn't check duplicates)

3. Manually delete duplicate rows in Google Sheet

4. Or clear sheet before re-running:
   - Delete all rows except header
   - Run script again

---

## 🌐 Network/Connection Issues

### Issue: "Connection timeout"

**Symptoms:**
```
requests.exceptions.ConnectionError: Connection timeout
```

**Solutions:**
1. Check internet connection

2. Check firewall settings

3. Try again after a few minutes

4. If behind proxy, configure proxy settings:
   ```bash
   export HTTP_PROXY=http://proxy.example.com:8080
   export HTTPS_PROXY=http://proxy.example.com:8080
   ```

---

## 🔧 General Debugging

### Enable Verbose Logging

Add to top of script for more details:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Python Version

```bash
python --version
# Should be 3.8 or higher
```

### Check Installed Packages

```bash
pip list
# Check if all required packages are installed
```

### Verify File Paths

```bash
# List all project files
find . -type f -name "*.py"
find . -type f -name "*.json"
```

### Test Individual Modules

```bash
# Test resume parser alone
cd src
python resume_parser.py

# Test JD matcher alone
python jd_matcher.py

# Test Google Sheets
python google_sheets_manager.py
```

---

## 🆘 Still Having Issues?

### Checklist:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Credentials files in correct location
- [ ] APIs enabled in Google Cloud
- [ ] Internet connection working
- [ ] Files have correct permissions

### Get More Info:
1. Read full error message (don't skip stack trace)
2. Check if error is at import or runtime
3. Verify all file paths are correct
4. Check README.md setup steps again

### Common Error Patterns:

| Error Type | Common Cause | Quick Fix |
|------------|--------------|-----------|
| ModuleNotFoundError | Missing package | `pip install package_name` |
| FileNotFoundError | Wrong path | Check file exists |
| PermissionError | File permissions | Check read/write access |
| APIError 403 | API not enabled | Enable in Google Cloud |
| APIError 401 | Bad credentials | Re-download credentials |
| ConnectionError | No internet | Check connection |

---

## 📝 Reporting Issues

If you need to report an issue, include:

1. **Error message** (full stack trace)
2. **Python version** (`python --version`)
3. **Installed packages** (`pip list`)
4. **Steps to reproduce**
5. **Expected vs actual behavior**

---

**Most issues can be solved by:**
1. Re-reading the setup instructions in README.md
2. Checking file paths and names are exact
3. Ensuring all APIs are enabled
4. Verifying credentials are correct

---

**Need more help?** Check [README.md](README.md) or [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
