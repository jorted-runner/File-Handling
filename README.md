# File Handling
While working in the IT department at a law firm, I frequently received daily or weekly requests to convert various files to PDF and to OCR PDF files within a case directory. As the requests came in, I wrote Python programs to handle the file conversions to PDF. Additionally, the firm had recently stopped paying for a service that monitored their network for PDFs, resulting in a significant increase in requests to OCR PDF files. To address this, I developed a program to monitor the network drive for new PDF files, check if the files were already OCRed, and OCR them if needed.
## Folder OCR GUI
As requests increased, I began working on a GUI that members of the firm could download to handle file conversions and OCR themselves. The GUI integrates the different programs I had developed. When users run the program, they enter the path to the folder they want to use and select the desired action from a dropdown menu.
## Getting Started
1. Install Pytesseract
   - Get latest release: https://github.com/UB-Mannheim/tesseract/wiki
      - Download and run https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe (Found using link above)
   - More info: https://pypi.org/project/pytesseract/
3. Follow instructions for pdfsizeopt:
    - Windows: https://github.com/pts/pdfsizeopt#installation-instructions-and-usage-on-windows
    - Linux: https://github.com/pts/pdfsizeopt#installation-instructions-and-usage-on-linux
    - With Docker on Linux and macOS: https://github.com/pts/pdfsizeopt?tab=readme-ov-file#installation-instructions-and-usage-with-docker-on-linux-and-macos
4. Install Poppler 23.01.0 (version I used, newer may work as well) and add path to bin to System Path variable (C:\poppler-23.01.0\Library\bin\)
   - https://github.com/oschwartz10612/poppler-windows/releases
5. Install latest version of wkhtmltopdf and add to PATH:
   - https://wkhtmltopdf.org/downloads.html
5. Install dependencies from Requirements.txt
6. Run main.py from Folder OCR GUI
