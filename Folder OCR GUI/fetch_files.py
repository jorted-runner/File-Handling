import os

class FetchFiles():
    def fetch_all_files_recursive(self, folder_save_point):
        target_files = []
        for entry_name in os.listdir(folder_save_point):
            full_path = os.path.join(folder_save_point, entry_name)
            if os.path.isfile(full_path):
                target_files.append(full_path)
            elif os.path.isdir(full_path):
                target_files.extend(self.fetch_all_files_recursive(full_path))
        return target_files

    def fetch_all_files(self, folder_save_point):
        target_files = []
        for file_name in os.listdir(folder_save_point):
            if os.path.isfile(os.path.join(folder_save_point, file_name)):
                target_files.append(os.path.join(folder_save_point, file_name))
        return target_files