import os
from PIL import Image

class Utils:
    def create_folders(self, folders):
        for folder in folders:
            if not self.check_folder(folder):
                os.makedirs(folder)

    def check_folder(self, folder):
        if os.path.exists(folder):
            return True
        return False
    
    def file_data(self, file):
        root_directory = os.path.dirname(file)
        file_w_ext = os.path.basename(file).split('/')[-1]
        split_tup = os.path.splitext(file_w_ext)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        return root_directory, file_w_ext, file_name, file_extension
    
    def invert_colors(self, image_path, path):
        img = Image.open(image_path)
        root_directory, file_w_ext, file_name, file_extension = self.file_data(image_path)
        new_file_name = f"{file_name}-inverted.jpg"
        outpath = os.path.join(path, new_file_name)
        inverted_img = Image.eval(img, lambda x: 255 - x)
        inverted_img.save(outpath)
        os.remove(image_path)