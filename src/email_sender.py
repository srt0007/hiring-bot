"""
Email Sender Module
Sends emails to candidates using Gmail API.
"""

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, Optional


class EmailSender:
    """
    Sends emails to candidates using Gmail API.
    Supports HTML email templates.
    """

    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self, credentials_path: str, token_path: str = 'credentials/token.json'):
        """
        Initialize the email sender.

        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load the token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Gmail API using OAuth2.

        Returns:
            Gmail API service instance
        """
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e:
                print(f"⚠ Error loading token: {str(e)}")

        # If no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                creds.refresh(Request())
            else:
                # Get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            print("[OK] Gmail authentication successful")

        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)
        return service

    def create_message(self, to: str, subject: str, body: str,
                      from_email: Optional[str] = None) -> Dict:
        """
        Create an email message.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (can include HTML)
            from_email: Sender email (uses authenticated account if None)

        Returns:
            Message dictionary ready to send
        """
        message = MIMEMultipart('alternative')
        message['To'] = to
        message['Subject'] = subject

        if from_email:
            message['From'] = from_email

        # Add HTML body
        html_part = MIMEText(body, 'html')
        message.attach(html_part)

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        return {'raw': raw_message}

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
        Send an email to a recipient.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (HTML format)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            message = self.create_message(to, subject, body)

            # Send message
            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()

            print(f"[OK] Email sent to {to} (Message ID: {result['id']})")
            return True

        except Exception as e:
            print(f"[ERROR] Error sending email to {to}: {str(e)}")
            return False

    def send_candidate_email(self, candidate: Dict, template_path: str) -> bool:
        """
        Send email to a candidate using a template.

        Args:
            candidate: Candidate information dictionary
            template_path: Path to email template HTML file

        Returns:
            True if successful, False otherwise
        """
        # Load email template
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                email_body = file.read()
        except Exception as e:
            print(f"[ERROR] Error loading email template: {str(e)}")
            return False

        # Replace placeholders with candidate information
        email_body = email_body.replace('{candidate_name}', candidate.get('candidate_name', 'Candidate'))
        email_body = email_body.replace('{role_name}', candidate.get('role_name', 'Position'))

        # Email subject
        subject = f"Interview Invitation - {candidate.get('role_name', 'Position')}"

        # Send email
        recipient_email = candidate.get('email')
        if not recipient_email:
            print(f"[ERROR] No email found for candidate: {candidate.get('candidate_name')}")
            return False

        return self.send_email(recipient_email, subject, email_body)


# Example usage (for testing)
if __name__ == "__main__":
    # Initialize sender
    sender = EmailSender(
        credentials_path="../credentials/gmail-credentials.json",
        token_path="../credentials/token.json"
    )

    # Test sending an email
    test_candidate = {
        'candidate_name': 'John Doe',
        'email': 'john@example.com',
        'role_name': 'Python Developer'
    }

    sender.send_candidate_email(test_candidate, "../templates/email_template.html")
