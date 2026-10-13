
import json

files = {}

filepaths = {
     "card_data":"Data_Files/card_data.json",
     "schedule":"Data_Files/card_data.json",
     "decks":"Data_Files/card_data.json",
}
# make a files dictionary which holds card data and schedule data

def load_files_startup():
    global files
    # read data.json and load info into dictionaries
    with open(filepaths["card_data"], "r",encoding="utf-8") as f:
        files["card_data"] = json.load(f)

    with open(filepaths["schedule"], "r",encoding="utf-8") as f:
        files["schedule"] = json.load(f)
    
    with open(filepaths["decks"], "r",encoding="utf-8") as f:
        files["decks"] = json.load(f)

def get_file_data(filename):
    global files
    return files[filename]

def save_file(file, data_to_write):

    current_file_data = get_file_data(file)

    current_file_data.update(data_to_write)

    # save a changed dictionary

    with open(filepaths[file], "w", encoding="utf-8") as f:
        json.dump(current_file_data, f, indent=4)

def append_decks_file(Deck,key):

    # fetch all deck data
    all_decks = get_file_data("decks")
    # find a single deck
    single_deck = all_decks[Deck]
    # add the new card id to deck list
    single_deck.append(key)
    # write the whole list of cards back to the list of decks
    all_decks[Deck] = single_deck

    with open(filepaths["decks"], "w", encoding="utf-8") as f:
        json.dump(all_decks, f, indent=4)

 

        