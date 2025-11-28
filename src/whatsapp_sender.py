"""
WhatsApp Sender Module
Sends WhatsApp messages to candidates using Twilio API.
"""

import os
from twilio.rest import Client
from typing import Dict


class WhatsAppSender:
    """
    Sends WhatsApp messages to candidates using Twilio.
    Requires Twilio account with WhatsApp enabled.
    """

    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initialize the WhatsApp sender.

        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            from_number: Twilio WhatsApp number (format: whatsapp:+14155238886)
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

        # Ensure from_number has whatsapp: prefix
        if not self.from_number.startswith('whatsapp:'):
            self.from_number = f'whatsapp:{self.from_number}'

        print("[OK] WhatsApp sender initialized")

    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a recipient.

        Args:
            to_number: Recipient phone number (format: +1234567890)
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure to_number has whatsapp: prefix and + sign
            if not to_number.startswith('whatsapp:'):
                # Add + if not present
                if not to_number.startswith('+'):
                    print(f"⚠ Warning: Phone number {to_number} should start with '+' for international format")
                    to_number = f'+{to_number}'
                to_number = f'whatsapp:{to_number}'

            # Send message via Twilio
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )

            print(f"[OK] WhatsApp message sent to {to_number} (SID: {message_obj.sid})")
            return True

        except Exception as e:
            print(f"[ERROR] Error sending WhatsApp to {to_number}: {str(e)}")
            return False

    def send_candidate_message(self, candidate: Dict, template_path: str) -> bool:
        """
        Send WhatsApp message to a candidate using a template.

        Args:
            candidate: Candidate information dictionary
            template_path: Path to WhatsApp message template text file

        Returns:
            True if successful, False otherwise
        """
        # Check if candidate has phone number
        phone_number = candidate.get('phone')
        if not phone_number:
            print(f"[ERROR] No phone number found for candidate: {candidate.get('candidate_name')}")
            return False

        # Load message template
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                message_text = file.read()
        except Exception as e:
            print(f"[ERROR] Error loading WhatsApp template: {str(e)}")
            return False

        # Replace placeholders with candidate information
        message_text = message_text.replace('{candidate_name}', candidate.get('candidate_name', 'Candidate'))
        message_text = message_text.replace('{role_name}', candidate.get('role_name', 'Position'))

        # Send message
        return self.send_message(phone_number, message_text)


# Example usage (for testing)
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Initialize sender with Twilio credentials
    sender = WhatsAppSender(
        account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        from_number=os.getenv("TWILIO_WHATSAPP_FROM")
    )

    # Test sending a message
    test_candidate = {
        'candidate_name': 'John Doe',
        'phone': '+1234567890',
        'role_name': 'Python Developer'
    }

    sender.send_candidate_message(test_candidate, "../templates/whatsapp_template.txt")
