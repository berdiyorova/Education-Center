import os
import json
from contextlib import contextmanager


@contextmanager
def custom_open(file_name, mode):
    file = open(file_name, mode)
    yield file
    file.close()


class JsonManager:
    def __init__(self, file_name):
        self.file_name = file_name


    def _file_exists_and_not_empty(self):
        return os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0


    def read_data(self):
        if self._file_exists_and_not_empty():
            with custom_open(self.file_name, 'r') as file:
                return json.load(file)
        return []


    def write_data(self, data):
        with custom_open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)


    def add_data(self, data: dict):
        all_data = self.read_data()
        all_data.append(data)
        self.write_data(all_data)
        return "Data added successfully"


    def update_data(self, user, new_data):
        all_data = self.read_data()

        for item in all_data:
            if item == user:
                item.update(new_data)
                self.write_data(all_data)
                return True
        return False

    def delete_data(self, obj):
        all_data = self.read_data()
        length = len(all_data)

        for item in all_data:
            if item == obj:
                all_data.remove(item)
                break

        self.write_data(all_data)
        return len(all_data) < length


user_manager = JsonManager("../data/users.json")
group_manager = JsonManager("../data/groups.json")
