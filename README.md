# File Handling
While working in the IT department at a law firm I would receive daily or weekly requests to convert different files to PDF and to OCR PDF files within a cases directory. As the requests came in I would write a python program to handle the files that needed to be converted to PDF. The firm had also recently stopped paying for the service that monitored their network for PDFs, and with that change I was receiving tons of requests to OCR PDF files. I decided to develop a program to monitor the network drive for new PDF files, check if the file is already OCRed, and then OCR the file if needed.
## Folder OCR GUI
As request came in a began working on a gui that members of the firm could download to handle the conversion and OCR themselves. The GUI combines the different programs I had developed. When the user has the program running they enter the path to the folder they want to use, and then they select from a drop down what they want the program to do. 
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
5. Install dependencies from Requirements.txt
6. Run main.py from Folder OCR GUI
