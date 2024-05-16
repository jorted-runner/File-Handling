import os
from PIL import Image
import pillow_heif
from PyPDF2 import PdfReader, PdfMerger
import shutil
import subprocess
import ffmpeg
import os
import re
from fpdf import FPDF
from PIL import Image
from moviepy.editor import VideoFileClip
import pydicom
from PIL import Image

class Utils:
    def __init__(self) -> None:
        self.PDF = PDF()

    def fetch_all_files(folder_save_point):
        target_files = []
        for path, subdirs, files in os.walk(folder_save_point):
            for name in files:
                target_files.append(os.path.join(path, name))
        return target_files
    
    def fetch_all_pdf_files(folder_save_point):
        target_files = []
        for file_name in os.listdir(folder_save_point):
            if file_name.lower().endswith('.pdf') and os.path.isfile(os.path.join(folder_save_point, file_name)):
                target_files.append(os.path.join(folder_save_point, file_name))
        return target_files

    def compress_pdf(pdf_path):
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
        print("Merge Complete.\nBeginning Compression.")
        self.compress_pdf(output_PDF)
        print(f"{file_name} compressed successfully")
        shutil.copy2(output_PDF, base_directory)
        print("OCRed moved to correct location\n")
        os.remove(output_PDF)

    def convert_heic_to_jpg(heic_file, jpg_file):
        heif_file = pillow_heif.read_heif(heic_file)
        image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        )
        image.save(jpg_file, format("jpeg"))
        print("Conversion complete!")

    def download_video_from_m3u8(m3u8_file, output_file):
        temp_directory = "temp_segments"
        os.makedirs(temp_directory, exist_ok=True)

        try:
            ffmpeg_command = [
                "ffmpeg",
                "-protocol_whitelist", "file,http,https,tcp,tls",
                "-i", m3u8_file,
                "-c", "copy",
                output_file
            ]
            subprocess.run(ffmpeg_command, check=True)
            print(f"Video downloaded and saved to: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while downloading the video: {e}")
        finally:
            if os.path.exists(temp_directory):
                for file_name in os.listdir(temp_directory):
                    file_path = os.path.join(temp_directory, file_name)
                    os.remove(file_path)
                os.rmdir(temp_directory)

    def convert_audio(input_file, output_file, output_format):
        try:
            ffmpeg.input(input_file).output(output_file, format=output_format).run()
            print(f"Audio file converted to {output_format}: {output_file}")
        except ffmpeg.Error as e:
            print(f"Error occurred while converting audio: {e}")

    def m4a_to_mp4(folder, file_name, file_extension):
        input_path = os.path.join(folder, file_name + file_extension)
        output_path = os.path.join(folder, file_name + ".mp4")
        
        try:
            ffmpeg.input(input_path).output(output_path, codec='copy').run()
            print(f"Audio file converted to mp4: {output_path}")
        except ffmpeg.Error as e:
            print(f"Error occurred while converting .m4a to .mp4: {e}")

    def extract_number(file_name):
        """Extract numbers from the file name for sorting."""
        match = re.search(r'(\d+)', file_name)
        return int(match.group(1)) if match else float('inf')

    def image_to_pdf(folder, file_name, file_extension):
        og_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".pdf")
        
        image = Image.open(og_path)
        image.save(converted, "PDF", resolution=100.0)
        image.close()

    def mov_to_mp4(folder, file_name, file_extension):
        input_path = os.path.join(folder, file_name + file_extension)
        output_path = os.path.join(folder, file_name + ".mp4")

        video_clip = VideoFileClip(input_path)
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        video_clip.close()

    def txt_to_pdf(self, path, file_name, file_extension):
        og_path = path + "\\" + file_name + file_extension
        converted = path + "\\" + file_name + ".pdf"
        pdf = self.PDF(file_name)  
        pdf.add_page()
        pdf.set_font("Arial", size = 10)
        f = open(og_path, "r", encoding='latin-1')
        for x in f:
            pdf.multi_cell(w=0, h=5, txt = x, align = 'L')
        pdf.output(converted)

    def dcm_to_jpeg(folder, file_name, file_extension):
        dcm_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".jpeg")

        dicom_data = pydicom.dcmread(dcm_path)

        pixel_data = dicom_data.pixel_array
        image = Image.fromarray(pixel_data)

        image.save(converted, "JPEG", quality=95)
        image.close()

    def dcm_to_pdf(folder, file_name, file_extension):
        dcm_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".pdf")

        dicom_data = pydicom.dcmread(dcm_path)

        pixel_data = dicom_data.pixel_array
        image = Image.fromarray(pixel_data)

        image.save(converted, "PDF", resolution=100.0)
        image.close()

class PDF(FPDF):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", style='', size=8)
        # .zfill changes the number of extra digits that get places. .zfill(3) formats its .000
        bates_range = f"{self.file_name}.{str(self.page_no()).zfill(3)}"
        self.cell(0, 10, bates_range, 0, 0, "R")