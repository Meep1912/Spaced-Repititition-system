from tkinter import *
from tkinter import ttk
import time
import Data
import Card_View


# ------------- Main Window configiration -------------------

def draw_add_card_menu():
    global add_card_menu

    add_card_menu = Toplevel()
    add_card_menu.title("Add Card")
    add_card_menu.geometry("600x500")

    draw_elements()

# --------------------------------------------------------------------------------
# ----------------------------- L O G I C ----------------------------------------
# --------------------------------------------------------------------------------


def done_button(Entries,Done):
    global add_card_menu

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

    key = str(generate_ID())

    # compare
    # generates upto 100 keys if there are colisions 
    i = 0
    while i < 100:
        if key in Data.get_file_data("card_data"):
            key = str(generate_ID())
        else:
            i = 100
        i += 1
    

        
    New_Card_Entry = {
        key:{"Front":front,
             "Back":Back,
             "Card_Type":Card_Type}}

    New_Schedule_Entry = {
        key:{"Due":"0",
             "Interval":1,
             "Ease":2.5,
             "Repeats":0,
             "Lapses":0,
             "Leech":False,
             "Suspended":False}}

    

    # write to card_data file
    Data.save_to_file("card_data",New_Card_Entry)
    # add an blank entry to schedule with matching id
    Data.save_to_file("schedule",New_Schedule_Entry)
    # write to file
    Data.append_decks_file(Deck,key)
    print("hi!")

    

def edit_done_button(Entries,Done,card):
    global add_card_menu

    def get_values(Entries):
        values = []
        for Entry in Entries:
            try:
                values.append(Entry.get("1.0","end-1c"))
            except:
                values.append(Entry.get())
        return(values)


    
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

    key = card

    Replace_Card_Entry = {
        key:{"Front":front,
             "Back":Back,
             "Card_Type":Card_Type}}
    

    # write to card_data file
    Data.delete_in_file("card_data",card)
    Data.save_to_file("card_data",Replace_Card_Entry)


    Card_View.draw_elements()





# --------------------------------------------------------------------------------
# ----------------------------- D R A W I N G ------------------------------------
# --------------------------------------------------------------------------------

def open_add_card_menu():
    draw_add_card_menu()

def draw_elements():

    global add_card_menu

    # ---TITLE ---
    
    Title = ttk.Label(add_card_menu,text="Add Card",style="Body.TLabel")
    
    # --- TYPE SELECTION ---

    Type_Text = ttk.Label(add_card_menu,text="Type: ",style="Body.TLabel")
    Card_Types_dict = Data.get_file_data("card_types")
    Card_Types = []

    for type in Card_Types_dict.keys():
        Card_Types.append(type)

    Type_Entry = ttk.Combobox(add_card_menu,
            state="readonly",
            values=Card_Types,
            style="Body.TCombobox")

    # when the user selects a value, run draw_fields(selected_value)
    def on_type_selected(event):
        draw_fields(event.widget.get())

    Type_Entry.bind("<<ComboboxSelected>>",on_type_selected)


    # --- DECK SELECTION ---         
    Deck_Text = ttk.Label(add_card_menu,
                        text="Deck: ",
                        style="Body.TLabel")
    
    
    Decks_from_file = Data.get_file_data("decks")
    
    Deck_Selection = []

    for Deck in Decks_from_file:
        Deck_Selection.append(Deck)

    Decks_Entry = ttk.Combobox(add_card_menu,
                               state="readonly",
                               values=Deck_Selection,
                               style="Body.TCombobox")

    style = ttk.Style()
    bg = style.lookup("Body.TEntry","fieldbackground")
    fg = style.lookup("Body.TEntry","foreground")

    # get card type data:


    def draw_fields(card_type_chosen):

        for widget in add_card_menu.winfo_children():
            if widget.winfo_class() == "Combobox":
                pass
            else:
                widget.destroy()
        card_type_fields_data = Data.get_file_data("card_types")[card_type_chosen]

        # instantianise labels and entries

        lbls = []
        entries = []

        for field in card_type_fields_data.keys():
            # ------------------ label-------------------
            x_lbl = ttk.Label(add_card_menu, style="Body.TLabel", text=field)
            lbls.append(x_lbl)
            x_lbl.pack()

            # ------------------entry-------------------
            x_entry = Text(add_card_menu, height=4, width=50, background=bg, foreground=fg)
            entries.append(x_entry)
            x_entry.pack()


        # --- DONE BUTTON ---
        Done = ttk.Button(add_card_menu,
            text="Add",style="Body.TLabel",command=lambda: done_button(entries,Done))
        Done.place(x=25, y=410)

    # -- PLACING --
    Title.pack()

    Type_Text.pack()
    Type_Entry.pack()

    Deck_Text.pack()
    Decks_Entry.pack()



def draw_elements_edit_card(card):
    print("hi")
    draw_add_card_menu()

    global add_card_menu

    add_card_menu.title("Edit Card")
    # ------- get the card field data --------------

    card_data = Data.get_file_data("card_data")[card]

    deck = Data.find_deck(card)
    

    # ---TITLE ---
    
    Title = ttk.Label(add_card_menu,
                    text="Edit Card",
                    style="Body.TLabel")
    
    # --- TYPE SELECTIN ---

    Card_Types_dict = Data.get_file_data("card_types")
    Card_Types = []

    for type in Card_Types_dict.keys():
        Card_Types.append(type)

    Type_Text = ttk.Label(add_card_menu,
                        text="Type: ",
                        style="Body.TLabel")

    Type_Entry = ttk.Combobox(add_card_menu,
                              style="Body.TEntry",
                              values=Card_Types)

    Type_Entry.insert(0, card_data["Card_Type"])
    Type_Entry.config(state="readonly")

    # --- DECK SELECTION ---     
    #     
    Deck_Text = ttk.Label(add_card_menu,
                        text="Deck: ",
                        style="Body.TLabel")
    
    Decks_from_file = Data.get_file_data("decks")
    
    Deck_Selection = []

    for Deck in Decks_from_file:
        Deck_Selection.append(Deck)

    Decks_Entry = ttk.Combobox(add_card_menu,
                               values=Deck_Selection,
                               style="Body.TEntry")

    Decks_Entry.insert(0,deck)
    Decks_Entry.config(state="readonly")

    style = ttk.Style()
    bg = style.lookup("Body.TEntry","fieldbackground")
    fg = style.lookup("Body.TEntry","foreground")
    print("fg: ",fg)
    print("bg: ",bg)

    # -- PLACING --
    Title.place(x=10,y=10)
    Type_Text.place(x=15,y=50)
    Type_Entry.place(x=70,y=55)
    Deck_Text.place(x=15,y=80)
    Decks_Entry.place(x=70,y=85)


    # get card type data:

    card_type_fields_data = Data.get_file_data("card_types")[Type_Entry.get()]


    # instantianise labels and entries

    lbls = []
    entries = []

    for field in card_type_fields_data.keys():
        #------------------ label-------------------
        x_lbl = ttk.Label(add_card_menu,style="Body.TLabel",text=field)
        lbls.append(x_lbl)
        x_lbl.pack()

        # ------------------entry-------------------
        x_entry = Text(add_card_menu,height=4,width=50,background=bg,foreground=fg)
        entries.append(x_entry)
        x_entry.insert("0.1",card_data[field])
        x_entry.pack()

    # --- DONE BUTTON ---

    Done = ttk.Button(add_card_menu,
                  text="Add",
                  style="Body.TButton",
                  command=lambda: edit_done_button(entries,Done,card))

    Done.place(x=25,y=410)

