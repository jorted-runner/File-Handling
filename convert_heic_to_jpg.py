
import os

from utils import Utils

util = Utils()

directory = r"C:\Users\dee.HFMLEGAL\hfmlegal.com\Rice, Kristi - School Bullying - 27127 - Documents"

for file in util.fetch_all_files(directory):
    root_directory = os.path.dirname(file)
    file_w_ext = os.path.basename(file).split('/')[-1]
    split_tup = os.path.splitext(file_w_ext)
    file_name = split_tup[0]
    file_extension = str(split_tup[1]).lower()
    if file_extension == '.heic':
        heic_file = file
        jpg_file = os.path.join(root_directory, f"{file_name}.jpeg")
        util.convert_heic_to_jpg(heic_file, jpg_file)

