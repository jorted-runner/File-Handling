## Danny Ellis 2023 ##

import os
import time
import shutil
import cv2
import subprocess
import datetime

import pytesseract
import pdf2image
import watchdog.events
import watchdog.observers
from PyPDF2 import PdfReader, PdfMerger

not_OCRed_directory = r"I:\Original Not OCRed"

def main():
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, r"I:\\", recursive = True)
    observer.start()
    observer.join()

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.pdf'],
                                                           ignore_patterns = None,
                                                           ignore_directories = False,
                                                           case_sensitive = False)
    
    def on_created(self, event):
        file_path = event.src_path
        root_directory = os.path.dirname(file_path)
        file_w_ext = os.path.basename(file_path).split('/')[-1]
        split_tup = os.path.splitext(file_w_ext)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        proccess_PDFs(file_path, root_directory, file_w_ext, file_name)

def fetch_all_files(folder_save_point):
    target_files = []
    for file_name in os.listdir(folder_save_point):
        if os.path.isfile(os.path.join(folder_save_point, file_name)):
            target_files.append(os.path.join(folder_save_point, file_name))
    return target_files

def proccess_PDFs(file_path, directory, file_name_ext, file_name):
    if "Original Not OCRed" not in directory and \
    not os.path.isfile(os.path.join(not_OCRed_directory, file_name_ext)):
        time.sleep(5)
        print(f"New File Detected: {file_path}")
        try:
            shutil.copy2(file_path, not_OCRed_directory)
            copied_file = os.path.join(not_OCRed_directory, file_name_ext)
            needs_OCRed = check_OCR(copied_file)
            if needs_OCRed:
                print(f"Needs OCRed: {file_path}")
                OCR_proccess(file_path, directory, file_name_ext, file_name)
            else:
                print("No OCR needed\n")
        except Exception as e:
            logError(e, file_name_ext, file_path)

def logError(error_type, actual_file, file_path):
    f = open(r"C:\Users\dee.HFMLEGAL\Desktop\Error_log.txt", "a")
    f.write("{0} -- {1}: {2} -- {3}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), actual_file, error_type, file_path))
    f.close()

def check_OCR(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                if page.extract_text().strip():
                    return False
        return True
    except PermissionError:
        print("Permission Error, unable to open the file")

def OCR_proccess(file_path, directory, file_name_ext, file_name):
    ocr_data_folder = os.path.join(r"C:\OCRdata", file_name)
    create_folder(ocr_data_folder)
    image_conversion(file_path, ocr_data_folder, file_name)
    jpgs = [f for f in os.listdir(ocr_data_folder) if os.path.isfile(os.path.join(ocr_data_folder, f))]
    for page, pic in enumerate(jpgs):
        page += 1
        OCR(page, pic, ocr_data_folder)
    extracted_files = fetch_all_files(ocr_data_folder)
    merge_pdf(extracted_files, file_name, directory)

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def image_conversion(inpath, folder_save_point, file_name):
        print("Converting to JPG")
        OUTPUT_FOLDER = folder_save_point
        FIRST_PAGE = None
        LAST_PAGE = None
        FORMAT = 'jpg'
        USERPWD = None
        USE_CROPBOX = False
        STRICT = False
        page = 0

        pdf2image.convert_from_path(inpath,
                                    output_folder = OUTPUT_FOLDER,
                                    first_page = FIRST_PAGE,
                                    last_page = LAST_PAGE,
                                    fmt = FORMAT,
                                    userpw = USERPWD,
                                    use_cropbox = USE_CROPBOX,
                                    strict = STRICT,
                                    dpi=300, output_file = f"{file_name}"
                                    )
        print("All pages converted to JPG.")

def OCR(pages, pic, ocr_data_folder):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        #OCR each JPG file and convert to OCRed PDF
        input_dir = os.path.join(ocr_data_folder, pic)
        img = cv2.imread(input_dir, 1)
        #img = cv2.bilateralFilter(img,9,75,75)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_pdf_or_hocr(img_rgb, lang = "eng",
                                                  config = "--dpi 300")
        input_dir = input_dir.replace('.jpg', '.pdf')
        f = open(input_dir, "w+b")
        f.write(bytearray(result))
        f.close()
        print("Page " , pages, " OCRed.") 

def merge_pdf(extracted_files: list [str], file_name, base_directory):
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
        print("Merge Complete.\nBeginning Compression.")
        compress_pdf(output_PDF)
        print(f"{file_name} compressed successfully")
        shutil.copy2(output_PDF, base_directory)
        print("OCRed moved to correct location\n")
        os.remove(output_PDF)

def compress_pdf(pdf_path):
    try:
        subprocess.run(['C:\pdfsizeopt\pdfsizeopt', '--use-pngout=no', pdf_path, pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during compression: {e}")

if __name__ == "__main__":
    main()