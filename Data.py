
import json
files = {}

def load_files_startup():
        global files

        with open("Data.json", "r",encoding="utf-8") as f:
            files["Data"] = json.load(f)

        with open("Schedule.json", "r",encoding="utf-8") as f:
            files["Schedule "] = json.load(f)

def load_file(filename):
    global files
    return files[filename]

def save_file(filename, data):
    with open(filename + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
     

        