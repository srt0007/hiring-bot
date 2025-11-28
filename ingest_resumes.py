"""
Resume Ingestion Script - Phase 1
Main script to process resumes and populate Google Sheets.

Usage:
    python ingest_resumes.py

This script will:
1. Read the JD file from jd_files folder
2. Parse all resumes from resumes folder
3. Match candidates against JD keywords
4. Save results to Google Sheets (Candidates_Master)
"""

import os
import sys
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from resume_parser import ResumeParser
from jd_matcher import JDMatcher
from google_sheets_manager import GoogleSheetsManager


def main():
    """
    Main function to orchestrate the resume ingestion process.
    """
    print("=" * 60)
    print("HIRING AUTOMATION - PHASE 1: RESUME INGESTION")
    print("=" * 60)
    print()

    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    RESUMES_FOLDER = "resumes"
    JD_FILE = "jd_files/job_description.txt"
    CREDENTIALS_FILE = "credentials/service-account.json"
    SHEET_NAME = "Hiring_Automation_Phase1"

    # Get role information from environment or use defaults
    ROLE_ID = os.getenv("ROLE_ID", "ROLE001")
    ROLE_NAME = os.getenv("ROLE_NAME", "Software Developer")

    # Validation: Check if required files and folders exist
    print("Step 1: Validating setup...")
    print("-" * 60)

    if not os.path.exists(RESUMES_FOLDER):
        print(f"[ERROR] Error: Resumes folder '{RESUMES_FOLDER}' not found")
        print(f"  Please create the folder and add resume files (PDF or DOCX)")
        return

    if not os.path.exists(JD_FILE):
        print(f"[ERROR] Error: Job description file '{JD_FILE}' not found")
        print(f"  Please create the file with the job description")
        return

    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] Error: Google credentials file '{CREDENTIALS_FILE}' not found")
        print(f"  Please follow README instructions to set up Google Sheets API")
        return

    # Count resume files
    resume_files = [f for f in os.listdir(RESUMES_FOLDER)
                    if f.endswith(('.pdf', '.docx'))]

    if len(resume_files) == 0:
        print(f"[ERROR] Error: No resume files found in '{RESUMES_FOLDER}'")
        print(f"  Please add PDF or DOCX resume files")
        return

    print(f"[OK] Found {len(resume_files)} resume(s) to process")
    print(f"[OK] JD file found: {JD_FILE}")
    print(f"[OK] Credentials file found: {CREDENTIALS_FILE}")
    print()

    # Step 2: Initialize components
    print("Step 2: Initializing components...")
    print("-" * 60)

    try:
        # Initialize resume parser
        parser = ResumeParser()
        print("[OK] Resume parser initialized")

        # Initialize JD matcher
        matcher = JDMatcher(JD_FILE)
        print(f"[OK] JD matcher initialized ({len(matcher.jd_keywords)} keywords extracted)")

        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsManager(CREDENTIALS_FILE)
        print("[OK] Google Sheets manager initialized")

        # Create/open Google Sheet
        sheet = sheets_manager.get_or_create_sheet(SHEET_NAME)
        print()

    except Exception as e:
        print(f"[ERROR] Error during initialization: {str(e)}")
        return

    # Step 3: Parse resumes
    print("Step 3: Parsing resumes...")
    print("-" * 60)

    try:
        candidates = parser.parse_multiple_resumes(RESUMES_FOLDER)

        if len(candidates) == 0:
            print("[ERROR] No candidates were successfully parsed")
            return

        print()

    except Exception as e:
        print(f"[ERROR] Error parsing resumes: {str(e)}")
        return

    # Step 4: Evaluate candidates against JD
    print("Step 4: Evaluating candidates against JD...")
    print("-" * 60)

    try:
        evaluated_candidates = matcher.evaluate_multiple_candidates(candidates)

        # Add role information to each candidate
        for candidate in evaluated_candidates:
            candidate['role_id'] = ROLE_ID
            candidate['role_name'] = ROLE_NAME
            candidate['source_portal'] = 'Local Resume'

        print()

    except Exception as e:
        print(f"[ERROR] Error evaluating candidates: {str(e)}")
        return

    # Step 5: Save to Google Sheets
    print("Step 5: Saving to Google Sheets...")
    print("-" * 60)

    try:
        count = sheets_manager.add_multiple_candidates(evaluated_candidates)

        if count > 0:
            print()
            print("=" * 60)
            print("[OK] SUCCESS: Resume ingestion completed!")
            print("=" * 60)
            print(f"Total candidates processed: {count}")
            print(f"Google Sheet URL: {sheets_manager.get_sheet_url()}")
            print()
            print("Next Steps:")
            print("1. Open the Google Sheet and review candidate information")
            print("2. Change 'hr_approved' from 'No' to 'Yes' for candidates you want to contact")
            print("3. Run the notification script: python send_notifications.py")
            print()
        else:
            print("[ERROR] Failed to save candidates to Google Sheets")

    except Exception as e:
        print(f"[ERROR] Error saving to Google Sheets: {str(e)}")
        return


if __name__ == "__main__":
    main()
