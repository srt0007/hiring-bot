# PDF Parsing Issues - Solutions Guide

## ⚠️ Common Issue: "Could not parse PDF"

### Why This Happens

When you see "⚠️ Could not parse [filename].pdf", it usually means:

1. **Image-based PDF (Most Common)**
   - The PDF is a scanned document
   - It contains images of text, not actual text
   - PyPDF2 cannot read images

2. **Encrypted/Protected PDF**
   - PDF has password protection
   - Cannot be opened by the parser

3. **Corrupted PDF**
   - File is damaged or incomplete
   - Cannot be read properly

---

## ✅ Solutions

### **Solution 1: Use Text-Based PDFs (Recommended)**

**Check if PDF has text:**
1. Open the PDF in Adobe Reader or browser
2. Try to select and copy text
3. If you CAN copy text → It's text-based (should work)
4. If you CANNOT copy text → It's image-based (won't work)

**How to get text-based PDFs:**
- Ask candidates to export from Word/Google Docs as PDF
- Use "Print to PDF" instead of scanning
- Save documents as PDF (not scan them)

---

### **Solution 2: Convert Image PDFs to Text PDFs (OCR)**

If you have scanned/image-based PDFs, you need OCR (Optical Character Recognition):

#### **Option A: Use Online OCR Tools**

**Free Online Tools:**
1. **Adobe Acrobat Online** - https://www.adobe.com/acrobat/online/pdf-to-word.html
   - Upload PDF → Download as Word → Re-export as PDF
   - Free, no signup needed

2. **Smallpdf** - https://smallpdf.com/ocr-pdf
   - Upload scanned PDF → Get text PDF
   - Free with limits

3. **PDF24 Tools** - https://tools.pdf24.org/en/ocr-pdf
   - Completely free
   - No file size limits

**Steps:**
1. Upload your scanned PDF
2. OCR will convert images to text
3. Download the new PDF
4. Upload to hiring automation tool

---

#### **Option B: Use Desktop Software**

**Adobe Acrobat Pro:**
- Open scanned PDF
- Tools → Recognize Text → In This File
- Save
- Now it's text-based!

**Free Alternative - Tesseract OCR:**
- Open source OCR engine
- Requires technical setup
- Very accurate

---

### **Solution 3: Use DOCX Format Instead**

**Easiest solution:**
1. Ask candidates to submit resumes as **.docx** files
2. DOCX files are easier to parse
3. No scanning issues

**Benefits:**
- 100% text-based
- No image issues
- Better compatibility

---

## 🔍 How to Test Your PDFs

### **Quick Test Script**

Create a file `test_pdf.py`:

```python
from src.resume_parser import ResumeParser

parser = ResumeParser()

# Test your PDF
pdf_file = "resumes/your_resume.pdf"
result = parser.parse_resume(pdf_file)

if result and 'text' in result:
    print("✅ PDF can be parsed!")
    print(f"Extracted {len(result['text'])} characters")
    print(f"Name: {result.get('name', 'Not found')}")
    print(f"Email: {result.get('email', 'Not found')}")
else:
    print("❌ PDF cannot be parsed")
    print("This is likely an image-based (scanned) PDF")
```

Run:
```bash
python test_pdf.py
```

---

## 📋 Best Practices for Resumes

### **For Your Team:**

**Instruct candidates to submit:**
1. ✅ **Format:** DOCX or text-based PDF
2. ✅ **Source:** Created in Word/Google Docs, not scanned
3. ✅ **Size:** Under 5MB
4. ✅ **Content:** Actual text, not images of text

**Avoid:**
- ❌ Scanned documents
- ❌ Photos of resumes
- ❌ Image files (JPG, PNG) converted to PDF
- ❌ Password-protected PDFs
- ❌ Corrupted files

---

## 🛠️ Advanced: Add OCR to Your Tool (Future)

If you frequently receive scanned PDFs, you can add OCR capability:

### **Option: Add pytesseract (Python OCR)**

**Install:**
```bash
pip install pytesseract pdf2image
# Also install Tesseract OCR software from: https://github.com/tesseract-ocr/tesseract
```

**Modify resume_parser.py:**
```python
import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(self, file_path: str) -> str:
    """
    Extract text from image-based PDF using OCR
    """
    try:
        # Convert PDF to images
        images = convert_from_path(file_path)

        text = ""
        for img in images:
            # OCR each page
            text += pytesseract.image_to_string(img) + "\n"

        return text
    except Exception as e:
        print(f"OCR failed: {str(e)}")
        return ""
```

**Note:** This requires:
- Tesseract OCR installation
- More processing time
- More dependencies
- Could be Phase 2 feature

---

## 📊 Current Capabilities

### ✅ What Works:
- Text-based PDFs (from Word, Google Docs)
- DOCX files
- PDFs with actual text layers
- Multi-page documents
- Most modern PDFs

### ❌ What Doesn't Work:
- Scanned PDFs (images)
- Photo-based PDFs
- Handwritten documents
- Password-protected PDFs
- Severely corrupted files

---

## 🎯 Recommended Workflow

### **For Testing:**
1. Use sample text-based resumes
2. Test with DOCX files first
3. Verify system works

### **For Production:**
1. **Update job posting:**
   - "Submit resume as DOCX or PDF (text-based, not scanned)"

2. **Email candidates:**
   - "Please ensure your resume is a Word document or PDF created from Word/Google Docs, not a scanned image"

3. **Pre-screening:**
   - Quickly check resumes before uploading
   - Try to copy text from PDF → If it works, it will parse

### **For Problem PDFs:**
1. Use online OCR tool (2 minutes)
2. Convert to DOCX and re-submit
3. Or ask candidate to re-send as DOCX

---

## 💡 Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Scanned PDF | Use https://smallpdf.com/ocr-pdf |
| Password PDF | Ask candidate for unprotected version |
| Corrupted PDF | Ask candidate to re-send |
| Image PDF | Convert with Adobe Acrobat online |
| Large file | Compress at https://smallpdf.com/compress-pdf |

---

## 📞 Support

If a resume consistently fails:

1. **Check the PDF:**
   - Open it
   - Try to copy text
   - If you can't copy → it's image-based

2. **Ask candidate:**
   - "Could you please send your resume as a Word document (.docx)?"
   - Or: "Could you re-export your resume as a PDF from Word?"

3. **Use online tools:**
   - OCR converters (listed above)
   - 2-minute solution
   - Works for most cases

---

## ✅ Summary

**The Issue:** PyPDF2 cannot read image-based (scanned) PDFs

**The Solutions:**
1. Use text-based PDFs or DOCX files ✅ (Easiest)
2. Convert scanned PDFs using OCR ✅ (Fast)
3. Ask candidates to resubmit ✅ (Best quality)
4. Add OCR to the tool ⏳ (Future)

**Best Practice:**
Update your job posting to request "DOCX or text-based PDF" resumes.

---

**Most candidates submit text-based PDFs, so this is rarely an issue in practice!**
