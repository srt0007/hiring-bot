# Installing Tesseract OCR for Image-Based PDF Support

## Current Status

Your system has the Python OCR packages installed (pytesseract, pdf2image, pillow), but the actual Tesseract OCR engine is not yet installed.

**What you have:**
- ✅ Python wrapper (pytesseract)
- ✅ PDF to image converter (pdf2image)
- ✅ Image processing (pillow)

**What you need:**
- ❌ Tesseract OCR engine (the actual OCR software)

---

## Quick Install Guide

### Step 1: Download Tesseract OCR

**Download the Windows installer:**
https://github.com/UB-Mannheim/tesseract/wiki

**Direct download link (64-bit):**
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe

**File size:** ~50 MB

---

### Step 2: Install Tesseract

1. Run the downloaded `.exe` file
2. **Important:** Install to the default location: `C:\Program Files\Tesseract-OCR`
3. During installation, make sure to check:
   - ☑ Install Tesseract OCR engine
   - ☑ Install English language data
4. Click "Install"
5. Wait for installation to complete (~1 minute)

---

### Step 3: Verify Installation

Open Command Prompt and run:

```bash
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

**Expected output:**
```
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.5.1) : libpng 1.6.40 : libtiff 4.6.0 : zlib 1.2.13 : libwebp 1.3.2 : libopenjp2 2.5.0
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP 201511
```

If you see this, Tesseract is installed correctly!

---

### Step 4: Restart Web UI

After installing Tesseract:

1. Close the current web UI (Ctrl+C in the console or close the window)
2. Double-click `RUN_WEB_UI.bat` again
3. The OCR functionality will now be available

---

## How OCR Works After Installation

Once Tesseract is installed, the resume parser will:

1. **First:** Try normal text extraction from PDF (fast, ~1 second)
2. **If no text found:** Automatically use OCR
   - Convert PDF pages to images
   - Run Tesseract OCR on each page
   - Extract text from images
   - Takes ~5-10 seconds per page

**You'll see messages like:**
```
[WARN] No text extracted from PDF. Attempting OCR...
[INFO] Starting OCR extraction for resumes/resume.pdf...
[INFO] Converted 2 pages to images
[INFO] OCR processing page 1/2...
[INFO] OCR processing page 2/2...
[OK] OCR extracted 1250 characters from resumes/resume.pdf
```

---

## Alternative: Use Online OCR (If You Don't Want to Install)

If you prefer not to install Tesseract, you can convert image-based PDFs to text-based PDFs using online tools:

### **Option 1: Adobe Acrobat Online**
https://www.adobe.com/acrobat/online/pdf-to-word.html
- Upload PDF → Download as Word → Re-export as PDF
- Free, no signup needed

### **Option 2: Smallpdf OCR**
https://smallpdf.com/ocr-pdf
- Upload scanned PDF → Get text PDF
- Free with limits

### **Option 3: PDF24 Tools**
https://tools.pdf24.org/en/ocr-pdf
- Completely free
- No file size limits

**Steps:**
1. Upload your scanned PDF
2. OCR will convert images to text
3. Download the new PDF
4. Upload to hiring automation tool

---

## Testing OCR (After Installation)

1. Install Tesseract using steps above
2. Restart web UI
3. Go to "Process Resumes" page
4. Upload "Nitin Professional Resume.pdf"
5. Click "Process Resumes"
6. Watch the console for OCR progress messages
7. Resume should be parsed successfully!

---

## Summary

**Current situation:**
- Python packages are installed ✅
- Tesseract OCR engine is NOT installed ❌
- Image-based PDFs won't work yet

**To enable OCR:**
1. Download installer from link above (5 minutes)
2. Run installer, use default location (2 minutes)
3. Restart web UI (30 seconds)
4. OCR will work automatically!

**Total time:** ~10 minutes

**Alternative:**
Use online OCR tools to convert PDFs before uploading (no installation needed)

---

## Need Help?

If installation fails or you have questions, check:
- Official Tesseract documentation: https://github.com/tesseract-ocr/tesseract
- Windows installer wiki: https://github.com/UB-Mannheim/tesseract/wiki

---

**Once Tesseract is installed, your hiring automation tool will be able to parse ANY type of PDF - text-based or image-based!**
