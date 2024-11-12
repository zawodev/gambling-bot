import os

def load(file_name: str):
    data_file_name = os.path.join(os.path.dirname(__file__), f"{file_name}.txt")
    if not os.path.exists(data_file_name):
        return ""
    try:
        with open(data_file_name, 'r') as file:
            data = file.read()
        return data
    except Exception as e:
        raise e
