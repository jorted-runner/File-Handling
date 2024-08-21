import os
from fpdf import FPDF
from docx2pdf import convert
from PIL import Image
import comtypes.client
import pillow_heif
import subprocess
import ffmpeg
import pydicom
import pdf2image
from moviepy.editor import VideoFileClip

class converter:
    def txt_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, f"{file_name}{file_extension}")
        converted = os.path.join(path, f"{file_name}.pdf")
        pdf = FPDF()  
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        f = open(og_path, "r")
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        pdf.output(converted)

    def docx_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, f"{file_name}{file_extension}")
        converted = os.path.join(path, f"{file_name}.pdf")
        convert(og_path, converted)

    def image_to_pdf(self, folder, file_name, file_extension):
        og_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".pdf")
        image = Image.open(og_path)
        image.save(converted, "PDF", resolution=100.0)
        image.close()

    def doc_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, file_name + file_extension)
        converted = os.path.join(path, file_name + ".pdf")
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(og_path)
        doc.SaveAs(converted, FileFormat=17)
        doc.Close()
        word.Quit()

    def convert_heic_to_jpg(self, heic_file, jpg_file):
        heif_file = pillow_heif.read_heif(heic_file)
        image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        )
        image.save(jpg_file, format("jpeg"))

    def download_video_from_m3u8(self, m3u8_file, output_file):
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
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while downloading the video: {e}")
        finally:
            if os.path.exists(temp_directory):
                for file_name in os.listdir(temp_directory):
                    file_path = os.path.join(temp_directory, file_name)
                    os.remove(file_path)
                os.rmdir(temp_directory)

    def convert_audio(self, input_file, output_file, output_format):
        try:
            ffmpeg.input(input_file).output(output_file, format=output_format).run()
        except ffmpeg.Error as e:
            print(f"Error occurred while converting audio: {e}")

    def m4a_to_mp4(self, folder, file_name, file_extension):
        input_path = os.path.join(folder, file_name + file_extension)
        output_path = os.path.join(folder, file_name + ".mp4")
        
        try:
            ffmpeg.input(input_path).output(output_path, codec='copy').run()
        except ffmpeg.Error as e:
            print(f"Error occurred while converting .m4a to .mp4: {e}")

    def mov_to_mp4(self, folder, file_name, file_extension):
        input_path = os.path.join(folder, file_name + file_extension)
        output_path = os.path.join(folder, file_name + ".mp4")

        video_clip = VideoFileClip(input_path)
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        video_clip.close()

    def dcm_to_jpeg(self, folder, file_name, file_extension):
        dcm_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".jpeg")

        dicom_data = pydicom.dcmread(dcm_path)

        pixel_data = dicom_data.pixel_array
        image = Image.fromarray(pixel_data)

        image.save(converted, "JPEG", quality=95)
        image.close()

    def dcm_to_pdf(self, folder, file_name, file_extension):
        dcm_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".pdf")

        dicom_data = pydicom.dcmread(dcm_path)

        pixel_data = dicom_data.pixel_array
        image = Image.fromarray(pixel_data)

        image.save(converted, "PDF", resolution=100.0)
        image.close()
    
    def image_conversion(self, inpath, folder_save_point, file_name):
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
                                    dpi=300, output_file = f"{file_name}",
                                    )
        
    def gif_to_mp4(self, folder, file_name, file_extension):
        input_path = os.path.join(folder, file_name + file_extension)
        output_path = os.path.join(folder, file_name + ".mp4")
        
        try:
            ffmpeg.input(input_path).output(output_path, vcodec='libx264', pix_fmt='yuv420p', acodec='aac').run()
        except ffmpeg.Error as e:
            print(f"Error occurred while converting .gif to .mp4: {e}")

    def mpg_to_mp4(self, path, file_name, file_extension):
            og_path = os.path.join(path, f"{file_name}{file_extension}")
            converted = os.path.join(path, f"{file_name}.mp4")
            
            clip = VideoFileClip(og_path)
            clip.write_videofile(converted, codec="libx264")
            clip.close()
