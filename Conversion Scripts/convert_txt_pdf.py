## DANNY ELLIS 2023 ##

# This script will convert all the txt files in a folder to pdf.
# Its add a bates number in the bottom right corner.
# EX: filename2344523.001
# The .000 will increment by pagenumber.

import os

from utils import Utils

util = Utils()

# Should be the only thing that needs to change. Change to directory with the txt files.
root_folder = r"C:\Users\dee.HFMLEGAL\OneDrive - hfmlegal.com\Desktop\Amber"

all_files = util.fetch_all_files(root_folder)

for file in all_files:
    path = file
    total_file_name = os.path.basename(path).split('/')[-1]
    split_tup = os.path.splitext(total_file_name)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    if file_extension == ".txt":
        util.txt_to_pdf(root_folder, file_name, file_extension)
    else:
        pass