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

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

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
from src.auth_pages import show_login_page, show_register_page, show_admin_users_page, show_user_profile
from src.drive_uploader import DriveUploader

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

# ============================================================
# AUTHENTICATION
# ============================================================

# Initialize authentication session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Check authentication
if not st.session_state.authenticated:
    # Show login or register page
    if st.session_state.get('show_register', False):
        show_register_page()
    else:
        show_login_page()
    st.stop()

# User is authenticated - show user profile in sidebar
show_user_profile()

# ============================================================
# MAIN APPLICATION (User is authenticated)
# ============================================================

# Initialize session state
if 'processed_candidates' not in st.session_state:
    st.session_state.processed_candidates = []
if 'sheet_url' not in st.session_state:
    st.session_state.sheet_url = None
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = None

# Sidebar navigation
st.sidebar.title("📋 Navigation")
# Navigation options (add admin option for admins)
nav_options = ["🏠 Home", "📝 Manage Job Descriptions", "🤖 AI Evaluator", "👥 Review Candidates", "📧 Send Notifications", "⚙️ Settings"]
if st.session_state.user_role == 'admin':
    nav_options.append("👥 Admin: Manage Users")

page = st.sidebar.radio(
    "Go to",
    nav_options
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
# MANAGE JOB DESCRIPTIONS PAGE
# ============================================================
elif page == "📝 Manage Job Descriptions":
    st.markdown('<div class="main-header">📝 Manage Job Descriptions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Add, edit, and manage job roles for screening</div>', unsafe_allow_html=True)

    # Ensure jd_library folder exists
    jd_library_path = 'jd_library'
    if not os.path.exists(jd_library_path):
        os.makedirs(jd_library_path)

    # Get all existing JD files
    jd_files = [f for f in os.listdir(jd_library_path) if f.endswith('.txt')]

    st.markdown("### 📚 Existing Job Descriptions")

    if jd_files:
        st.success(f"✅ {len(jd_files)} job description(s) found")

        # Display existing JDs in a table-like format
        for jd_file in sorted(jd_files):
            role_name = jd_file.replace('.txt', '').replace('_', ' ').title()
            jd_path = os.path.join(jd_library_path, jd_file)

            with st.expander(f"📄 {role_name}", expanded=False):
                # Read the JD content
                with open(jd_path, 'r', encoding='utf-8') as f:
                    jd_content = f.read()

                # Edit mode
                edited_content = st.text_area(
                    "Job Description:",
                    value=jd_content,
                    height=300,
                    key=f"edit_{jd_file}"
                )

                col1, col2 = st.columns([1, 4])

                with col1:
                    if st.button("💾 Save", key=f"save_{jd_file}"):
                        with open(jd_path, 'w', encoding='utf-8') as f:
                            f.write(edited_content)
                        st.success(f"✅ Updated {role_name}")
                        st.rerun()

                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{jd_file}"):
                        os.remove(jd_path)
                        st.success(f"✅ Deleted {role_name}")
                        st.rerun()
    else:
        st.info("ℹ️ No job descriptions found. Create your first one below!")

    st.markdown("---")
    st.markdown("### ➕ Add New Job Description")

    # Form to create new JD
    with st.form("new_jd_form"):
        new_role_name = st.text_input(
            "Role Name:",
            placeholder="e.g., Senior Data Analyst",
            help="Enter the job role name"
        )

        new_jd_content = st.text_area(
            "Job Description:",
            height=300,
            placeholder="Paste the full job description here...",
            help="Include all details: responsibilities, requirements, qualifications, etc."
        )

        submit_button = st.form_submit_button("➕ Create Job Description", type="primary")

        if submit_button:
            if not new_role_name:
                st.error("❌ Please enter a role name")
            elif not new_jd_content:
                st.error("❌ Please enter job description content")
            else:
                # Convert role name to filename
                filename = new_role_name.lower().replace(' ', '_').replace('-', '_') + '.txt'
                filepath = os.path.join(jd_library_path, filename)

                # Check if file already exists
                if os.path.exists(filepath):
                    st.error(f"❌ A job description for '{new_role_name}' already exists!")
                else:
                    # Save the new JD
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_jd_content)

                    st.success(f"✅ Created job description: {new_role_name}")
                    st.info(f"📁 Saved as: {filename}")
                    st.balloons()
                    st.rerun()

# ============================================================
# AI EVALUATOR PAGE
# ============================================================
elif page == "🤖 AI Evaluator":
    st.markdown('<div class="main-header">🤖 AI Evaluator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Powered by OpenAI - Intelligent resume evaluation and ranking</div>', unsafe_allow_html=True)

    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("❌ OpenAI API key not found!")
        st.info("""
        **Setup Required:**

        1. Get your API key from: https://platform.openai.com/api-keys
        2. Add it to your `.env` file:
           ```
           OPENAI_API_KEY=your-key-here
           ```
        3. Restart the app

        Or use the command-line tool: `python evaluate_resumes.py`
        """)
        st.stop()

    st.success("✅ OpenAI API key configured")

    # Import evaluator
    try:
        from src.resume_evaluator import ResumeEvaluator
        evaluator = ResumeEvaluator()
    except Exception as e:
        st.error(f"❌ Failed to initialize AI evaluator: {str(e)}")
        st.stop()

    # Job Description Selection
    st.markdown("### 📝 Step 1: Select Job Description")

    # Auto-detect all JD files in jd_library folder
    jd_library_path = 'jd_library'
    if not os.path.exists(jd_library_path):
        os.makedirs(jd_library_path)

    # Get all .txt files in jd_library
    jd_files_list = [f for f in os.listdir(jd_library_path) if f.endswith('.txt')]

    # Create a mapping of display names to filenames
    jd_display_map = {}
    for jd_file in jd_files_list:
        # Convert filename to display name: senior_python_developer.txt -> Senior Python Developer
        display_name = jd_file.replace('.txt', '').replace('_', ' ').title()
        jd_display_map[display_name] = jd_file

    # Also check old jd_files folder for backward compatibility
    if os.path.exists('jd_files/job_description.txt'):
        jd_display_map['Full Stack Developer (Legacy)'] = 'job_description.txt (from jd_files)'

    if not jd_display_map:
        st.warning("⚠️ No job descriptions found!")
        st.info("""
        **How to add job roles:**

        Use the **"📝 Manage Job Descriptions"** page in the sidebar to add new JDs easily!

        Your team can add, edit, and delete job descriptions without touching any files.
        """)

        jd_text = ""
        selected_jd_file = None
        selected_display_name = None
    else:
        # Show success message with count
        st.success(f"✅ Found {len(jd_display_map)} job role(s)")

        # Let user select which role (using display names)
        selected_display_name = st.selectbox(
            "Select the job role you're screening for:",
            options=sorted(jd_display_map.keys()),
            help="Choose which position these resumes are for"
        )

        # Get the actual filename from the display name
        selected_jd_file = jd_display_map[selected_display_name]

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
                key=f"edit_jd_{selected_jd_file}"
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

    # Evaluate Button
    st.markdown("### ⚙️ Step 3: Evaluate & Rank")

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

    if st.button("🤖 AI Evaluate Resumes", type="primary", disabled=not uploaded_files or not jd_text):
        if not uploaded_files:
            st.error("❌ Please upload at least one resume")
        elif not jd_text:
            st.error("❌ Please select or enter a job description")
        else:
            # Save uploaded files temporarily
            temp_resumes = []

            with st.spinner("📤 Processing uploaded files..."):
                for uploaded_file in uploaded_files:
                    file_path = os.path.join('resumes', uploaded_file.name)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())

            # Parse resumes
            with st.spinner("📄 Parsing resumes..."):
                resume_parser = ResumeParser()
                for uploaded_file in uploaded_files:
                    file_path = os.path.join('resumes', uploaded_file.name)
                    try:
                        parsed_data = resume_parser.parse_resume(file_path)
                        if parsed_data and parsed_data.get('resume_text'):
                            temp_resumes.append({
                                'filename': uploaded_file.name,
                                'resume_text': parsed_data['resume_text']
                            })
                    except Exception as e:
                        st.warning(f"⚠️ Could not parse {uploaded_file.name}: {str(e)}")

            if not temp_resumes:
                st.error("❌ No resumes could be parsed successfully")
                st.stop()

            st.success(f"✅ Parsed {len(temp_resumes)} resume(s)")

            # Evaluate with AI
            st.markdown("### 🤖 AI Evaluation in Progress...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                results = []
                for idx, resume in enumerate(temp_resumes):
                    status_text.text(f"Evaluating {idx + 1}/{len(temp_resumes)}: {resume['filename']}")

                    # Extract candidate data (pass JD for relevant experience calculation)
                    candidate_data = evaluator.extract_candidate_data(resume['resume_text'], jd_text)
                    print(f"[DEBUG] Extracted candidate data: {candidate_data}")

                    # Fallback: If AI didn't extract name/phone/email, try traditional parser
                    if not candidate_data.get('name') or not candidate_data.get('phone') or not candidate_data.get('email'):
                        print(f"[DEBUG] AI extraction incomplete, trying fallback parser...")
                        fallback_name = resume_parser.extract_name(resume['resume_text'], resume['filename'])
                        fallback_phone = resume_parser.extract_phone(resume['resume_text'])
                        fallback_email = resume_parser.extract_email(resume['resume_text'])
                        fallback_location = resume_parser.extract_location(resume['resume_text'])

                        # Use fallback values if AI returned None
                        if not candidate_data.get('name') and fallback_name:
                            candidate_data['name'] = fallback_name
                            print(f"[DEBUG] Used fallback name: {fallback_name}")
                        if not candidate_data.get('phone') and fallback_phone:
                            candidate_data['phone'] = fallback_phone
                            print(f"[DEBUG] Used fallback phone: {fallback_phone}")
                        if not candidate_data.get('email') and fallback_email:
                            candidate_data['email'] = fallback_email
                            print(f"[DEBUG] Used fallback email: {fallback_email}")
                        if not candidate_data.get('location') and fallback_location:
                            candidate_data['location'] = fallback_location
                            print(f"[DEBUG] Used fallback location: {fallback_location}")

                    # Evaluate resume
                    evaluation = evaluator.evaluate_resume(resume['resume_text'], jd_text)
                    print(f"[DEBUG] Evaluation result: fit_score={evaluation.get('fit_score')}, fit_label={evaluation.get('fit_label')}")

                    # Combine results
                    result = {
                        'filename': resume['filename'],
                        'candidate_name': candidate_data.get('name'),
                        'email': candidate_data.get('email'),
                        'phone': candidate_data.get('phone'),
                        'location': candidate_data.get('location'),
                        'total_years_experience': candidate_data.get('total_years_experience'),
                        'relevant_years_experience': candidate_data.get('relevant_years_experience'),
                        'experience_brief': candidate_data.get('experience_brief'),
                        'fit_score': evaluation.get('fit_score', 0),
                        'fit_label': evaluation.get('fit_label', 'Unknown'),
                        'reasoning': evaluation.get('reasoning', ''),
                        'strengths': evaluation.get('strengths', []),
                        'gaps': evaluation.get('gaps', [])
                    }
                    print(f"[DEBUG] Combined result: name={result['candidate_name']}, phone={result['phone']}, email={result['email']}, location={result['location']}, total_yrs={result['total_years_experience']}, relevant_yrs={result['relevant_years_experience']}, exp_brief={result['experience_brief']}, score={result['fit_score']}")

                    results.append(result)
                    progress_bar.progress((idx + 1) / len(temp_resumes))

                # Sort by fit_score
                results.sort(key=lambda x: x['fit_score'], reverse=True)

                # Store results and JD info in session state for the save button
                st.session_state.ai_eval_results = results
                st.session_state.ai_eval_jd_name = selected_jd_file.replace('.txt', '').replace('_', ' ').title() if 'selected_jd_file' in locals() else 'AI Evaluation'

                status_text.text("✅ Evaluation complete!")

            except Exception as e:
                st.error(f"❌ Evaluation failed: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    # Display Results (moved outside button block to persist across reruns)
    if 'ai_eval_results' in st.session_state and st.session_state.ai_eval_results:
        results = st.session_state.ai_eval_results

        st.markdown("---")
        st.markdown("### 📊 Evaluation Results")

        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Candidates", len(results))
        with col2:
            avg_score = sum(r['fit_score'] for r in results) / len(results) if results else 0
            st.metric("Average Score", f"{avg_score:.1f}/5")
        with col3:
            strong_matches = sum(1 for r in results if r['fit_score'] >= 4)
            st.metric("Strong Matches (4-5)", strong_matches)
        with col4:
            top_score = results[0]['fit_score'] if results else 0
            st.metric("Top Score", f"{top_score}/5")

        st.markdown("---")

        # Detailed results
        for idx, result in enumerate(results):
            rank = idx + 1

            # Color code by score
            if result['fit_score'] >= 4:
                header_emoji = "🌟"
            elif result['fit_score'] >= 3:
                header_emoji = "✅"
            elif result['fit_score'] >= 2:
                header_emoji = "⚠️"
            else:
                header_emoji = "❌"

            with st.expander(f"{header_emoji} Rank #{rank}: {result['candidate_name'] or 'Unknown'} - {result['fit_score']}/5 ({result['fit_label']})", expanded=(idx < 3)):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Email:** {result['email'] or 'N/A'}")
                    st.markdown(f"**Phone:** {result['phone'] or 'N/A'}")
                    st.markdown(f"**Location:** {result['location'] or 'N/A'}")
                    st.markdown(f"**Experience:** {result.get('experience_brief') or 'N/A'}")

                    # Show years of experience
                    total_yrs = result.get('total_years_experience')
                    relevant_yrs = result.get('relevant_years_experience')
                    if total_yrs is not None:
                        exp_text = f"{total_yrs} years total"
                        if relevant_yrs is not None:
                            exp_text += f" ({relevant_yrs} years relevant)"
                        st.markdown(f"**Years:** {exp_text}")

                    st.markdown("**Reasoning:**")
                    st.info(result['reasoning'])

                    if result['strengths']:
                        st.markdown("**Strengths:**")
                        for strength in result['strengths']:
                            st.markdown(f"- ✓ {strength}")

                    if result['gaps'] and result['gaps'] != ['None']:
                        st.markdown("**Gaps/Concerns:**")
                        for gap in result['gaps']:
                            st.markdown(f"- ✗ {gap}")

                with col2:
                    st.markdown(f"### {result['fit_score']}/5")
                    st.markdown(f"**{result['fit_label']}**")
                    st.markdown(f"📄 {result['filename']}")

        # Download results and save to Google Sheets
        st.markdown("---")
        st.markdown("### 💾 Save & Export Results")

        col1, col2 = st.columns(2)

        with col1:
            import json
            json_data = json.dumps(results, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="evaluation_results.json",
                mime="application/json"
            )

        with col2:
            if st.button("📊 Save to Google Sheets", type="primary", key="save_to_sheets_btn"):
                with st.spinner("💾 Saving to Google Sheets..."):
                    try:
                        # Get results from session state
                        if 'ai_eval_results' not in st.session_state:
                            st.error("❌ No evaluation results found. Please run evaluation first.")
                        else:
                            results_to_save = st.session_state.ai_eval_results
                            jd_name = st.session_state.get('ai_eval_jd_name', 'AI Evaluation')

                            # Get sheets manager
                            sheets_manager = get_sheets_manager()

                            if sheets_manager is None:
                                st.error("❌ Google Sheets not configured")
                            else:
                                # Initialize Drive uploader
                                try:
                                    drive_uploader = DriveUploader(
                                        credentials_path='credentials/service-account.json',
                                        folder_id='1hqK7adC5NKJU2bbAyT24Mc9XhRyBIkIz'
                                    )
                                    print("[OK] Drive uploader initialized")
                                except Exception as e:
                                    print(f"[ERROR] Failed to initialize Drive uploader: {str(e)}")
                                    drive_uploader = None

                                # Convert results to format expected by sheets manager
                                candidates_to_save = []
                                for result in results_to_save:
                                    # Use the AI-extracted experience brief
                                    experience_brief = result.get('experience_brief') or 'N/A'

                                    # Create detailed auto screen comment
                                    auto_screen_comment = f"DECISION: {result['fit_label']}\n\n"
                                    auto_screen_comment += f"REASONING: {result['reasoning']}\n\n"

                                    if result['strengths']:
                                        auto_screen_comment += f"HIGHLIGHTS:\n"
                                        for strength in result['strengths']:
                                            auto_screen_comment += f"✓ {strength}\n"
                                        auto_screen_comment += "\n"

                                    if result['gaps'] and result['gaps'] != ['None']:
                                        auto_screen_comment += f"MISSING SKILLS/GAPS:\n"
                                        for gap in result['gaps']:
                                            auto_screen_comment += f"✗ {gap}\n"

                                    # Upload resume to Google Drive
                                    resume_link = ''
                                    if drive_uploader:
                                        try:
                                            # Find the resume file path
                                            resume_file_path = os.path.join('resumes', result['filename'])
                                            if os.path.exists(resume_file_path):
                                                resume_link = drive_uploader.upload_resume(
                                                    file_path=resume_file_path,
                                                    candidate_name=result['candidate_name'] or 'Unknown',
                                                    job_role=jd_name
                                                )
                                        except Exception as e:
                                            print(f"[ERROR] Failed to upload resume to Drive: {str(e)}")

                                    candidate = {
                                        'role_id': f"AI_{datetime.now().strftime('%Y%m%d')}",
                                        'role_name': jd_name,
                                        'candidate_name': result['candidate_name'] or 'Unknown',
                                        'phone': result['phone'] or '',
                                        'email': result['email'] or '',
                                        'location': result['location'] or '',
                                        'source_portal': 'AI Evaluator',
                                        'experience_brief': experience_brief,
                                        'total_years_experience': result.get('total_years_experience') or '',
                                        'relevant_years_experience': result.get('relevant_years_experience') or '',
                                        'ai_score_0_5': result['fit_score'],  # Raw AI score (0-5)
                                        'auto_fit_score': result['fit_score'] * 20,  # Convert 0-5 to 0-100
                                        'auto_fit_label': result['fit_label'],
                                        'auto_screen_comment': auto_screen_comment,
                                        'screened_by': st.session_state.get('user_email', 'Unknown'),  # Capture who did the screening
                                        'resume_link': resume_link  # Google Drive link
                                    }
                                    candidates_to_save.append(candidate)

                                # Save to sheets
                                sheets_manager.add_multiple_candidates(candidates_to_save)
                                sheet_url = sheets_manager.get_sheet_url()
                                st.session_state.sheet_url = sheet_url
                                st.session_state.save_success = True
                                st.session_state.saved_count = len(candidates_to_save)

                                # Show success message
                                st.markdown("---")
                                st.success(f"✅ {len(candidates_to_save)} candidate(s) saved to Google Sheets!")
                                st.markdown(f"### [🔗 Open Google Sheet]({sheet_url})")
                                st.balloons()

                    except Exception as e:
                        st.error(f"❌ Failed to save to Google Sheets: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())

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
elif page == "👥 Admin: Manage Users":
    show_admin_users_page()

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
