from gambling_bot.data.json_manager import save_data

class DictData:
    def __init__(self, default_data, data, path):
        if not isinstance(data, dict):
            print("Warning: data provided is not a dictionary. Using default values instead.")
            data = {}
        default_data.update(data)

        self._data = default_data
        self._path = path

        self.save()

    def save(self):
        save_data(self._path, self._data)

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            print(f"Error: key '{key}' does not exist.")
            return None

    def __setitem__(self, key, value):
        self._data[key] = value
        self.save()
