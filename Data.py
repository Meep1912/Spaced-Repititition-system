
import json

files = {}

filepaths = {
     "card_data":"Data_Files/card_data.json",
     "schedule":"Data_Files/schedule.json",
     "decks":"Data_Files/decks.json",
     "stats":"Data_Files/stats.json",
     "card_types":"Data_Files/card_types.json",
     "user_settings":"Data_Files/user_settings.json",
}
# make a files dictionary which holds card data and schedule data

def load_files_startup():
    global files
    # read data.json and load info into dictionaries

    for file in filepaths.keys():
        with open(filepaths[file], "r",encoding="utf-8") as f:
            files[file] = json.load(f)



def get_length_of_dict(filename):

    global files

    return(files[filename].len())
    

def get_keys_in_dict(filename):

    global files

    keys = []    
    for file in files[filename].keys():
        keys.append(file)
    return keys


def get_file_data(filename):
    global files
    return files[filename]




def clear_file(file):
    
    empty_dict = {}
    with open(filepaths[file], "w", encoding="utf-8") as f:
        json.dump(empty_dict, f, indent=4)
    
def delete_in_file(file,key):
    data = get_file_data(file)
    data.pop(key)
    save_whole_dict(file,data)

def save_whole_dict(file,dictionary):

    
    with open(filepaths[file], "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=4)
    

def save_to_file(file, data_to_write):

    current_file_data = get_file_data(file)

    current_file_data.update(data_to_write)

    # save a changed dictionary

    save_whole_dict(file,current_file_data)

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

 

def find_deck(card):
    decks = get_file_data("decks")
    
    for deck_name, cards in decks.items():
        if card in cards:
            return deck_name
    return "Empty"
