import json
import os

DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')
# categories: players, dealers, tables

def load_data(path=None):
    """Wczytuje fragment z pliku JSON z podanej ścieżki. Jeśli plik lub ścieżka nie istnieje, zwraca pusty słownik."""
    if not os.path.exists(DATA_FILE_NAME):
        return {}
    try:
        with open(DATA_FILE_NAME, 'r') as file:
            data = json.load(file)
        if path is None:
            return data
        keys = path.split('/')
        for key in keys:
            data = data.get(key, {})
        return data
    except json.JSONDecodeError:
        return {}

def save_data(path=None, data=None):
    """Zapisuje dane do pliku JSON w danej ścieżce, tworząc brakujące ścieżki."""
    existing_data = load_data() if os.path.exists(DATA_FILE_NAME) else {}

    if data is None:
        data = {}

    if path is None:
        existing_data = data
    else:
        keys = path.split('/')
        sub_data = existing_data
        for key in keys[:-1]:
            sub_data = sub_data.setdefault(key, {})
        sub_data[keys[-1]] = data

    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(existing_data, file, indent=4) # noqa

def remove_data(path=None):
    """Usuwa cały rekord lub całą bazę danych pod daną ścieżką."""
    data = load_data()

    if path is None:
        save_data(None, None)
    else:
        keys = path.split('/')
        sub_data = data
        for key in keys[:-1]:
            sub_data = sub_data.get(key, {})
        if keys[-1] in sub_data:
            del sub_data[keys[-1]]
        save_data(None, data)

def move_data(src_path, dest_path):
    """Przenosi dane z jednej ścieżki do innej, zmieniając ewentualnie nazwę."""
    data = load_data()
    src_keys = src_path.split('/')
    dest_keys = dest_path.split('/')

    src_data = data
    for key in src_keys[:-1]:
        src_data = src_data.get(key, {})

    src_value = src_data.pop(src_keys[-1], None)

    dest_data = data
    for key in dest_keys[:-1]:
        dest_data = dest_data.setdefault(key, {})
    dest_data[dest_keys[-1]] = src_value

    save_data(None, data)


def save_data_raw(path: str, data: str):
    # sprawdź, czy plik istnieje; jeśli nie, ustaw json_data jako pusty słownik
    if os.path.exists(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as file:
            json_data = json.load(file)
    else:
        json_data = {}  # tworzy pusty słownik, jeśli plik nie istnieje

    if data == "":
        data = "{}"

    # jeśli path jest pusty, ustaw data jako root json_data
    if path == "":
        json_data = json.loads(data)
    else:
        # rozdziel ścieżkę na poszczególne klucze
        keys = path.split('/')

        # przejdź przez klucze, aby dotrzeć do miejsca docelowego
        temp = json_data
        for key in keys[:-1]:
            if key not in temp:
                temp[key] = {}  # tworzy nowy pod-słownik, jeśli klucz nie istnieje
            temp = temp[key]

        # aktualizacja ostatniego klucza, parsując data jako JSON
        temp[keys[-1]] = json.loads(data)

    # zapisz zaktualizowane dane do pliku (tworzy plik, jeśli go nie było)
    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(json_data, file, indent=4)
