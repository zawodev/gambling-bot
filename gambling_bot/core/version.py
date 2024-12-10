from gambling_bot.data.txt_manager import load, save
from datetime import datetime

def get_current_build_version():
    return load("version")

def generate_current_build_version_file():
    current_date = datetime.now()
    version = f"{current_date.year - 2024}.{current_date.timetuple().tm_yday}.{current_date.hour}.{current_date.minute}"
    save("version", version)

if __name__ == "__main__":
    generate_current_build_version_file()
