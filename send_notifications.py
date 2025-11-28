"""
Send Notifications Script - Phase 1
Sends email and WhatsApp messages to HR-approved candidates.

Usage:
    python send_notifications.py

This script will:
1. Read the Candidates_Master sheet from Google Sheets
2. Filter for candidates with hr_approved = 'Yes'
3. Send email and WhatsApp messages to approved candidates
"""

import os
import sys
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from google_sheets_manager import GoogleSheetsManager
from email_sender import EmailSender
from whatsapp_sender import WhatsAppSender


def main():
    """
    Main function to send notifications to approved candidates.
    """
    print("=" * 60)
    print("HIRING AUTOMATION - PHASE 1: SEND NOTIFICATIONS")
    print("=" * 60)
    print()

    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    CREDENTIALS_FILE = "credentials/service-account.json"
    GMAIL_CREDENTIALS_FILE = "credentials/gmail-credentials.json"
    TOKEN_FILE = "credentials/token.json"
    EMAIL_TEMPLATE = "templates/email_template.html"
    WHATSAPP_TEMPLATE = "templates/whatsapp_template.txt"
    SHEET_NAME = "Hiring_Automation_Phase1"

    # Twilio configuration from environment
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

    # Validation
    print("Step 1: Validating setup...")
    print("-" * 60)

    if not os.path.exists(CREDENTIALS_FILE):
        print(f"[ERROR] Error: Google credentials file '{CREDENTIALS_FILE}' not found")
        return

    if not os.path.exists(GMAIL_CREDENTIALS_FILE):
        print(f"[ERROR] Error: Gmail credentials file '{GMAIL_CREDENTIALS_FILE}' not found")
        print(f"  Please follow README instructions to set up Gmail API")
        return

    if not os.path.exists(EMAIL_TEMPLATE):
        print(f"[ERROR] Error: Email template '{EMAIL_TEMPLATE}' not found")
        return

    if not os.path.exists(WHATSAPP_TEMPLATE):
        print(f"[ERROR] Error: WhatsApp template '{WHATSAPP_TEMPLATE}' not found")
        return

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_FROM:
        print("⚠ Warning: Twilio credentials not found in .env file")
        print("  WhatsApp messages will be skipped")
        send_whatsapp = False
    else:
        send_whatsapp = True

    print("[OK] All required files found")
    print()

    # Step 2: Initialize components
    print("Step 2: Initializing components...")
    print("-" * 60)

    try:
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsManager(CREDENTIALS_FILE)
        sheet = sheets_manager.get_or_create_sheet(SHEET_NAME)
        print("[OK] Google Sheets manager initialized")

        # Initialize email sender
        email_sender = EmailSender(GMAIL_CREDENTIALS_FILE, TOKEN_FILE)
        print("[OK] Email sender initialized")

        # Initialize WhatsApp sender if credentials available
        if send_whatsapp:
            whatsapp_sender = WhatsAppSender(
                TWILIO_ACCOUNT_SID,
                TWILIO_AUTH_TOKEN,
                TWILIO_WHATSAPP_FROM
            )
            print("[OK] WhatsApp sender initialized")
        else:
            whatsapp_sender = None

        print()

    except Exception as e:
        print(f"[ERROR] Error during initialization: {str(e)}")
        return

    # Step 3: Retrieve approved candidates
    print("Step 3: Retrieving approved candidates from Google Sheets...")
    print("-" * 60)

    try:
        approved_candidates = sheets_manager.get_approved_candidates()

        if len(approved_candidates) == 0:
            print("⚠ No approved candidates found (hr_approved = 'Yes')")
            print()
            print("Action Required:")
            print("1. Open the Google Sheet")
            print("2. Change 'hr_approved' from 'No' to 'Yes' for candidates you want to contact")
            print("3. Run this script again")
            print()
            print(f"Google Sheet URL: {sheets_manager.get_sheet_url()}")
            return

        print(f"[OK] Found {len(approved_candidates)} approved candidate(s)")
        print()

    except Exception as e:
        print(f"[ERROR] Error retrieving candidates: {str(e)}")
        return

    # Step 4: Send notifications
    print("Step 4: Sending notifications...")
    print("-" * 60)

    email_success_count = 0
    whatsapp_success_count = 0

    for i, candidate in enumerate(approved_candidates, 1):
        print(f"\n[{i}/{len(approved_candidates)}] Processing: {candidate.get('candidate_name', 'Unknown')}")
        print("-" * 40)

        # Send email
        try:
            if email_sender.send_candidate_email(candidate, EMAIL_TEMPLATE):
                email_success_count += 1
        except Exception as e:
            print(f"  [ERROR] Email error: {str(e)}")

        # Send WhatsApp (if enabled)
        if send_whatsapp and whatsapp_sender:
            try:
                if whatsapp_sender.send_candidate_message(candidate, WHATSAPP_TEMPLATE):
                    whatsapp_success_count += 1
            except Exception as e:
                print(f"  [ERROR] WhatsApp error: {str(e)}")

    # Step 5: Summary
    print()
    print("=" * 60)
    print("[OK] NOTIFICATION PROCESS COMPLETED")
    print("=" * 60)
    print(f"Total approved candidates: {len(approved_candidates)}")
    print(f"Emails sent successfully: {email_success_count}")

    if send_whatsapp:
        print(f"WhatsApp messages sent successfully: {whatsapp_success_count}")

    print()

    if email_success_count < len(approved_candidates):
        print("⚠ Some notifications failed. Check the logs above for details.")
        print()


if __name__ == "__main__":
    main()
