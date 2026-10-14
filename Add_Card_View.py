from tkinter import *
from tkinter import ttk
import time
import Data

def open_add_card_menu():
    draw_add_card_menu()

# main window settings 
def draw_add_card_menu():
    add_card_menu = Toplevel()
    add_card_menu.title("Add Card")
    add_card_menu.geometry("600x500")
    add_card_menu.config(bg="white")

    draw_elements(add_card_menu)

# components of window

def draw_elements(add_card_menu):

    # ---TITLE ---
    
    Title = Label(add_card_menu,
                    text="Add Card",
                    bg="white",
                    relief="flat",
                    font=(12))
    
    # --- TYPE SELECTION ---

    Type_Text = Label(add_card_menu,
                        text="Type: ",
                        bg="white",
                        relief="flat",
                        font=(12))
    Card_Types = [
        "Card Type 1",
        "Card Type 2",
        "Card Type 3",
    ]

    Type_Entry = ttk.Combobox(add_card_menu,
            state="readonly",
            values=Card_Types,
    )

    # --- DECK SELECTION ---         
    Deck_Text = Label(add_card_menu,
                        text="Deck: ",
                        bg="white",
                        relief="flat",
                        font=(12))
    Decks_from_file = Data.get_file_data("decks")
    
    Deck_Selection = []

    for Deck in Decks_from_file:
        Deck_Selection.append(Deck)

    Decks_Entry = ttk.Combobox(add_card_menu,
                               state="readonly",
                               values=Deck_Selection)
    
    # --- FRONT FIELD ENTRY BOX ---
    Front_Field_Text = Label(add_card_menu,
                                text="Front: ",
                                bg="white",
                                relief="flat",
                                font=(12))
    Front_Field_Entry = Text(add_card_menu,
                              height=4,
                              width=50,
                              bg="white",
                              font=(12)
                              )

    # --- BACK FIELD ENTRY BOX ---
    Back_Field_Text = Label(add_card_menu,
                                text="Back: ",
                                bg="white",
                                relief="flat",
                                font=(12))
    Back_Field_Entry = Text(add_card_menu,
                              height=4,
                              width=50,
                              bg="white",
                              font=(12)
                              )

    # --- DONE BUTTON ---

    Entries = Front_Field_Entry,Back_Field_Entry,Type_Entry,Decks_Entry
    Done = Button(add_card_menu,
                  text="Add",
                  command=lambda: done_button(Entries,Done,add_card_menu),
                  bg="white",
                  border=1,
                  )
    
    # -- PLACING --
    Title.place(x=10,y=10)

    Type_Text.place(x=15,y=50)
    Type_Entry.place(x=70,y=55)

    Deck_Text.place(x=15,y=80)
    Decks_Entry.place(x=70,y=85)

    Front_Field_Text.place(x=25,y=140)
    Front_Field_Entry.place(x=25,y=170)

    Back_Field_Text.place(x=25,y=270)
    Back_Field_Entry.place(x=25,y=300)

    Done.place(x=25,y=410)

def done_button(Entries,Done,add_card_menu):

    def get_values(Entries):
        values = []
        for Entry in Entries:
            try:
                values.append(Entry.get("1.0","end-1c"))
            except:
                values.append(Entry.get())
        return(values)

    def generate_ID():
        ID = time.time_ns()
        return ID
    
    def compare_ID(key):
        return 0
    
    values = get_values(Entries)

    def reset_done(Done):
        Done.config(text="Add")

    def card_added(Done):
        Done.config(text="Card Added")
        add_card_menu.after(500,reset_done,Done)

    for value in values:
        if not value.strip():
            Done.config(text="Empty Fields")
            add_card_menu.after(500,reset_done,Done)
            return 0
        else:
            add_card_menu.after(500,card_added,Done)


    # break values up into variables

    front = values[0]
    Back = values[1]
    Deck = values[3]
    Card_Type = values[2]

    key = generate_ID()

    # compare
    # generates upto 100 keys if there are colisions 
    i = 0
    while i < 100:
        if key in Data.get_file_data("card_data"):
            key = generate_ID()
        else:
            i = 100
        i += 1
    

        
    New_Card_Entry = {
        key:{"Front":front,
             "Back":Back,
             "Card_Type":Card_Type}}

    New_Schedule_Entry = {
        key:{"Due":"0",
             "Interval":"",
             "Ease":0.0,
             "Repeats":0}}

    

    # write to card_data file
    Data.save_file("card_data",New_Card_Entry)
    # add an blank entry to schedule with matching id
    Data.save_file("schedule",New_Schedule_Entry)
    # write to file
    Data.append_decks_file(Deck,key)
    print("hi!")




# TO DO -

# Need to fetch Card types
# Need to fetch Deck types
    # Need an add card type
    # Need an add deck type

# Need done to write to Data.json
