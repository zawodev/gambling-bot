from gambling_bot.data.json_manager import save_data, load_data

class DictData:
    def __init__(self, default_data, data, path):
        self.path = path
        if not isinstance(data, dict):
            print("Warning: data provided is not a dictionary. Using default values instead.")
            data = {}
        default_data.update(data)
        save_data(self.path, default_data)

    def __getitem__(self, key):
        data = load_data(self.path)
        return data.get(key, {})

    def __setitem__(self, key, value):
        data = load_data(self.path)
        data[key] = value
        save_data(self.path, data)
