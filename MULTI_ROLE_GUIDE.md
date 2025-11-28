# Multi-Role Screening Guide - For Teams Managing 30+ Positions

## ✅ Simple Setup - No Complex Configuration!

Your hiring automation tool now supports **unlimited job roles** with automatic detection!

---

## 🚀 How to Add New Job Positions

### Method 1: Create Files Directly (Recommended for Bulk Setup)

1. Open the `jd_library` folder
2. For each position, create a `.txt` file:
   - Filename format: `position_name.txt`
   - Example: `senior_python_developer.txt`
   - Example: `data_analyst.txt`
   - Example: `product_manager.txt`

3. Paste the job description in each file
4. Save the file

**That's it!** The system automatically detects all JD files!

---

### Method 2: Use the Web UI (For Adding One Role at a Time)

1. Go to "Process Resumes" page
2. If no JDs exist, you'll see a form
3. Enter:
   - Role Name: "Senior Python Developer"
   - Job Description: (paste the full JD)
4. Click "Create Job Role"
5. File automatically created!

---

## 📋 Using the System

### When Screening Resumes:

1. **Go to "Process Resumes" page**
2. **Step 1:** Select the job role from dropdown
   - System shows: "Found X job role(s)"
   - Choose which position you're screening for
3. **Step 2:** Upload resumes (PDF/DOCX)
4. **Step 3:** Click "Process Resumes"

**The system automatically:**
- Uses the correct JD for matching
- Tags candidates with Role ID
- Saves to Google Sheets with role information

---

## 📊 Google Sheets Organization

All candidates are saved with role tracking:

| Role ID | Role Name | Candidate Name | Email | Fit Score | Status |
|---------|-----------|----------------|-------|-----------|--------|
| ROLE001 | Senior Python Developer | John Doe | ... | 85% | Pending |
| ROLE002 | Data Analyst | Jane Smith | ... | 75% | Pending |
| ROLE003 | Product Manager | Bob Wilson | ... | 90% | Pending |

**Benefits:**
- ✅ All data in one place
- ✅ Easy filtering by role
- ✅ Cross-role candidate search
- ✅ Comprehensive reporting

---

## 🎯 Example Workflow for 30+ Positions

### One-Time Setup (15 minutes for 30 positions):

```
1. Open jd_library folder
2. Create 30 text files (one per position)
3. Paste job descriptions
4. Done!
```

### Daily Usage:

```
Morning: Screen for "Python Developer"
├─ Select "Senior Python Developer" from dropdown
├─ Upload 15 resumes
├─ Process → All tagged as ROLE001
└─ Results in Google Sheets

Afternoon: Screen for "Data Analyst"
├─ Select "Data Analyst" from dropdown
├─ Upload 10 resumes
├─ Process → All tagged as ROLE002
└─ Results in Google Sheets

Evening: Review all candidates
├─ Open Google Sheets
├─ Filter by role to see specific positions
└─ Approve/reject candidates
```

---

## 📁 File Naming Convention

**Good Examples:**
- `senior_python_developer.txt` → "Senior Python Developer"
- `data_analyst.txt` → "Data Analyst"
- `product_manager_saas.txt` → "Product Manager Saas"
- `ui_ux_designer.txt` → "Ui Ux Designer"

**The system automatically:**
- Converts underscores to spaces
- Capitalizes each word
- Generates unique Role IDs

---

## 💡 Pro Tips

1. **Consistent Naming:**
   - Use descriptive filenames
   - Include seniority level (senior, junior, mid-level)
   - Include department if needed

2. **Organize by Department:**
   - `eng_senior_python_developer.txt`
   - `eng_frontend_developer.txt`
   - `sales_account_executive.txt`
   - `sales_sdr.txt`

3. **View/Edit JDs:**
   - Click "View/Edit Job Description" expander
   - Make changes inline
   - Save updates

4. **Reuse JDs:**
   - Copy existing JD file
   - Rename for similar position
   - Edit as needed

---

## ✅ Current Setup

You already have example roles:
- ✅ `senior_python_developer.txt`
- ✅ `data_analyst.txt`
- ✅ `job_description.txt (from jd_files)` - Legacy file

**Add more by creating new .txt files in jd_library folder!**

---

## 🔍 Viewing Candidates by Role

### In Google Sheets:

1. Open your candidates sheet
2. Click on "Role Name" column header
3. Use filter dropdown
4. Select specific role
5. See only those candidates

### In Web UI (Review Candidates page):

1. Go to "Review Candidates"
2. Use "Role" column to see all roles
3. Sort/filter as needed

---

## ❓ FAQ

**Q: How many roles can I have?**
A: Unlimited! Create as many .txt files as you need.

**Q: Can I edit a JD after creating it?**
A: Yes! Either edit the .txt file directly or use the "View/Edit" option in the UI.

**Q: What if two roles have similar names?**
A: Use descriptive filenames: `python_developer_backend.txt` vs `python_developer_fullstack.txt`

**Q: Can I delete a role?**
A: Yes, just delete the .txt file from jd_library folder.

**Q: Will old candidates be affected if I change a JD?**
A: No, already-processed candidates keep their original scores.

---

## 🚀 Ready to Scale!

Your system is now ready to handle:
- ✅ 30+ simultaneous job positions
- ✅ Multiple team members screening
- ✅ Thousands of candidates
- ✅ Organized tracking and reporting

**No need to upload JDs every time - just select from the dropdown!**

