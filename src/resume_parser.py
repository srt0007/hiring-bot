"""
Resume Parser Module
Extracts candidate information from PDF and DOCX resume files.
Supports OCR for image-based PDFs.
"""

import re
import os
import base64
import requests
from typing import Dict, Optional
import PyPDF2
import docx
import phonenumbers

# Try to import local OCR libraries (faster if available)
LOCAL_OCR_AVAILABLE = False
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image

    # Set Tesseract path for Windows
    if os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        LOCAL_OCR_AVAILABLE = True
        print("[INFO] Local Tesseract OCR detected - will use for faster processing")
except ImportError:
    print("[INFO] Local OCR not available - will use cloud OCR API")

# Cloud OCR - always available as backup
CLOUD_OCR_AVAILABLE = True


class ResumeParser:
    """
    Parses resume files (PDF and DOCX) to extract candidate information.
    Extracts: name, email, phone, and location (best effort).
    """

    def __init__(self):
        """Initialize the resume parser."""
        # Common email pattern
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

        # Common phone patterns (supports various formats)
        self.phone_patterns = [
            re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'),
            re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
        ]

        # Location keywords (cities, states, countries - extend as needed)
        self.location_keywords = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'San Francisco', 'Seattle', 'Boston', 'Austin', 'Denver',
            'California', 'Texas', 'Florida', 'New York', 'Illinois',
            'India', 'USA', 'UK', 'Canada', 'Australia',
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune',
            'Remote', 'Willing to relocate'
        ]

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.
        Ignores images and only extracts text layers.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text as string
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Extract text from all pages, ignoring errors
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            text += page_text + "\n"
                    except Exception as page_error:
                        # Skip pages that can't be read (images, etc.)
                        print(f"[WARN] Skipping page {page_num + 1}: {str(page_error)}")
                        continue

            # Check if we got any text
            if not text.strip():
                print(f"[WARN] No text extracted from PDF {file_path}. Attempting OCR...")
                # Try OCR if available
                return self.extract_text_with_ocr(file_path)

            return text
        except Exception as e:
            print(f"[ERROR] Error reading PDF {file_path}: {str(e)}")
            return ""

    def extract_text_with_local_ocr(self, file_path: str) -> str:
        """
        Extract text from image-based PDF using local Tesseract OCR.
        Faster than cloud OCR (3-5 seconds per page vs 10 seconds total).

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text as string
        """
        if not LOCAL_OCR_AVAILABLE:
            return ""

        try:
            print(f"[INFO] Starting local OCR extraction for {file_path}...")

            # Convert PDF pages to images
            images = convert_from_path(file_path, dpi=300)
            print(f"[INFO] Converted {len(images)} pages to images")

            text = ""
            # OCR each page
            for page_num, image in enumerate(images):
                try:
                    print(f"[INFO] OCR processing page {page_num + 1}/{len(images)}...")
                    page_text = pytesseract.image_to_string(image, lang='eng')
                    if page_text.strip():
                        text += page_text + "\n"
                except Exception as page_error:
                    print(f"[WARN] Local OCR failed for page {page_num + 1}: {str(page_error)}")
                    continue

            if text.strip():
                print(f"[OK] Local OCR extracted {len(text)} characters from {file_path}")
                return text
            else:
                print(f"[WARN] Local OCR extracted no text from {file_path}")
                return ""

        except Exception as e:
            print(f"[ERROR] Local OCR processing failed for {file_path}: {str(e)}")
            return ""

    def extract_text_with_ocr(self, file_path: str) -> str:
        """
        Extract text from image-based PDF using OCR.
        Tries local Tesseract OCR first (faster), then cloud OCR as backup.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text as string
        """
        # Try local OCR first (much faster: 3-5 sec/page)
        if LOCAL_OCR_AVAILABLE:
            text = self.extract_text_with_local_ocr(file_path)
            if text.strip():
                return text
            print(f"[INFO] Local OCR failed, trying cloud OCR...")

        # Fallback to cloud OCR
        if not CLOUD_OCR_AVAILABLE:
            print(f"[ERROR] No OCR method available")
            return ""

        try:
            print(f"[INFO] Starting cloud OCR extraction for {file_path}...")

            # Read PDF file as base64
            with open(file_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode()

            # Use OCR.space free API (25,000 requests/month)
            # Free API key - no registration needed for basic usage
            api_url = 'https://api.ocr.space/parse/image'

            payload = {
                'base64Image': f'data:application/pdf;base64,{pdf_content}',
                'language': 'eng',
                'isOverlayRequired': False,
                'detectOrientation': True,
                'scale': True,
                'OCREngine': 2,  # Engine 2 is better for documents
                'filetype': 'PDF'
            }

            # Free API key (no registration needed)
            headers = {
                'apikey': 'helloworld'  # Free tier API key
            }

            print(f"[INFO] Sending PDF to cloud OCR service...")
            response = requests.post(api_url, data=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                result = response.json()

                if result.get('IsErroredOnProcessing'):
                    error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
                    print(f"[ERROR] OCR API error: {error_msg}")
                    return ""

                # Extract text from all pages
                text = ""
                if 'ParsedResults' in result:
                    for page_result in result['ParsedResults']:
                        page_text = page_result.get('ParsedText', '')
                        if page_text.strip():
                            text += page_text + "\n"

                if text.strip():
                    print(f"[OK] Cloud OCR extracted {len(text)} characters from {file_path}")
                    return text
                else:
                    print(f"[WARN] OCR extracted no text from {file_path}")
                    return ""
            else:
                print(f"[ERROR] OCR API returned status code: {response.status_code}")
                return ""

        except requests.exceptions.Timeout:
            print(f"[ERROR] OCR request timed out for {file_path}")
            return ""
        except Exception as e:
            print(f"[ERROR] Cloud OCR processing failed for {file_path}: {str(e)}")
            return ""

    def extract_text_from_docx(self, file_path: str) -> str:
        """
        Extract text content from a DOCX file.

        Args:
            file_path: Path to the DOCX file

        Returns:
            Extracted text as string
        """
        try:
            doc = docx.Document(file_path)
            # Extract text from all paragraphs
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"[ERROR] Error reading DOCX {file_path}: {str(e)}")
            return ""

    def extract_email(self, text: str) -> Optional[str]:
        """
        Extract email address from text.

        Args:
            text: Text to search for email

        Returns:
            First email found, or None
        """
        match = self.email_pattern.search(text)
        if match:
            return match.group(0).lower()
        return None

    def extract_phone(self, text: str) -> Optional[str]:
        """
        Extract phone number from text.
        Attempts to parse and format using phonenumbers library.

        Args:
            text: Text to search for phone number

        Returns:
            First phone number found, or None
        """
        # Try each pattern
        for pattern in self.phone_patterns:
            matches = pattern.findall(text)
            if matches:
                # Try to parse and format the first match
                phone_text = matches[0]
                try:
                    # Try to parse with default region
                    for region in ['US', 'IN', 'GB']:
                        try:
                            phone_number = phonenumbers.parse(phone_text, region)
                            if phonenumbers.is_valid_number(phone_number):
                                # Return in international format
                                return phonenumbers.format_number(
                                    phone_number,
                                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                                )
                        except:
                            continue
                    # If parsing fails, return as is (cleaned)
                    return phone_text.strip()
                except:
                    return phone_text.strip()
        return None

    def extract_name(self, text: str, filename: str) -> str:
        """
        Extract candidate name from resume.
        Uses simple heuristic: first line or filename as fallback.

        Args:
            text: Resume text
            filename: Name of the resume file

        Returns:
            Candidate name (best guess)
        """
        lines = text.strip().split('\n')

        # Try to find name in first few lines
        for line in lines[:5]:
            line = line.strip()
            # Simple heuristic: name is usually 2-4 words, not too long
            words = line.split()
            if 2 <= len(words) <= 4 and len(line) < 50:
                # Check if it doesn't look like a title/header
                if not any(keyword in line.lower() for keyword in
                          ['resume', 'cv', 'curriculum', 'vitae', 'contact', 'email']):
                    return line

        # Fallback: use filename (remove extension)
        name_from_file = os.path.splitext(os.path.basename(filename))[0]
        # Clean up filename (replace underscores/hyphens with spaces)
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        return name_from_file.title()

    def extract_location(self, text: str) -> Optional[str]:
        """
        Extract location from resume text.
        Uses keyword matching (best effort).

        Args:
            text: Resume text

        Returns:
            Location if found, None otherwise
        """
        # Convert to lines for better matching
        lines = text.split('\n')

        # Check each line for location keywords
        for line in lines[:20]:  # Focus on top of resume
            for location in self.location_keywords:
                if location.lower() in line.lower():
                    # Return the line or just the location keyword
                    return location

        return None

    def parse_resume(self, file_path: str) -> Dict:
        """
        Main method to parse a resume file and extract all information.

        Args:
            file_path: Path to the resume file (PDF or DOCX)

        Returns:
            Dictionary with extracted candidate information
        """
        # Determine file type and extract text
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(file_path)
        else:
            print(f"[ERROR] Unsupported file format: {file_extension}")
            return None

        if not text or len(text.strip()) < 50:
            print(f"[ERROR] Could not extract sufficient text from {file_path}")
            return None

        # Extract all information
        candidate_info = {
            'candidate_name': self.extract_name(text, file_path),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'location': self.extract_location(text),
            'resume_text': text  # Store full text for JD matching
        }

        return candidate_info

    def parse_multiple_resumes(self, folder_path: str) -> list:
        """
        Parse all resume files in a folder.

        Args:
            folder_path: Path to folder containing resume files

        Returns:
            List of candidate information dictionaries
        """
        candidates = []
        supported_extensions = ['.pdf', '.docx']

        # Get all files in the folder
        try:
            files = os.listdir(folder_path)
        except Exception as e:
            print(f"[ERROR] Error reading folder {folder_path}: {str(e)}")
            return candidates

        # Process each file
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            file_extension = os.path.splitext(filename)[1].lower()

            # Check if it's a supported file
            if file_extension in supported_extensions:
                print(f"Processing: {filename}")
                candidate_info = self.parse_resume(file_path)

                if candidate_info:
                    candidates.append(candidate_info)
                    print(f"[OK] Extracted: {candidate_info['candidate_name']}")
                else:
                    print(f"[ERROR] Failed to parse: {filename}")

        print(f"\n[OK] Total resumes processed: {len(candidates)}")
        return candidates


# Example usage (for testing)
if __name__ == "__main__":
    parser = ResumeParser()

    # Test with a single resume
    # candidate = parser.parse_resume("../resumes/john_doe_resume.pdf")
    # print(candidate)

    # Test with multiple resumes
    candidates = parser.parse_multiple_resumes("../resumes")
    for candidate in candidates:
        print(f"\nName: {candidate['candidate_name']}")
        print(f"Email: {candidate['email']}")
        print(f"Phone: {candidate['phone']}")
        print(f"Location: {candidate['location']}")
