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