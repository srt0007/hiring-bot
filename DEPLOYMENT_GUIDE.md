# 🚀 Deployment Guide - hiring.printo.in

Complete guide to deploy your Hiring Automation Tool to a Printo subdomain.

---

## 📋 Table of Contents

1. [Local Testing](#local-testing)
2. [GitHub Setup](#github-setup)
3. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
4. [Cloudflare DNS Configuration](#cloudflare-dns-configuration)
5. [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Testing

Before deploying, test the web UI locally.

### Step 1: Install Web Dependencies

```bash
cd hiring-automation-phase1
python -m pip install -r requirements-web.txt
```

### Step 2: Run Streamlit Locally

```bash
streamlit run app.py
```

This will:
- Start a local web server
- Open your browser to `http://localhost:8501`
- Show the Hiring Automation web UI

### Step 3: Test All Features

✅ **Home Page** - Check system status
✅ **Process Resumes** - Upload a test resume
✅ **Review Candidates** - View and approve candidates
✅ **Send Notifications** - Test email/WhatsApp (optional)
✅ **Settings** - Check configuration

**If everything works locally, you're ready to deploy!**

---

## 📦 GitHub Setup

You need to push your code to GitHub before deploying to Streamlit Cloud.

### Step 1: Create GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the registration process

### Step 2: Create a New Repository

1. Click the "+" icon in top-right corner
2. Select "New repository"
3. Repository settings:
   - **Name:** `hiring-automation-printo`
   - **Visibility:** **Private** (important for security!)
   - **Don't** initialize with README (we already have files)
4. Click "Create repository"

### Step 3: Prepare Your Code

**IMPORTANT:** Before pushing, secure your credentials!

Create a `.gitignore` file (already exists, but verify):

```
# Credentials (NEVER commit these!)
credentials/
.env
token.json

# Python cache
__pycache__/
*.pyc
*.pyo

# Temporary files
resumes/
*.pdf
*.docx
temp/

# OS files
.DS_Store
Thumbs.db
```

**Make sure your credentials are NOT in Git:**

```bash
# Check what will be committed
git status

# If you see credentials files, they should be in .gitignore
# Do NOT proceed if credentials are showing!
```

### Step 4: Push to GitHub

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Hiring Automation Tool"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hiring-automation-printo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Your code is now on GitHub!**

---

## ☁️ Streamlit Cloud Deployment

Deploy your app to Streamlit Cloud (free hosting).

### Step 1: Create Streamlit Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up"
3. **Sign up with GitHub** (easiest option)
4. Authorize Streamlit to access your GitHub

### Step 2: Deploy Your App

1. Click "New app" button
2. Fill in deployment settings:
   - **Repository:** `YOUR_USERNAME/hiring-automation-printo`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Choose a subdomain (e.g., `hiring-printo`)
3. Click "Advanced settings"
4. Set **Python version:** `3.10` (or your version)
5. Click "Deploy!"

**Wait 5-10 minutes for deployment...**

### Step 3: Configure Secrets (Credentials)

Your app needs credentials but they can't be in GitHub!

1. In Streamlit Cloud dashboard, click on your app
2. Click the "⚙️ Settings" menu
3. Click "Secrets"
4. Add your secrets in TOML format:

```toml
# Google Sheets Service Account
[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account"

# Twilio (WhatsApp)
[twilio]
account_sid = "your-twilio-account-sid"
auth_token = "your-twilio-auth-token"
whatsapp_from = "whatsapp:+14155238886"

# Role settings
[role]
role_id = "ROLE001"
role_name = "Python Developer"
```

**How to get these values:**

From `credentials/service-account.json`:
```bash
# Open the file and copy the values
notepad credentials\service-account.json
```

From `.env` file:
```bash
# Open the file and copy Twilio values
notepad .env
```

5. Click "Save"
6. Your app will automatically restart with the secrets

### Step 4: Update Code to Use Secrets

We need to modify the code to read from Streamlit secrets instead of local files.

**Create a new file: `secrets_helper.py`**

```python
import streamlit as st
import json
import os

def get_google_credentials():
    """Get Google Sheets credentials from Streamlit secrets or local file"""
    try:
        # Try Streamlit secrets first (for deployment)
        if 'google_sheets' in st.secrets:
            return dict(st.secrets['google_sheets'])
        else:
            # Fall back to local file (for local testing)
            with open('credentials/service-account.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Failed to load Google credentials: {str(e)}")
        return None

def get_twilio_credentials():
    """Get Twilio credentials from Streamlit secrets or .env"""
    try:
        # Try Streamlit secrets first
        if 'twilio' in st.secrets:
            return {
                'account_sid': st.secrets['twilio']['account_sid'],
                'auth_token': st.secrets['twilio']['auth_token'],
                'whatsapp_from': st.secrets['twilio']['whatsapp_from']
            }
        else:
            # Fall back to .env file
            from dotenv import load_dotenv
            load_dotenv()
            return {
                'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
                'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
                'whatsapp_from': os.getenv('TWILIO_WHATSAPP_FROM')
            }
    except Exception as e:
        st.error(f"Failed to load Twilio credentials: {str(e)}")
        return None
```

**Then update `app.py`** to use this helper (I'll provide the updated version if needed).

### Step 5: Get Your App URL

Once deployed, you'll get a URL like:
```
https://hiring-printo-abc123.streamlit.app
```

**✅ Your app is now live!**

---

## 🔗 Cloudflare DNS Configuration

Point `hiring.printo.in` to your Streamlit app.

### Step 1: Login to Cloudflare

1. Go to [cloudflare.com](https://cloudflare.com)
2. Login with your Printo account
3. Select the `printo.in` domain

### Step 2: Add CNAME Record

1. Click "DNS" in the left menu
2. Click "Add record"
3. Fill in:
   - **Type:** CNAME
   - **Name:** `hiring` (this creates hiring.printo.in)
   - **Target:** `hiring-printo-abc123.streamlit.app` (your Streamlit URL)
   - **Proxy status:** Proxied (orange cloud icon)
   - **TTL:** Auto
4. Click "Save"

**Wait 5-10 minutes for DNS propagation...**

### Step 3: Configure Streamlit for Custom Domain

1. Go back to Streamlit Cloud dashboard
2. Click on your app
3. Click "⚙️ Settings"
4. Click "General"
5. Under "Custom domain", add: `hiring.printo.in`
6. Click "Save"

**Streamlit will provide instructions to verify domain ownership:**

1. Copy the TXT record values
2. Go back to Cloudflare DNS
3. Add a TXT record:
   - **Type:** TXT
   - **Name:** `_streamlit-site-verification.hiring`
   - **Content:** (paste the verification code)
4. Click "Save"
5. Go back to Streamlit and click "Verify domain"

**Wait 5-10 minutes...**

### Step 4: Test Your Domain

Open your browser and visit:
```
https://hiring.printo.in
```

**✅ Your app is now accessible at hiring.printo.in!**

---

## 🔒 Security Checklist

Before going live, verify:

- [ ] Credentials are NOT in GitHub repository
- [ ] Repository is set to **Private**
- [ ] Streamlit secrets are configured correctly
- [ ] `.gitignore` includes all sensitive files
- [ ] Google Sheets API credentials are working
- [ ] Only authorized people have access to the app
- [ ] Cloudflare proxy is enabled (orange cloud)

---

## 🐛 Troubleshooting

### Issue: "App failed to start"

**Solution:**
1. Check Streamlit logs (click on app → "Manage app" → "Logs")
2. Look for missing dependencies
3. Verify secrets are configured correctly
4. Make sure `requirements-web.txt` is complete

### Issue: "Can't connect to Google Sheets"

**Solution:**
1. Verify secrets are in correct TOML format
2. Check that service account has access to the sheet
3. Make sure all required fields are in secrets
4. Test with local credentials first

### Issue: "Custom domain not working"

**Solution:**
1. Wait longer (DNS can take up to 24 hours)
2. Clear your browser cache
3. Try accessing from incognito mode
4. Check Cloudflare DNS records are correct
5. Verify domain ownership in Streamlit

### Issue: "Email/WhatsApp not sending"

**Solution:**
1. Gmail API requires OAuth2 - harder to set up for deployment
2. For production, consider using SMTP instead of Gmail API
3. Verify Twilio credentials in secrets
4. Check Twilio account has sufficient balance

---

## 🎯 Alternative Deployment Options

If Streamlit Cloud doesn't work for you:

### Option 1: Heroku (Simple)
- Similar to Streamlit Cloud
- Free tier available
- Good for small teams
- Guide: [Heroku Streamlit Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)

### Option 2: Railway (Modern)
- Easy deployment
- Free tier available
- Automatic HTTPS
- Guide: [Railway Deployment](https://railway.app/)

### Option 3: DigitalOcean (Full Control)
- Your own server
- More configuration required
- $5/month
- Full control over environment

### Option 4: AWS EC2 (Enterprise)
- Most flexible
- Complex setup
- Pay-as-you-go pricing
- Best for large scale

---

## 📊 Cost Breakdown

### Completely Free Option:
- ✅ Streamlit Cloud: Free
- ✅ GitHub: Free (private repo)
- ✅ Cloudflare: Free (DNS + proxy)
- ✅ Google Sheets API: Free
- ⚠️ Gmail API: Free (with limits)
- ⚠️ Twilio: Pay-per-message (~$0.005/WhatsApp)

**Total: $0/month + Twilio usage**

### Paid Option (More Reliable):
- Heroku Hobby: $7/month
- Railway: $5/month
- DigitalOcean: $5/month
- SendGrid Email: Free tier (100 emails/day)

---

## 🚀 Next Steps After Deployment

1. **Test thoroughly** with sample data
2. **Share the link** with your team
3. **Train your team** on how to use it
4. **Monitor usage** and errors
5. **Collect feedback** for Phase 2
6. **Scale up** as needed

---

## 📧 Support

If you face any issues during deployment:

1. Check Streamlit logs
2. Review Cloudflare DNS settings
3. Verify all secrets are configured
4. Test locally first before debugging deployment

---

**🎉 Congratulations! Your hiring automation tool is now live at hiring.printo.in!**
