# File Handling
While working in the IT department at a law firm I would receive daily or weekly requests to convert different files to PDF and to OCR PDF files within a cases directory. As the requests came in I would write a python program to handle the files that needed to be converted to PDF. The firm had also recently stopped paying for the service that monitored their network for PDFs, and with that change I was receiving tons of requests to OCR PDF files. I decided to develop a program to monitor the network drive for new PDF files, check if the file is already OCRed, and then OCR the file if needed.
## Folder OCR GUI
As request came in a began working on a gui that members of the firm could download to handle the conversion and OCR themselves. The GUI combines the different programs I had developed. When the user has the program running they enter the path to the folder they want to use, and then they select from a drop down what they want the program to do. 
## Getting Started
1. Install Pytesseract - https://pypi.org/project/pytesseract/
   - Installation instructions (exert from pytesseract pypi page)

        Prerequisites:
        
        Python-tesseract requires Python 3.6+
        
        You will need the Python Imaging Library (PIL) (or the Pillow fork). Under Debian/Ubuntu, this is the package python-imaging or python3-imaging.
        
        Install Google Tesseract OCR (https://github.com/tesseract-ocr/tesseract) (additional info how to install the engine on Linux, Mac OSX and Windows). You must be able to invoke the tesseract command as tesseract. If this isn’t the case, for example because tesseract isn’t in your PATH, you will have to change the “tesseract_cmd” variable pytesseract.pytesseract.tesseract_cmd. Under Debian/Ubuntu you can use the package tesseract-ocr. For Mac OS users. install homebrew package tesseract.
        
        Note: In some rare cases, you might need to additionally install tessconfigs and configs from tesseract-ocr/tessconfigs (https://github.com/tesseract-ocr/tessconfigs) if the OS specific package doesn’t include them.
        
        Installing via pip:
        Check the pytesseract package page for more information.
        
        pip install pytesseract
        Or if you have git installed:
     ```
        pip install -U git+https://github.com/madmaze/pytesseract.git
     ```
        Installing from source:
     ```
        git clone https://github.com/madmaze/pytesseract.git
        cd pytesseract && pip install -U .
     ```
        Install with conda (via conda-forge):
     ```
        conda install -c conda-forge pytesseract
     ```
2. Follow instructions for pdfsizeopt:
    - Windows: https://github.com/pts/pdfsizeopt#installation-instructions-and-usage-on-windows
    - Linux: https://github.com/pts/pdfsizeopt#installation-instructions-and-usage-on-linux
    - With Docker on Linux and macOS: https://github.com/pts/pdfsizeopt?tab=readme-ov-file#installation-instructions-and-usage-with-docker-on-linux-and-macos
3. Install dependencies from Requirements.txt
4. Run main.py from Folder OCR GUI
