import os
from utils import Utils

util = Utils()

root_folder = r"C:\Users\dee.HFMLEGAL\hfmlegal.com\Singer, Nikita - Personal Injury - 26720 - screenshots"

all_files = util.fetch_all_files(root_folder)

for file in all_files:
    total_file_name = os.path.basename(file)
    split_tup = os.path.splitext(total_file_name)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    if file_extension.lower() in [".jpg", ".jpeg", ".png"]:
        print(file)
        util.image_to_pdf(root_folder, file_name, file_extension)
    elif file_extension.lower() == ".mov":
        print(file)
        util.mov_to_mp4(root_folder, file_name, file_extension)
    elif file_extension.lower() == ".m3u8":
        print(file)
        util.download_video_from_m3u8(file, output_file=os.path.join(root_folder, file_name + ".mp4"))
    elif file_extension.lower() == ".aac":
        input_path = os.path.join(root_folder, file_name + file_extension)
        util.convert_audio(input_path, os.path.join(root_folder, file_name + ".mp4"), 'mp4')
    elif file_extension.lower() == ".m4a":
        print(file)
        util.m4a_to_mp4(root_folder, file_name, file_extension)

# This was to combine the image files that were converted to PDF
all_pdfs = util.fetch_all_pdf_files(root_folder)
all_fran = []
for file in all_pdfs:
    total_file_name = os.path.basename(file)
    split_tup = os.path.splitext(total_file_name)
    file_name = split_tup[0]
    if 'Fran' in file_name:
        all_fran.append(file)

util.merge_pdf(all_fran, 'FRAN_MSGS_2', root_folder)
