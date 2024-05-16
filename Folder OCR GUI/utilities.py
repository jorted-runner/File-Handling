import os

class Utils:
    def create_folders(self, folders):
        for folder in folders:
            if not self.check_folder(folder):
                os.makedirs(folder)

    def check_folder(folder):
        if os.path.exists(folder):
            return True
        return False
    
    def file_data(file):
        root_directory = os.path.dirname(file)
        file_w_ext = os.path.basename(file).split('/')[-1]
        split_tup = os.path.splitext(file_w_ext)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        return root_directory, file_w_ext, file_name, file_extension