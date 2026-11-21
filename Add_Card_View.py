from tkinter import *
from tkinter import ttk
import time
import Data
import Card_View
from tkinter import filedialog
import os
import Media


# ------------- Main Window configiration -------------------

def draw_add_card_menu():
    global add_card_menu

    add_card_menu = Toplevel()
    add_card_menu.title("Add Card")
    add_card_menu.geometry("600x500")

    def get_first_type():
        for type in Data.get_file_data("card_types"):
            return type

    draw_elements(get_first_type())


## Menu Bar Add Card

def flash(Done,text):
        def reset_done(Done):
            Done.config(text="Add")
        Done.config(text=text)
        add_card_menu.after(250,reset_done,Done)

def done_button(fields, Done, Deck, Type):
    card_type = Type.get()
    deck = Deck.get()
    if not card_type or not deck:
        flash(Done, "Pick type + deck")
        return

    # validate everything first, write nothing yet
    values = {}
    for name, media_type, get_value, clear in fields:
        value = get_value()
        if not value:
            flash(Done, "Empty Fields")
            return
        values[name] = value

    # unique key
    existing = Data.get_file_data("card_data")
    key = str(time.time_ns())
    while key in existing:
        key = str(time.time_ns())

    # build the card, importing media only now that validation has passed
    card = {}
    for name, media_type, get_value, clear in fields:
        if media_type in ("Media", "Image"):
            try:
                card[name] = Media.import_media(values[name])   # returns the hashed filename
            except OSError:
                flash(Done, "Can't read file")
                return
        else:
            card[name] = values[name]
    card["Card_Type"] = card_type

    schedule_entry = {"Due": "0", "Interval": 1, "Ease": 2.5, "Repeats": 0,
                      "Lapses": 0, "Leech": False, "Suspended": False}

    Data.append_decks_file(deck, key)
    Data.save_to_file("card_data", {key: card})
    Data.save_to_file("schedule", {key: schedule_entry})

    for name, media_type, get_value, clear in fields:
        clear()
    flash(Done, "Added")

def draw_elements(type_selected, deck=""):
    global add_card_menu

    def on_type_selected(event):
        type_selected = event.widget.get()
        for widget in add_card_menu.winfo_children():
            widget.destroy()
        draw_elements(type_selected)
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

    Type_Entry.set(type_selected)


    # when the user selects a value, run draw_fields(selected_value)
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

    if deck:
         Decks_Entry.set(deck) #

    style = ttk.Style()
    bg = style.lookup("Body.TEntry","fieldbackground")
    fg = style.lookup("Body.TEntry","foreground")

    # get card type data:


    def draw_fields(card_type_chosen):

        card_type_fields_data = Data.get_file_data("card_types")[card_type_chosen]

        # instantianise labels and entries

        fields = []   # one entry per field: (name, media_type, get_value, clear)

        for field, (side, media_type) in card_type_fields_data.items():
            ttk.Label(add_card_menu, style="Body.TLabel", text=field).pack()

            if media_type == "Text":
                box = Text(add_card_menu, height=4, width=50, background=bg, foreground=fg)
                box.pack()
                fields.append((
                    field, media_type,
                    lambda b=box: b.get("1.0", "end-1c").strip(),
                    lambda b=box: b.delete("1.0", "end"),
                ))

            elif media_type in ("Image"):
                chosen = {"path": ""}
                status = ttk.Label(add_card_menu, style="Body.TLabel", text="No file chosen")

                def choose(chosen=chosen, status=status):
                    path = filedialog.askopenfilename(
                        parent=add_card_menu,
                        title="Choose a file",
                        filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
                    if not path:                     # cancelled
                        return
                    chosen["path"] = path
                    status.config(text=os.path.basename(path))

                def clear_media(chosen=chosen, status=status):
                    chosen["path"] = ""
                    status.config(text="No file chosen")

                ttk.Button(add_card_menu, text="Choose file", style="Body.TButton",
                        command=choose).pack()
                status.pack()
                fields.append((field, media_type, lambda c=chosen: c["path"], clear_media))

            else:
                raise ValueError(f"Unknown field type {media_type!r} in {card_type_chosen}")



        # --- DONE BUTTON ---
        Done = ttk.Button(add_card_menu,
            text="Add",style="Body.TButton",command=lambda: done_button(fields,Done,Decks_Entry,Type_Entry))
        Done.pack(pady=10)

    # -- PLACING --
    Title.pack()

    Type_Text.pack()
    Type_Entry.pack()

    Deck_Text.pack()
    Decks_Entry.pack()
    draw_fields(type_selected)



## Card View Edit Card

## TODO EDIT CARD NEEDS UPDATING WITH TYPE STUFF

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

    Done.pack(pady=10)

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

## TODO EDIT CARD NEEDS UPDATING WITH TYPE STUFF
