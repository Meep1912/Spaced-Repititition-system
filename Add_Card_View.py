from tkinter import *
from tkinter import ttk
import time

def open_add_card_menu():
    draw_add_card_menu()

# main window settings 
def draw_add_card_menu():
    add_card_menu = Toplevel()
    add_card_menu.title("Project")
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
            values=Card_Types
    )

    # --- DECK SELECTION ---         
    Deck_Text = Label(add_card_menu,
                        text="Deck: ",
                        bg="white",
                        relief="flat",
                        font=(12))
    Decks = [
        "Deck 1",
        "Deck 2",
        "Deck 3",
    ]
    Decks_Entry = ttk.Combobox(add_card_menu,
            values=Decks
    )

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
                              relief="flat",
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
                              relief="flat",
                              font=(12)
                              )

    # --- DONE BUTTON ---

    Entries = Type_Entry,Decks_Entry,Front_Field_Entry,Back_Field_Entry
    Done = Button(add_card_menu,
                  text="Done",
                  command=lambda: done_button(Entries),
                  relief="flat",
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

def done_button(Entries):

    def get_values(Entries):
        values = []
        for Entry in Entries:
            try:
                values.append(Entry.get("1.0",END))
            except:
                values.append(Entry.get())
        return(values)

    def generate_id():
        id = time.time_ns()
        return id

    values = get_values(Entries)
    id = generate_id()

    def Compare_Card_ID():
        pass
    
    def write_to_file():
        pass





# TO DO -

# Need to fetch Card types
# Need to fetch Deck types
    # Need an add card type
    # Need an add deck type

# Need done to write to Data.json
