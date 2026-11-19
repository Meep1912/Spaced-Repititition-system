import json
import os
import tempfile

filepaths = {
    "card_data": "Data_Files/card_data.json",
    "schedule": "Data_Files/schedule.json",
    "decks": "Data_Files/decks.json",
    "stats": "Data_Files/stats.json",
    "card_types": "Data_Files/card_types.json",
    "user_settings": "Data_Files/user_settings.json",
}

files = {}  # in-memory store

def load_files_startup():
    for name, path in filepaths.items():
        with open(path, "r", encoding="utf-8") as f:
            files[name] = json.load(f)

def write(name, data): # the only function which writes to file
    path = filepaths[name] # look up the files path
    # create a temporary file with a random name
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: # open the temp file
            json.dump(data, f, indent=4) # write to the temp file
            f.flush() # make the os prioratise the software
            os.fsync(f.fileno()) # forces os to write to file
        os.replace(tmp_path, path) # rename the temp file the real file
    except BaseException: # if an error occurs
        if os.path.exists(tmp_path): # if there is a left over temp file
            os.remove(tmp_path) # delete it
        raise # raise the original error

def get_file_data(name):
    return files[name]

def save_whole_dict(name, data):
    write(name, data)  # write to file
    files[name] = data # internal store only updates if write succeeds 

def save_to_file(name, data_to_write):
    merged = {**files[name], **data_to_write}  # merges old + new
    save_whole_dict(name, merged) # only saves to internal store

def delete_in_file(name, key):
    updated = {k: v for k, v in files[name].items() if k != key} # delete item at key
    save_whole_dict(name, updated) # save internal store

def clear_file(name):
    save_whole_dict(name, {})  # writes an empty dict to internal store

def append_decks_file(deck, card_id):
    decks = files["decks"]
    updated = {**decks, deck: [*decks[deck], card_id]}
    save_whole_dict("decks", updated)


def find_deck(card_id):
    for deck_name, cards in files["decks"].items():
        if card_id in cards:
            return deck_name
    return None


def get_length_of_dict(name):
    return len(files[name])


def get_keys_in_dict(name):
    return list(files[name])
