import os

from utils import Utils

util = Utils()

root_folder = r"D:\DAVEY,SHARON\DAVEY,SHARON\Davey Images"

all_files = util.fetch_all_files(root_folder)

for file in all_files:
    total_file_name = os.path.basename(file).split('/')[-1]
    split_tup = os.path.splitext(total_file_name)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    util.dcm_to_jpeg(root_folder, file_name, file_extension)
    util.dcm_to_pdf(root_folder, file_name, file_extension)