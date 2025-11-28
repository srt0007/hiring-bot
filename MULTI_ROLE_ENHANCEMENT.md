# Multi-Role Management Enhancement

## What's Being Added

Your hiring automation tool will now support **30+ positions simultaneously**!

### New Features:

1. **Manage Roles Page** - Add/view/manage all job positions
2. **Role Selection** - Select which role you're screening for
3. **Separate Tracking** - Each role tracks candidates independently
4. **JD Library** - Store multiple job descriptions
5. **Role-based Filtering** - View candidates by position

---

## How It Works

### For Your Team:

**Step 1: Add New Job Positions**
1. Go to "Manage Roles" page
2. Click "Add New Role"
3. Enter:  
   - Role Name (e.g., "Senior Python Developer")
   - Job Description (paste or upload)
4. Click "Save Role"

**Step 2: Upload Resumes for a Specific Role**
1. Go to "Process Resumes" page
2. **Select Role from Dropdown** (e.g., "Senior Python Developer")
3. Upload resumes
4. All candidates tagged with that role

**Step 3: Review by Role**
1. Go to "Review Candidates" page
2. Filter by role
3. See only candidates for that position

---

## File Structure

```
hiring-automation-phase1/
├── jd_library/                    # All job descriptions
│   ├── python_developer.txt
│   ├── data_analyst.txt
│   ├── product_manager.txt
│   └── ... (30+ files)
├── roles_config.json              # Role database
└── src/
    └── role_manager.py            # Role management logic
```

---

## Google Sheets Structure

All candidates go to the same sheet but with role tracking:

| Role ID | Role Name | Candidate Name | Email | Fit Score | Status |
|---------|-----------|----------------|-------|-----------|--------|
| ROLE001 | Python Developer | John Doe | ... | 85% | Pending |
| ROLE002 | Data Analyst | Jane Smith | ... | 75% | Pending |
| ROLE001 | Python Developer | Bob Wilson | ... | 90% | Approved |

**Benefits:**
- Single source of truth
- Easy filtering by role
- Cross-role candidate search
- Comprehensive reporting

---

## Implementation Status

✅ Role Manager module created
✅ Configuration file created
✅ Ready to integrate into web UI

**Next Step:** Update app.py to add "Manage Roles" page

---

## For 30+ Positions

**Workflow:**
1. HR team adds all 30+ job roles once
2. Recruiters select role when uploading resumes
3. System automatically matches against correct JD
4. Candidates tracked by role in Google Sheets
5. Easy filtering and reporting per role

**Time Saved:**
- No need to upload JD every time ✅
- No confusion about which role ✅
- Automatic organization ✅
- Bulk processing per role ✅

