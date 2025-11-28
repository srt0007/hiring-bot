"""
Hiring Automation Tool - Phase 1
Core modules for resume processing and candidate notification.
"""

__version__ = "1.0.0"
__author__ = "Hiring Automation Team"

# Import main classes for easy access
from .resume_parser import ResumeParser
from .jd_matcher import JDMatcher
from .google_sheets_manager import GoogleSheetsManager
from .email_sender import EmailSender
from .whatsapp_sender import WhatsAppSender

__all__ = [
    'ResumeParser',
    'JDMatcher',
    'GoogleSheetsManager',
    'EmailSender',
    'WhatsAppSender'
]
