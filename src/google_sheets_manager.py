"""
Google Sheets Manager Module
Handles all interactions with Google Sheets API for storing candidate data.
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import List, Dict, Optional


class GoogleSheetsManager:
    """
    Manages Google Sheets operations for the hiring automation system.
    Creates and updates the Candidates_Master sheet.
    """

    def __init__(self, credentials_path: str):
        """
        Initialize the Google Sheets manager.

        Args:
            credentials_path: Path to the Google service account JSON credentials file
        """
        # Define the scopes needed for Google Sheets API
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # Authenticate and create client
        self.credentials = Credentials.from_service_account_file(
            credentials_path,
            scopes=self.scopes
        )
        self.client = gspread.authorize(self.credentials)
        self.sheet = None

    def get_or_create_sheet(self, sheet_name: str = "Hiring_Automation_Phase1") -> gspread.Spreadsheet:
        """
        Get existing Google Sheet or create a new one.

        Args:
            sheet_name: Name of the Google Sheet to create/open

        Returns:
            The Google Spreadsheet object
        """
        try:
            # Try to open existing spreadsheet
            self.sheet = self.client.open(sheet_name)
            print(f"[OK] Opened existing Google Sheet: {sheet_name}")
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet if it doesn't exist
            self.sheet = self.client.create(sheet_name)
            print(f"[OK] Created new Google Sheet: {sheet_name}")

        return self.sheet

    def setup_candidates_master_sheet(self) -> gspread.Worksheet:
        """
        Set up the Candidates_Master worksheet with proper headers.
        Creates the worksheet if it doesn't exist, or gets it if it does.

        Returns:
            The Candidates_Master worksheet
        """
        try:
            # Try to get existing worksheet
            worksheet = self.sheet.worksheet("Candidates_Master")
            print("[OK] Found existing Candidates_Master sheet")
        except gspread.WorksheetNotFound:
            # Create new worksheet if it doesn't exist
            worksheet = self.sheet.add_worksheet(
                title="Candidates_Master",
                rows="1000",
                cols="13"
            )
            print("[OK] Created new Candidates_Master sheet")

            # Add headers
            headers = [
                "role_id",
                "role_name",
                "candidate_name",
                "phone",
                "email",
                "location",
                "source_portal",
                "auto_fit_score",
                "auto_fit_label",
                "auto_screen_comment",
                "hr_approved",
                "created_at",
                "updated_at"
            ]

            # Write headers to first row
            worksheet.update('A1:M1', [headers])

            # Format headers (bold)
            worksheet.format('A1:M1', {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
            })

            print("[OK] Added headers to Candidates_Master sheet")

        return worksheet

    def add_candidate(self, candidate_data: Dict) -> bool:
        """
        Add a single candidate to the Candidates_Master sheet.

        Args:
            candidate_data: Dictionary containing candidate information

        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self.setup_candidates_master_sheet()

            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Prepare row data (must match header order)
            row_data = [
                candidate_data.get('role_id', ''),
                candidate_data.get('role_name', ''),
                candidate_data.get('candidate_name', ''),
                candidate_data.get('phone', ''),
                candidate_data.get('email', ''),
                candidate_data.get('location', ''),
                candidate_data.get('source_portal', 'Local Resume'),
                candidate_data.get('auto_fit_score', 0),
                candidate_data.get('auto_fit_label', ''),
                candidate_data.get('auto_screen_comment', ''),
                'No',  # hr_approved default value
                timestamp,  # created_at
                timestamp   # updated_at
            ]

            # Append the row to the sheet
            worksheet.append_row(row_data)
            print(f"[OK] Added candidate: {candidate_data.get('candidate_name', 'Unknown')}")
            return True

        except Exception as e:
            print(f"[ERROR] Error adding candidate: {str(e)}")
            return False

    def add_multiple_candidates(self, candidates_list: List[Dict]) -> int:
        """
        Add multiple candidates to the Candidates_Master sheet in batch.
        More efficient than adding one by one.

        Args:
            candidates_list: List of candidate dictionaries

        Returns:
            Number of candidates successfully added
        """
        try:
            worksheet = self.setup_candidates_master_sheet()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Prepare all rows
            rows_data = []
            for candidate_data in candidates_list:
                row_data = [
                    candidate_data.get('role_id', ''),
                    candidate_data.get('role_name', ''),
                    candidate_data.get('candidate_name', ''),
                    candidate_data.get('phone', ''),
                    candidate_data.get('email', ''),
                    candidate_data.get('location', ''),
                    candidate_data.get('source_portal', 'Local Resume'),
                    candidate_data.get('auto_fit_score', 0),
                    candidate_data.get('auto_fit_label', ''),
                    candidate_data.get('auto_screen_comment', ''),
                    'No',  # hr_approved
                    timestamp,  # created_at
                    timestamp   # updated_at
                ]
                rows_data.append(row_data)

            # Batch append all rows
            worksheet.append_rows(rows_data)
            print(f"[OK] Added {len(rows_data)} candidates to the sheet")
            return len(rows_data)

        except Exception as e:
            print(f"[ERROR] Error adding candidates: {str(e)}")
            return 0

    def get_approved_candidates(self) -> List[Dict]:
        """
        Retrieve all candidates where hr_approved = 'Yes'.
        Used by the notification script.

        Returns:
            List of candidate dictionaries with hr_approved = 'Yes'
        """
        try:
            worksheet = self.setup_candidates_master_sheet()

            # Get all records as list of dictionaries
            all_records = worksheet.get_all_records()

            # Filter for approved candidates
            approved_candidates = [
                record for record in all_records
                if record.get('hr_approved', '').strip().lower() == 'yes'
            ]

            print(f"[OK] Found {len(approved_candidates)} approved candidates")
            return approved_candidates

        except Exception as e:
            print(f"[ERROR] Error retrieving approved candidates: {str(e)}")
            return []

    def get_sheet_url(self) -> Optional[str]:
        """
        Get the URL of the Google Sheet for easy access.

        Returns:
            URL string or None if sheet not initialized
        """
        if self.sheet:
            return self.sheet.url
        return None


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Initialize the manager
    manager = GoogleSheetsManager("../credentials/service-account.json")

    # Create/get the sheet
    sheet = manager.get_or_create_sheet("Hiring_Automation_Phase1")

    # Setup Candidates_Master worksheet
    manager.setup_candidates_master_sheet()

    # Test adding a candidate
    test_candidate = {
        'role_id': 'ROLE001',
        'role_name': 'Python Developer',
        'candidate_name': 'John Doe',
        'phone': '+1234567890',
        'email': 'john@example.com',
        'location': 'New York',
        'auto_fit_score': 85,
        'auto_fit_label': 'Good Fit',
        'auto_screen_comment': 'Strong Python skills'
    }

    manager.add_candidate(test_candidate)

    print(f"\nGoogle Sheet URL: {manager.get_sheet_url()}")
