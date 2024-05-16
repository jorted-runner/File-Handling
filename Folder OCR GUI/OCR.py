import os
import shutil
import cv2
import subprocess
import pytesseract

from PyPDF2 import PdfReader, PdfMerger

class ocr:
    def check_OCR(self, file_path):
        try:
            with open(file_path, "rb") as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    if page.extract_text().strip():
                        return False
            return True
        except PermissionError:
            print("Permission Error, unable to open the file")


    def OCR(self, pages, pic, ocr_data_folder):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        input_dir = os.path.join(ocr_data_folder, pic)
        img = cv2.imread(input_dir, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_pdf_or_hocr(img_rgb, lang = "eng",
                                                config = "--dpi 300")
        input_dir = input_dir.replace('.jpg', '.pdf')
        f = open(input_dir, "w+b")
        f.write(bytearray(result))
        f.close()

    def compress_pdf(self, pdf_path):
        try:
            subprocess.run(['C:\pdfsizeopt\pdfsizeopt', '--use-pngout=no', pdf_path, pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during compression: {e}")

    def merge_pdf(self, extracted_files: list [str], file_name, base_directory):
        #Merge OCRed PDFs
        output_PDF = file_name + ".pdf"
        merger = PdfMerger()
        pdfs = 0
        for pdf in extracted_files:
            if pdf.endswith('.pdf'):
                merger.append(pdf)
                pdfs += 1
        merger.write(output_PDF)
        merger.close()
        self.compress_pdf(output_PDF)
        shutil.copy2(output_PDF, base_directory)
        os.remove(output_PDF)