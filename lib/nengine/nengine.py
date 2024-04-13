import random
import os
import datetime


class NotesEngine:

    def __init__(self, path):
        self.path = path

    def get_files(self, target_date=None):
        files_created_on_date = []
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            stat = os.stat(file_path)
            if os.path.isfile(file_path):
                created_at = datetime.date.fromtimestamp(stat.st_ctime)
                if target_date is None or created_at == target_date:
                    files_created_on_date.append(filename)
        return files_created_on_date

    def pick_random_file(self, files_list):
        if not files_list:
            return None
        return random.choice(files_list)

    def read_file_content(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print("File not found")
            return None
