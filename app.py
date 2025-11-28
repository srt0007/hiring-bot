"""
HIRING AUTOMATION - STREAMLIT WEB UI
A user-friendly web interface for the hiring automation tool
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
import importlib

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Force reload modules to avoid caching issues
if 'src.resume_parser' in sys.modules:
    importlib.reload(sys.modules['src.resume_parser'])
if 'src.jd_matcher' in sys.modules:
    importlib.reload(sys.modules['src.jd_matcher'])
if 'src.google_sheets_manager' in sys.modules:
    importlib.reload(sys.modules['src.google_sheets_manager'])

from src.resume_parser import ResumeParser
from src.jd_matcher import JDMatcher
from src.google_sheets_manager import GoogleSheetsManager
from src.email_sender import EmailSender
from src.whatsapp_sender import WhatsAppSender

# Page configuration
st.set_page_config(
    page_title="Hiring Automation - Printo",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #145a8a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_candidates' not in st.session_state:
    st.session_state.processed_candidates = []
if 'sheet_url' not in st.session_state:
    st.session_state.sheet_url = None
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = None

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📄 Process Resumes", "👥 Review Candidates", "📧 Send Notifications", "⚙️ Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**Hiring Automation Tool**

Streamline your hiring process:
- Upload & parse resumes
- Match candidates to JD
- Review & approve
- Send notifications

Built with ❤️ for Printo
""")

# Helper functions
def validate_setup():
    """Validate that all required files and folders exist"""
    errors = []
    warnings = []

    # Check credentials
    if not os.path.exists('credentials/service-account.json'):
        errors.append("Google Sheets credentials not found")

    if not os.path.exists('credentials/gmail-credentials.json'):
        warnings.append("Gmail credentials not found (email notifications disabled)")

    # Check folders
    if not os.path.exists('resumes'):
        os.makedirs('resumes')
        warnings.append("Created 'resumes' folder")

    if not os.path.exists('jd_files'):
        os.makedirs('jd_files')
        warnings.append("Created 'jd_files' folder")

    # Check templates
    if not os.path.exists('templates/email_template.html'):
        warnings.append("Email template not found")

    if not os.path.exists('templates/whatsapp_template.txt'):
        warnings.append("WhatsApp template not found")

    return errors, warnings

def get_sheets_manager():
    """Get or create Google Sheets manager instance"""
    if st.session_state.sheets_manager is None:
        try:
            st.session_state.sheets_manager = GoogleSheetsManager('credentials/service-account.json')

            # Try to open existing sheet first (to avoid storage quota issues)
            try:
                # Use the existing sheet ID
                st.session_state.sheets_manager.sheet = st.session_state.sheets_manager.client.open_by_key('1hqcD0b1fuYjyJab1oLu9y_4wTuvM1EeQeFdbHV3zJGE')
                st.session_state.sheets_manager.worksheet = st.session_state.sheets_manager.sheet.worksheet('Candidates_Master')
                st.session_state.sheet_url = 'https://docs.google.com/spreadsheets/d/1hqcD0b1fuYjyJab1oLu9y_4wTuvM1EeQeFdbHV3zJGE'
            except:
                # If that fails, try to create new
                st.session_state.sheets_manager.sheet = st.session_state.sheets_manager.get_or_create_sheet('Hiring_Automation_Candidates')
                st.session_state.sheets_manager.worksheet = st.session_state.sheets_manager.setup_candidates_master_sheet()
                st.session_state.sheet_url = st.session_state.sheets_manager.get_sheet_url()

        except Exception as e:
            st.error(f"Failed to initialize Google Sheets: {str(e)}")
            return None
    return st.session_state.sheets_manager

# ============================================================
# HOME PAGE
# ============================================================
if page == "🏠 Home":
    st.markdown('<div class="main-header">🎯 Hiring Automation Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Streamline your recruitment process with automated resume screening</div>', unsafe_allow_html=True)

    # System status
    st.markdown("### 📊 System Status")

    errors, warnings = validate_setup()

    col1, col2, col3 = st.columns(3)

    with col1:
        if not errors:
            st.success("✅ System Ready")
        else:
            st.error(f"❌ {len(errors)} Error(s)")

    with col2:
        resume_count = len([f for f in os.listdir('resumes') if f.endswith(('.pdf', '.docx'))]) if os.path.exists('resumes') else 0
        st.info(f"📄 {resume_count} Resume(s)")

    with col3:
        if st.session_state.sheet_url:
            st.success("📊 Sheet Connected")
        else:
            st.warning("📊 No Sheet Yet")

    # Show errors and warnings
    if errors:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown("**❌ Errors:**")
        for error in errors:
            st.markdown(f"- {error}")
        st.markdown('</div>', unsafe_allow_html=True)

    if warnings:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**⚠️ Warnings:**")
        for warning in warnings:
            st.markdown(f"- {warning}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick actions
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Process Resumes", key="home_process"):
            st.session_state.page = "📄 Process Resumes"
            st.rerun()

    with col2:
        if st.button("👥 Review Candidates", key="home_review"):
            st.session_state.page = "👥 Review Candidates"
            st.rerun()

    with col3:
        if st.button("📧 Send Notifications", key="home_notify"):
            st.session_state.page = "📧 Send Notifications"
            st.rerun()

    # Workflow diagram
    st.markdown("### 📋 Workflow")
    st.markdown("""
    ```
    1. Upload Resumes (PDF/DOCX)
           ↓
    2. Add Job Description
           ↓
    3. Process & Match
           ↓
    4. Review in Google Sheets
           ↓
    5. Approve Candidates
           ↓
    6. Send Email & WhatsApp
    ```
    """)

    # Google Sheet link
    if st.session_state.sheet_url:
        st.markdown("### 📊 Your Google Sheet")
        st.markdown(f"[🔗 Open Candidates Sheet]({st.session_state.sheet_url})")

# ============================================================
# PROCESS RESUMES PAGE
# ============================================================
elif page == "📄 Process Resumes":
    st.markdown('<div class="main-header">📄 Process Resumes</div>', unsafe_allow_html=True)

    # Check setup
    errors, warnings = validate_setup()
    if errors:
        st.error("⚠️ Please fix the errors on the Home page before processing resumes.")
        st.stop()

    # Job Description / Role Selection
    st.markdown("### 📝 Step 1: Select Job Role")

    # Auto-detect all JD files in jd_library folder
    jd_library_path = 'jd_library'
    if not os.path.exists(jd_library_path):
        os.makedirs(jd_library_path)

    # Get all .txt files in jd_library
    jd_files_list = [f for f in os.listdir(jd_library_path) if f.endswith('.txt')]

    # Also check old jd_files folder for backward compatibility
    if os.path.exists('jd_files/job_description.txt') and 'job_description.txt' not in jd_files_list:
        jd_files_list.insert(0, 'job_description.txt (from jd_files)')

    if not jd_files_list:
        st.warning("⚠️ No job descriptions found!")
        st.info("""
        **How to add job roles:**
        1. Go to the `jd_library` folder (created for you)
        2. For each position, create a .txt file with the JD
           - Example: `senior_python_developer.txt`
           - Example: `data_analyst.txt`
        3. Refresh this page

        **Or use the form below to create one now:**
        """)

        # Simple form to create JD
        new_role_name = st.text_input("Role Name (e.g., Senior Python Developer):")
        new_jd_text = st.text_area("Job Description:", height=200)

        if st.button("💾 Create Job Role") and new_role_name and new_jd_text:
            # Convert role name to filename
            filename = new_role_name.lower().replace(' ', '_') + '.txt'
            filepath = os.path.join(jd_library_path, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_jd_text)

            st.success(f"✅ Created: {filename}")
            st.rerun()

        jd_text = ""
        selected_jd_file = None
    else:
        # Show success message with count
        st.success(f"✅ Found {len(jd_files_list)} job role(s)")

        # Let user select which role
        selected_jd_file = st.selectbox(
            "Select the job role you're screening for:",
            options=jd_files_list,
            help="Choose which position these resumes are for"
        )

        # Load the selected JD
        if selected_jd_file.endswith('(from jd_files)'):
            jd_file_path = 'jd_files/job_description.txt'
        else:
            jd_file_path = os.path.join(jd_library_path, selected_jd_file)

        with open(jd_file_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()

        # Option to view/edit
        with st.expander("📄 View/Edit Job Description"):
            edited_jd = st.text_area(
                "Job Description:",
                value=jd_text,
                height=200,
                key="edit_jd"
            )

            if st.button("💾 Save Changes"):
                with open(jd_file_path, 'w', encoding='utf-8') as f:
                    f.write(edited_jd)
                st.success("✅ Updated!")
                jd_text = edited_jd

    st.markdown("---")

    # Resume upload
    st.markdown("### 📤 Step 2: Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload resume files (PDF or DOCX)",
        type=['pdf', 'docx'],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

        # Show uploaded files
        with st.expander("📋 View uploaded files"):
            for file in uploaded_files:
                st.text(f"📄 {file.name} ({file.size / 1024:.1f} KB)")

    st.markdown("---")

    # Process button
    st.markdown("### ⚙️ Step 3: Process")

    # Auto-generate role name and ID from selected JD file
    if selected_jd_file:
        if selected_jd_file.endswith('(from jd_files)'):
            role_name_auto = "Python Developer"
            role_id_auto = "ROLE001"
        else:
            # Convert filename to role name
            role_name_auto = selected_jd_file.replace('.txt', '').replace('_', ' ').title()
            # Generate role ID from index
            role_index = jd_files_list.index(selected_jd_file) + 1
            role_id_auto = f"ROLE{role_index:03d}"

        st.info(f"**Processing for:** {role_name_auto} (ID: {role_id_auto})")
        role_name = role_name_auto
        role_id = role_id_auto
    else:
        role_name = "Unknown Role"
        role_id = "ROLE000"

    if st.button("🚀 Process Resumes", type="primary", disabled=not uploaded_files or not jd_text):
        if not uploaded_files:
            st.error("❌ Please upload at least one resume")
        elif not jd_text:
            st.error("❌ Please enter a job description")
        else:
            # Save uploaded files to resumes folder
            with st.spinner("📤 Saving uploaded files..."):
                for uploaded_file in uploaded_files:
                    file_path = os.path.join('resumes', uploaded_file.name)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())

            # Initialize components
            with st.spinner("🔧 Initializing components..."):
                try:
                    resume_parser = ResumeParser()
                    jd_matcher = JDMatcher(jd_file_path='jd_files/job_description.txt')
                    sheets_manager = get_sheets_manager()

                    if sheets_manager is None:
                        st.error("❌ Failed to initialize Google Sheets")
                        st.stop()

                    st.success("✅ Components initialized")
                except Exception as e:
                    st.error(f"❌ Initialization error: {str(e)}")
                    st.stop()

            # Parse resumes
            st.markdown("### 📊 Processing Results")
            progress_bar = st.progress(0)
            status_text = st.empty()

            candidates = []

            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")

                try:
                    # Parse resume
                    file_path = os.path.join('resumes', uploaded_file.name)
                    parsed_data = resume_parser.parse_resume(file_path)

                    # Validate parsed_data is a dictionary
                    if parsed_data is None or not isinstance(parsed_data, dict):
                        st.warning(f"⚠️ Could not parse {uploaded_file.name}")
                        continue

                    if 'resume_text' not in parsed_data or not parsed_data['resume_text']:
                        st.warning(f"⚠️ No text extracted from {uploaded_file.name}")
                        continue

                    # Match against JD (pass the full dictionary, not just the text)
                    evaluation_result = jd_matcher.evaluate_candidate(parsed_data)

                    # Extract evaluation fields
                    evaluation = {
                        'fit_score': evaluation_result.get('auto_fit_score', 0),
                        'fit_label': evaluation_result.get('auto_fit_label', 'Unknown'),
                        'screening_comment': evaluation_result.get('auto_screen_comment', '')
                    }

                    # Ensure evaluation is a dictionary
                    if evaluation is None or not isinstance(evaluation, dict):
                        st.warning(f"⚠️ Could not evaluate {uploaded_file.name} - invalid evaluation result")
                        continue

                    # Extract candidate info safely
                    candidate_name = parsed_data.get('candidate_name') if isinstance(parsed_data, dict) else 'Unknown'
                    phone = parsed_data.get('phone', '') if isinstance(parsed_data, dict) else ''
                    email = parsed_data.get('email', '') if isinstance(parsed_data, dict) else ''
                    location = parsed_data.get('location', '') if isinstance(parsed_data, dict) else ''

                    fit_score = evaluation.get('fit_score', 0) if isinstance(evaluation, dict) else 0
                    fit_label = evaluation.get('fit_label', 'Unknown') if isinstance(evaluation, dict) else 'Unknown'
                    screen_comment = evaluation.get('screening_comment', '') if isinstance(evaluation, dict) else ''

                    # Combine data
                    candidate = {
                        'role_id': role_id,
                        'role_name': role_name,
                        'candidate_name': candidate_name,
                        'phone': phone,
                        'email': email,
                        'location': location,
                        'source_portal': 'Manual Upload',
                        'auto_fit_score': fit_score,
                        'auto_fit_label': fit_label,
                        'auto_screen_comment': screen_comment,
                        'hr_approved': 'No'
                    }

                    candidates.append(candidate)
                    st.success(f"✅ {candidate_name} - {fit_score}% ({fit_label})")

                except Exception as e:
                    import traceback
                    error_details = traceback.format_exc()
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    # Print full traceback to console for debugging
                    print(f"Full error for {uploaded_file.name}:")
                    print(error_details)

                progress_bar.progress((idx + 1) / len(uploaded_files))

            status_text.text("✅ All resumes processed!")

            # Save to Google Sheets
            if candidates:
                with st.spinner("💾 Saving to Google Sheets..."):
                    try:
                        sheets_manager.add_multiple_candidates(candidates)
                        sheet_url = sheets_manager.get_sheet_url()
                        st.session_state.sheet_url = sheet_url
                        st.session_state.processed_candidates = candidates

                        st.success(f"✅ {len(candidates)} candidate(s) saved to Google Sheets!")
                        st.markdown(f"[🔗 Open Google Sheet]({sheet_url})")

                        # Show summary
                        st.markdown("### 📈 Summary")
                        summary_data = []
                        for c in candidates:
                            summary_data.append({
                                'Name': str(c['candidate_name']),
                                'Email': str(c['email']),
                                'Phone': str(c['phone']),
                                'Fit Score': int(c['auto_fit_score']) if c['auto_fit_score'] else 0,
                                'Fit Label': str(c['auto_fit_label'])
                            })
                        st.dataframe(summary_data, use_container_width=True)

                    except Exception as e:
                        st.error(f"❌ Failed to save to Google Sheets: {str(e)}")
            else:
                st.warning("⚠️ No candidates were successfully processed")

# ============================================================
# REVIEW CANDIDATES PAGE
# ============================================================
elif page == "👥 Review Candidates":
    st.markdown('<div class="main-header">👥 Review Candidates</div>', unsafe_allow_html=True)

    # Get sheets manager
    sheets_manager = get_sheets_manager()

    if sheets_manager is None:
        st.error("❌ Google Sheets not configured. Please check your credentials.")
        st.stop()

    # Load candidates from Google Sheets
    with st.spinner("📥 Loading candidates from Google Sheets..."):
        try:
            # Get all candidates
            worksheet = sheets_manager.worksheet
            all_data = worksheet.get_all_values()

            if len(all_data) <= 1:
                st.info("ℹ️ No candidates found. Please process some resumes first.")
                st.stop()

            # Convert to list of dictionaries
            headers = all_data[0]
            rows = all_data[1:]
            candidates_list = []
            for row in rows:
                candidate_dict = {}
                for i, header in enumerate(headers):
                    candidate_dict[header] = row[i] if i < len(row) else ''
                candidates_list.append(candidate_dict)

            st.success(f"✅ Loaded {len(candidates_list)} candidate(s)")

        except Exception as e:
            st.error(f"❌ Failed to load candidates: {str(e)}")
            st.stop()

    # Filter options
    st.markdown("### 🔍 Filter Candidates")

    col1, col2, col3 = st.columns(3)

    with col1:
        filter_fit = st.multiselect(
            "Fit Label:",
            options=['Strong Fit', 'Good Fit', 'Moderate Fit', 'Weak Fit'],
            default=['Strong Fit', 'Good Fit', 'Moderate Fit', 'Weak Fit']
        )

    with col2:
        filter_approved = st.selectbox(
            "Approval Status:",
            options=['All', 'Approved', 'Pending'],
            index=0
        )

    with col3:
        search_name = st.text_input("Search by name:")

    # Apply filters
    filtered_candidates = candidates_list.copy()

    if filter_fit:
        filtered_candidates = [c for c in filtered_candidates if c.get('auto_fit_label', '') in filter_fit]

    if filter_approved == 'Approved':
        filtered_candidates = [c for c in filtered_candidates if c.get('hr_approved', '') == 'Yes']
    elif filter_approved == 'Pending':
        filtered_candidates = [c for c in filtered_candidates if c.get('hr_approved', '') == 'No']

    if search_name:
        filtered_candidates = [c for c in filtered_candidates if search_name.lower() in c.get('candidate_name', '').lower()]

    st.markdown(f"### 📋 Candidates ({len(filtered_candidates)} shown)")

    # Display candidates with approval checkboxes
    if len(filtered_candidates) > 0:
        for idx, row in enumerate(filtered_candidates):
            with st.expander(f"{'✅' if row['hr_approved'] == 'Yes' else '❌'} {row['candidate_name']} - {row['auto_fit_label']} ({row['auto_fit_score']}%)"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Email:** {row['email']}")
                    st.markdown(f"**Phone:** {row['phone']}")
                    st.markdown(f"**Location:** {row['location']}")
                    st.markdown(f"**Screening Comment:**")
                    st.text(row['auto_screen_comment'])

                with col2:
                    current_approval = row['hr_approved'] == 'Yes'
                    new_approval = st.checkbox(
                        "Approve",
                        value=current_approval,
                        key=f"approve_{idx}"
                    )

                    if new_approval != current_approval:
                        if st.button("💾 Save", key=f"save_{idx}"):
                            try:
                                # Update in Google Sheets (row index + 2 because of header and 0-indexing)
                                row_num = int(idx) + 2
                                col_num = headers.index('hr_approved') + 1
                                worksheet.update_cell(row_num, col_num, 'Yes' if new_approval else 'No')
                                st.success("✅ Updated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Failed to update: {str(e)}")

        # Quick approve/reject actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approve All Filtered", type="primary"):
                try:
                    for idx, candidate in enumerate(filtered_candidates):
                        # Find the actual row in all_data
                        row_num = candidates_list.index(candidate) + 2
                        col_num = headers.index('hr_approved') + 1
                        worksheet.update_cell(row_num, col_num, 'Yes')
                    st.success(f"✅ Approved {len(filtered_candidates)} candidate(s)!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")

        with col2:
            if st.button("❌ Reject All Filtered"):
                try:
                    for idx, candidate in enumerate(filtered_candidates):
                        # Find the actual row in all_data
                        row_num = candidates_list.index(candidate) + 2
                        col_num = headers.index('hr_approved') + 1
                        worksheet.update_cell(row_num, col_num, 'No')
                    st.success(f"❌ Rejected {len(filtered_candidates)} candidate(s)!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")

        # Open Google Sheet button
        if st.session_state.sheet_url:
            st.markdown("---")
            st.markdown(f"[🔗 Open in Google Sheets]({st.session_state.sheet_url})")
    else:
        st.info("ℹ️ No candidates match your filters")

# ============================================================
# SEND NOTIFICATIONS PAGE
# ============================================================
elif page == "📧 Send Notifications":
    st.markdown('<div class="main-header">📧 Send Notifications</div>', unsafe_allow_html=True)

    # Get sheets manager
    sheets_manager = get_sheets_manager()

    if sheets_manager is None:
        st.error("❌ Google Sheets not configured. Please check your credentials.")
        st.stop()

    # Load approved candidates
    with st.spinner("📥 Loading approved candidates..."):
        try:
            approved_candidates = sheets_manager.get_approved_candidates()

            if not approved_candidates:
                st.info("ℹ️ No approved candidates found. Please approve some candidates first.")
                st.stop()

            st.success(f"✅ Found {len(approved_candidates)} approved candidate(s)")

        except Exception as e:
            st.error(f"❌ Failed to load candidates: {str(e)}")
            st.stop()

    # Show approved candidates
    st.markdown("### 👥 Approved Candidates")

    display_data = []
    for c in approved_candidates:
        display_data.append({
            'Name': c.get('candidate_name', ''),
            'Email': c.get('email', ''),
            'Phone': c.get('phone', ''),
            'Role': c.get('role_name', '')
        })
    st.dataframe(display_data, use_container_width=True)

    st.markdown("---")

    # Notification options
    st.markdown("### 📧 Notification Settings")

    col1, col2 = st.columns(2)

    with col1:
        send_email = st.checkbox("Send Emails", value=True)
        if send_email:
            if not os.path.exists('credentials/gmail-credentials.json'):
                st.warning("⚠️ Gmail credentials not found. Email notifications will be skipped.")
                send_email = False

    with col2:
        send_whatsapp = st.checkbox("Send WhatsApp", value=True)
        if send_whatsapp:
            if not os.path.exists('.env'):
                st.warning("⚠️ Twilio credentials not found in .env file. WhatsApp notifications will be skipped.")
                send_whatsapp = False

    # Preview templates
    with st.expander("📄 Preview Email Template"):
        if os.path.exists('templates/email_template.html'):
            with open('templates/email_template.html', 'r', encoding='utf-8') as f:
                email_template = f.read()
            st.code(email_template, language='html')
        else:
            st.warning("⚠️ Email template not found")

    with st.expander("📱 Preview WhatsApp Template"):
        if os.path.exists('templates/whatsapp_template.txt'):
            with open('templates/whatsapp_template.txt', 'r', encoding='utf-8') as f:
                whatsapp_template = f.read()
            st.code(whatsapp_template)
        else:
            st.warning("⚠️ WhatsApp template not found")

    st.markdown("---")

    # Send notifications button
    if st.button("🚀 Send Notifications", type="primary", disabled=not (send_email or send_whatsapp)):

        # Initialize senders
        email_sender = None
        whatsapp_sender = None

        if send_email:
            try:
                email_sender = EmailSender(
                    credentials_file='credentials/gmail-credentials.json',
                    template_file='templates/email_template.html'
                )
                st.success("✅ Email sender initialized")
            except Exception as e:
                st.error(f"❌ Failed to initialize email sender: {str(e)}")
                send_email = False

        if send_whatsapp:
            try:
                whatsapp_sender = WhatsAppSender(template_file='templates/whatsapp_template.txt')
                st.success("✅ WhatsApp sender initialized")
            except Exception as e:
                st.error(f"❌ Failed to initialize WhatsApp sender: {str(e)}")
                send_whatsapp = False

        # Send notifications
        st.markdown("### 📤 Sending Notifications")

        progress_bar = st.progress(0)

        email_success = 0
        email_failed = 0
        whatsapp_success = 0
        whatsapp_failed = 0

        for idx, candidate in enumerate(approved_candidates):
            st.markdown(f"**[{idx + 1}/{len(approved_candidates)}] {candidate['candidate_name']}**")

            # Send email
            if send_email and email_sender:
                try:
                    email_sender.send_candidate_email(
                        to_email=candidate['email'],
                        candidate_name=candidate['candidate_name'],
                        role_name=candidate['role_name']
                    )
                    st.success(f"  ✅ Email sent to {candidate['email']}")
                    email_success += 1
                except Exception as e:
                    st.error(f"  ❌ Email failed: {str(e)}")
                    email_failed += 1

            # Send WhatsApp
            if send_whatsapp and whatsapp_sender:
                try:
                    whatsapp_sender.send_candidate_message(
                        to_phone=candidate['phone'],
                        candidate_name=candidate['candidate_name'],
                        role_name=candidate['role_name']
                    )
                    st.success(f"  ✅ WhatsApp sent to {candidate['phone']}")
                    whatsapp_success += 1
                except Exception as e:
                    st.error(f"  ❌ WhatsApp failed: {str(e)}")
                    whatsapp_failed += 1

            progress_bar.progress((idx + 1) / len(approved_candidates))

        # Summary
        st.markdown("---")
        st.markdown("### 📊 Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Email Sent", email_success)
        with col2:
            st.metric("Email Failed", email_failed)
        with col3:
            st.metric("WhatsApp Sent", whatsapp_success)
        with col4:
            st.metric("WhatsApp Failed", whatsapp_failed)

        if (email_success + whatsapp_success) > 0:
            st.success("🎉 Notification process completed!")

# ============================================================
# SETTINGS PAGE
# ============================================================
elif page == "⚙️ Settings":
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)

    # System information
    st.markdown("### 📊 System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Python Version:**")
        st.code(sys.version)

        st.markdown("**Working Directory:**")
        st.code(os.getcwd())

    with col2:
        st.markdown("**Google Sheets:**")
        if os.path.exists('credentials/service-account.json'):
            st.success("✅ Configured")
        else:
            st.error("❌ Not configured")

        st.markdown("**Gmail API:**")
        if os.path.exists('credentials/gmail-credentials.json'):
            st.success("✅ Configured")
        else:
            st.warning("⚠️ Not configured")

        st.markdown("**Twilio (WhatsApp):**")
        if os.path.exists('.env'):
            st.success("✅ Configured")
        else:
            st.warning("⚠️ Not configured")

    st.markdown("---")

    # File counts
    st.markdown("### 📁 File Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        resume_count = len([f for f in os.listdir('resumes') if f.endswith(('.pdf', '.docx'))]) if os.path.exists('resumes') else 0
        st.metric("Resumes", resume_count)

    with col2:
        jd_count = len([f for f in os.listdir('jd_files') if f.endswith('.txt')]) if os.path.exists('jd_files') else 0
        st.metric("Job Descriptions", jd_count)

    with col3:
        template_count = len([f for f in os.listdir('templates')]) if os.path.exists('templates') else 0
        st.metric("Templates", template_count)

    st.markdown("---")

    # Configuration
    st.markdown("### ⚙️ Configuration")

    # Role settings
    st.markdown("#### Role Settings")
    role_id = st.text_input("Default Role ID:", value="ROLE001")
    role_name = st.text_input("Default Role Name:", value="Python Developer")

    if st.button("💾 Save Role Settings"):
        st.success("✅ Role settings saved!")

    st.markdown("---")

    # Template editor
    st.markdown("### 📝 Edit Templates")

    template_type = st.selectbox(
        "Select Template:",
        ["Email Template", "WhatsApp Template"]
    )

    if template_type == "Email Template":
        if os.path.exists('templates/email_template.html'):
            with open('templates/email_template.html', 'r', encoding='utf-8') as f:
                template_content = f.read()

            edited_content = st.text_area(
                "Edit Email Template:",
                value=template_content,
                height=300,
                help="Use {candidate_name} and {role_name} as placeholders"
            )

            if st.button("💾 Save Email Template"):
                with open('templates/email_template.html', 'w', encoding='utf-8') as f:
                    f.write(edited_content)
                st.success("✅ Email template saved!")
        else:
            st.warning("⚠️ Email template file not found")

    elif template_type == "WhatsApp Template":
        if os.path.exists('templates/whatsapp_template.txt'):
            with open('templates/whatsapp_template.txt', 'r', encoding='utf-8') as f:
                template_content = f.read()

            edited_content = st.text_area(
                "Edit WhatsApp Template:",
                value=template_content,
                height=200,
                help="Use {candidate_name} and {role_name} as placeholders"
            )

            if st.button("💾 Save WhatsApp Template"):
                with open('templates/whatsapp_template.txt', 'w', encoding='utf-8') as f:
                    f.write(edited_content)
                st.success("✅ WhatsApp template saved!")
        else:
            st.warning("⚠️ WhatsApp template file not found")

    st.markdown("---")

    # Clear data
    st.markdown("### 🗑️ Clear Data")

    st.warning("⚠️ Use these actions with caution!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear Resume Folder", type="secondary"):
            if st.checkbox("Confirm clear resumes?"):
                try:
                    for file in os.listdir('resumes'):
                        if file.endswith(('.pdf', '.docx')):
                            os.remove(os.path.join('resumes', file))
                    st.success("✅ Resume folder cleared!")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")

    with col2:
        if st.button("🔄 Reset Session", type="secondary"):
            st.session_state.clear()
            st.success("✅ Session reset!")
            st.rerun()

    st.markdown("---")

    # About
    st.markdown("### ℹ️ About")
    st.info("""
    **Hiring Automation Tool v1.0**

    Phase 1 Features:
    - Resume parsing (PDF/DOCX)
    - Job description matching
    - Google Sheets integration
    - Email notifications (Gmail API)
    - WhatsApp notifications (Twilio)

    Built for Printo with ❤️
    """)
