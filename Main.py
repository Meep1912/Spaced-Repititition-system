from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

from datetime import date
import datetime
import time as time

import Card_View 
import Add_Card_View
import Data
import Scheduler
import Stats

from Theme import theme
from Theme import configure_styles



# ------------- Main Window configiration -------------------

mainwindow = Tk()
canvas = Canvas()
mainwindow.title("S.R.S")
mainwindow.geometry("900x580")
mainwindow.config(bg="white")

# when press esc draw decks view
mainwindow.bind("<Escape>",lambda event: decksbuttonpressed())



# --------------------------------------------------------------------------------
# ----------------------------- L O G I C ----------------------------------------
# --------------------------------------------------------------------------------

# taskbar buttons

def filebuttonpressed():
    pass
def editbuttonpressed():
    pass
def veiwbuttonpressed():
    pass
def toolsbuttonpressed():
    pass
def decksbuttonpressed():
    clear_main_frame()
    decks_list_elements()
    heatmap()
    

def what_cards_need_to_be_reviewed(deck):

        def get_schedule_data(deck_data):
            cards_schedule_data= {}
            for card in deck_data:
                schedule_data = Data.get_file_data("schedule")[str(card)]
                cards_schedule_data[card] = schedule_data
            return cards_schedule_data
        
        def pick_new_cards(cards_schedule_data):
            brand_new_cards = []
            daily_new_card_limit = 10

            count = 0
            for card_id, card_schedule in cards_schedule_data.items():
                if count >= daily_new_card_limit:
                    break
                if card_schedule["Due"] == "0":
                    if card_schedule["Suspended"] == False:
                        brand_new_cards.append(card_id)
            
            return brand_new_cards
        
        def find_due_today_or_earlier(cards_schedule_data):

            cards_to_review = []
            
            daily_review_card_limit = 100
            
            count = 0

        
            for card_id, card_schedule in cards_schedule_data.items():
                if count >= daily_review_card_limit:
                    break
                if card_schedule["Due"] <= str(date.today()):
                    if card_schedule["Suspended"] == False:
                        cards_to_review.append(card_id)
                    
            return cards_to_review

    
        # get all the card IDs in the Deck
        deck_data = Data.get_file_data("decks")[deck]

        # for each of the cards in the deck. get the schedule data
        cards_schedule_data = get_schedule_data(deck_data)

        # pick brand_new_cards (ordered by card creation)
        brand_new_cards = pick_new_cards(cards_schedule_data)

        # find cards which are set to be reviewed today
        
        cards_to_review = find_due_today_or_earlier(cards_schedule_data)

        # combine new and to revise into list

        queue_of_cards = brand_new_cards + cards_to_review

        return brand_new_cards,cards_to_review, queue_of_cards

def get_card_data(current_card_being_reviewed):
        card_data = Data.get_file_data("card_data")[current_card_being_reviewed]
        front = card_data["Front"]
        back = card_data["Back"]
        type = card_data["Card_Type"]
        return front,back,type


# --------------------------------------------------------------------------------
# ----------------------------- D R A W I N G ------------------------------------
# --------------------------------------------------------------------------------


def clear_main_frame():
    for widget in mainwindow.winfo_children():
        if widget.winfo_class() == "Menu":
            pass
        else:
            widget.destroy()

# ----------------------------- Draw Sub-Menus ------------------------------------

def draw_deck_options(deck):

    
    def rename_deck(deck):
        
            # main window settings 
            rename_deck_view = Toplevel()
            rename_deck_view.title("Rename Deck")
            rename_deck_view.geometry("200x50")
        
            def validation(newname,originalname):
                decks_Data = Data.get_file_data("decks")
                if newname.isspace():
                    return 0
                elif newname == "":
                    return 0
                elif newname == originalname:
                    return 1
                elif newname in decks_Data.keys() and newname != originalname:
                    return 2
                else:
                    return newname 
        
            def reset_done(Deck_Entry):
                Deck_Entry.config(text="Rename Deck")
            def pressed_edit_deck_name(Deck_Entry):
                
                New_Deck_Name = Deck_Entry.get()
        
                if validation(New_Deck_Name,deck) == 0:
                    Deck_Entry.config(text="Empty field")
                    rename_deck_view.after(250,reset_done,Deck_Entry)
                if validation(New_Deck_Name,deck) == 1:
                    Deck_Entry.config(text="Unchanged")
                    rename_deck_view.after(250,reset_done,Deck_Entry)
                if validation(New_Deck_Name,deck) == 2:
                    Deck_Entry.config(text="Deck already exists")
                    rename_deck_view.after(250,reset_done,Deck_Entry)
                else:
                    decks = Data.get_file_data("decks")
                    decks[New_Deck_Name] = decks.pop(deck)
                    Data.save_whole_dict("decks",deck)
                    Deck_Entry.config(text="Added")
                    rename_deck_view.after(250,reset_done,Deck_Entry)

                    decksbuttonpressed()
        
        
            def draw_elements(rename_deck_view):
                
                Done_Button = Button(rename_deck_view,
                        
                        text="Delete Deck",

                        # stlying
                        
                        relief="flat",
                        bg=theme["Button"]["BgColur"],
                        fg=theme["Button"]["FontColour"],
                        font=(theme["Button"]["Font"],
                            theme["Button"]["FontSize"]),

                        # command

                        command=lambda: pressed_edit_deck_name(Deck_Entry))

                Deck_Entry = Entry(rename_deck_view,
                        
                        # stlying
                        
                        relief="flat",
                        bg=theme["Entry"]["BgColour"],
                        fg=theme["Entry"]["FontColour"],
                        font=(theme["Entry"]["Font"],
                            theme["Entry"]["FontSize"]))
                
                
                Deck_Entry.insert(0,deck)         
                Done_Button.place(x=0,y=20)
                Deck_Entry.place(x=0,y=0)
            
        
            draw_elements(rename_deck_view)

    def confirmation(deck):
        cards = len(Data.get_file_data("decks")[deck])
        result = messagebox.askokcancel("Deleting deck with "+str(cards)+" cards","are you you want to delete this deck:"+deck,icon="warning")
        if result:
            Delete_Deck(deck)
            decksbuttonpressed()

    def Delete_Deck(deck):
        
        # get card ids in deck
        card_IDs = Data.get_file_data("decks")[deck]
        # get schedule data
        schedule = Data.get_file_data("schedule")
        # get card data
        card_data = Data.get_file_data("card_data")
        
        for card in card_IDs:
            schedule.pop(card)
            card_data.pop(card)

        # delete the data in decks.json
        Data.delete_in_file("decks",deck)

        # save the new dictionarys which have the cards removed
        Data.save_whole_dict("card_data",card_data)
        Data.save_whole_dict("schedule",schedule)
        

    # main window settings 

    deck_options = Toplevel()
    deck_options.title((deck + " options"))
    deck_options.geometry("600x400")


    Delete_deck_btn = Button(deck_options,
                    
                    text="Delete Deck",

                    # stlying
                    
                    relief="flat",
                    bg=theme["Button"]["BgColour"],
                    fg=theme["Button"]["FontColour"],
                    font=(theme["Button"]["Font"],
                          theme["Button"]["FontSize"]),

                    # command

                    command=lambda: confirmation(deck))

    rename_deck_btn = Button(deck_options,
                    
                    text="Delete Deck",

                    # stlying
                    
                    relief="flat",
                    bg=theme["Button"]["BgColour"],
                    fg=theme["Button"]["FontColour"],
                    font=(theme["Button"]["Font"],
                          theme["Button"]["FontSize"]),

                    # command

                    command=lambda: rename_deck(deck))

    Delete_deck_btn.pack()

    rename_deck_btn.pack()

def Add_Deck_View():
    
    # main window settings 
    Add_Deck_view = Toplevel()
    Add_Deck_view.title("Add Deck")
    Add_Deck_view.geometry("200x50")

    def validation(name):
        if name.isspace():
            return 0
        elif name == "":
            return 0
        else:
            return name 

    def reset_done(button):
        button.config(text="Add Deck")

    def pressed_add_deck(Deck_Entry,button):
        
        New_Deck = {Deck_Entry.get(): []}

        if validation == 0:
            button.config(text="Empty field")
            Add_Deck_view.after(250,reset_done,button)
        else:
            Data.save_to_file("decks",New_Deck)
            button.config(text="Added")
            Add_Deck_view.after(250,reset_done,button)
            decksbuttonpressed()


    def draw_elements(Add_Deck_view):
        
        Title = ttk.Button(Add_Deck_view,
                      text="Add Deck",
                      style="Body.TButton",
                       command=lambda: pressed_add_deck(Deck_Entry, Title))
        
        Deck_Entry = ttk.Entry(Add_Deck_view,
                           style="Body.TEntry")
                      
        Title.place(x=0,y=20)
        Deck_Entry.place(x=0,y=0)
    

    draw_elements(Add_Deck_view)

def heatmap():
    def reveiws_in_day(date):
        all_stats = Data.get_file_data("stats")
        day_stats = all_stats.get(str(date),{})
        return ( len(day_stats) )

    def colour_gradient(count):
        if count == 0:
            return(rgb_to_hex(189,189,189))
        else:
            # rgb goes from 0 - 255
            green = min(255,60 +count*5)
            return(rgb_to_hex(0,green,0))

    def rgb_to_hex(r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def draw_days():
        today = datetime.date.today()
        weeks = 52
        # Monday of the current week, then go back (weeks - 1) more weeks
        start = today - datetime.timedelta(days=today.weekday() + 7 * (weeks - 1))

        heatmap_frame = Frame(mainwindow)

        for i in range((today - start).days + 1):
            day = start + datetime.timedelta(days=i)
            column, row = divmod(i, 7)    # row 0 = Monday ... row 6 = Sunday

            Frame(heatmap_frame,
                  bg=colour_gradient(reveiws_in_day(day)),
                  width=12, height=12).grid(row=row, column=column, padx=1, pady=1)

        heatmap_frame.place(x=100, y=400)

    draw_days()

def Help_View(selected_theme):
    
    # main window settings 
    Help_view_frame = Toplevel()
    Help_view_frame.title("Help")
    Help_view_frame.geometry("500x400")
    def Draw_Elements(selected_theme):

    

        text = Text(Help_view_frame,
                     wrap="word",
                     width=50,
                     height=10,
                     # styling
                     background = selected_theme["WidgetBackground"],
                     foreground= selected_theme["WidgetForeground"],
                     font=selected_theme["Font"],
                     insertbackground=selected_theme["Foreground"])

        text.pack()

        scroll = Scrollbar(Help_view_frame, command=text.yview)
        text.config(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y")
        text.pack(side="left",fill="both",expand=True)

        

        text.tag_config("link",

                        # styling
                        foreground=selected_theme["Selection"],
                        underline=True,
                        font=(selected_theme["Font"]))
        
        text.tag_config("heading",

                        # styling
                        font=selected_theme["Font"])
        
        sections = {
            "intro": ("Introduction", "S.R.S stands for Spaced Repitition System this software aims to help you forget less, how does it do that? It tries to predict when you are about to forget something and then reminds you at that estimated time."),
            "setup": ("Fundementals", "\nCreating Decks:\n\n""press Decks > add deck, then a window with an entry box should appear, Type what you would like to name your deck then press: Add Deck"
            "\n\nCreating Cards:\n\n""Now that you have a deck you can start to fill it with cards: press Add > Add Card, then a window with multiple entry boxes should appear,choose a type, a deck and then fill the front and back fields"),
            "usage": ("Usage","hello world")}

        def jump(mark):
            text.see(mark)
            text.yview(mark)

        text.insert("end","Contents\n","heading")

        # table of contents
        for mark, (title, body) in sections.items():
            tag = f"toc_{mark}"
            text.insert("end", title + "\n", ("link", tag))
            text.tag_bind(tag, "<Button-1>", lambda e, m=mark: jump(m))
            text.tag_bind(tag, "<Enter>", lambda e: text.config(cursor="hand2"))
            text.tag_bind(tag, "<Leave>", lambda e: text.config(cursor=""))

        text.insert("end", "\n")

        # sections
        for mark, (title, body) in sections.items():
            text.mark_set(mark, "end-1c")
            text.mark_gravity(mark, "left")
            text.insert("end", title + "\n", "heading")
            text.insert("end", body + "\n\n")

        text.config(state="disabled")

    Draw_Elements(selected_theme)    

def Card_Types_View():


    # title

    # card types veiw 
    # card fields veiw

    def Fields_View(card_type):

        field_menu = Toplevel()
        field_menu.title("Add new field")
        field_menu.geometry("200x300")

# ignore

        def on_field_select(event):
            selection = listbox_of_fields.selection()
            if not selection:
                return
            field, field_type = listbox_of_fields.item(selection[0], "values")


        def save_button(Front_Entry, Back_Entry):
            pass



        def add_field_button(card_type):
            #
            def field_done(name_entry, type_box, btn, card_type):
                def flash(text, ms=500):
                    btn.config(text=text)
                    field_menu.after(ms, lambda: btn.config(text="Add"))

                name = name_entry.get().strip()
                media_type = type_box.get().strip()

                if not name or not media_type:
                    flash("Empty Fields")
                    return

                existing = Data.get_file_data("card_types")[card_type]
                if name in existing:
                    flash("Field Name Exists")
                    return

                # save_to_file merges at the top level, so pass the whole card type's dict
                Data.save_to_file("card_types", {card_type: {**existing, name: ["Front", media_type]}})
                listbox_of_fields.insert("", "end", values=(name, media_type))
                flash("Field Added", 400)

            # name of new field
            ttk.Label(field_menu,text="Name of new field",style="Body.TLabel").pack()
            new_field_name = ttk.Entry(field_menu, style="Body.TEntry")

            # combo-box (field type)
            types = ["Text","Image"]
            ttk.Label(field_menu,text="Field type",style="Body.TLabel").pack()
            new_field_type = ttk.Combobox(field_menu, style="Body.TCombobox",values=types)
            
            # submit button
            done_btn = ttk.Button(field_menu,text="Add",style="Body.TButton",
                command= lambda: field_done(new_field_name,new_field_type, done_btn, card_type))

            new_field_name.pack()
            new_field_type.pack()
            done_btn.pack()
            #
# ingore

        # get card types
        fields = Data.get_file_data("card_types")[card_type]
        # set a title
        title = ttk.Label(field_menu, style="Heading.TLabel", text="Fields")
        


        style = ttk.Style()
        bg = style.lookup("Body.TEntry","fieldbackground")
        fg = style.lookup("Body.TEntry","foreground")

        
        fields_frame = ttk.Frame(card_type_menu, 
                                 style="Frame.TFrame",)
        
        Front_Field_lbl = ttk.Label(fields_frame, text="Front of Card", style="Body.TLabel")
        Front_Field_Entry = Text(fields_frame, height=5, width=20, background=bg,
                              foreground=fg, font=(12))
        Back_Field_lbl = ttk.Label(fields_frame, text="Back of Card", style="Body.TLabel")
        Back_Field_Entry = Text(fields_frame, height=5, width=20, background=bg,
                              foreground=fg, font=(12))

        add_field_btn = ttk.Button(card_type_menu,
                                   text = "add field",
                                   style="Body.TButton",
                                   command= lambda: add_field_button(card_type))

        save_btn = ttk.Button(card_type_menu,
                                   text = "Save",
                                   style="Body.TButton",
                                   command= lambda: save_button(Front_Field_Entry, Back_Field_Entry))
        # ------------- LIST BOX --------------------
        listbox_of_fields = ttk.Treeview(card_type_menu,
            selectmode="browse", style="Treeview.Heading")
        listbox_of_fields["columns"] = ("0", "1")

        listbox_of_fields["show"] = "headings"
        listbox_of_fields.column("0", width=90)
        listbox_of_fields.heading("0", text="field")
        listbox_of_fields.column("1", width=90)
        listbox_of_fields.heading("1", text="type")
        listbox_of_fields.bind("<<TreeviewSelect>>", on_field_select)


        front_string = ""
        back_string = ""

        for field in card_type_fields.keys():
            
            side = card_type_fields[field][0]
            field_type = card_type_fields[field][1]

            listbox_of_fields.insert("","end", values=(field,field_type))

            if side == "Front":
                front_string = (front_string + field + "\n")
            if side == "Back":
                back_string = (back_string + field + "\n")
            if side == "Both":
                front_string = (front_string + field + "\n")
                back_string = (back_string + field + "\n")

        
        Front_Field_Entry.insert("1.0",front_string)
        Back_Field_Entry.insert("1.0",back_string)

        # Placing
        title.pack()
        listbox_of_fields.pack(side="left", anchor="n", padx=5)
        add_field_btn.pack(side="top",anchor="s")
        save_btn.pack(side="top",anchor="s")
        fields_frame.pack(side="left", anchor="n", padx=5)
        Front_Field_lbl.pack(anchor="w")
        Front_Field_Entry.pack(anchor="e")
        Back_Field_lbl.pack(anchor="w")
        Back_Field_Entry.pack(anchor="e")
        
      
    def card_types_():

        def on_card_type_select(event):
            selection = listbox_of_types.selection()
            if not selection:
                return
            (card_type,) = listbox_of_types.item(selection[0], "values")
            Fields_View(card_type)
      
        title = ttk.Label(card_type_menu,
                        style="Heading.TLabel",
                        text="Card Types")

        title.pack()

        card_types = Data.get_file_data("card_types")
        listbox_of_types = ttk.Treeview(card_type_menu,
                                        selectmode="browse",
                                        style="Treeview.Heading")
        
        listbox_of_types["columns"] = ("0")
        listbox_of_types["show"] = "headings"
        listbox_of_types.column("0", width=90)
        listbox_of_types.bind("<<TreeviewSelect>>", on_card_type_select)
        listbox_of_types.pack()


                            
        card_types_list = []
        for type in card_types.keys():
            card_types_list.append(type)
            listbox_of_types.insert("","end", values=card_types_list)


def User_Settings_View():

    

    def draw_elements(User_Settings_frame):

        fields = {}

        # Themes
        available_themes = []    
        for value in theme.keys():
            available_themes.append(value)


        themes_lbl = ttk.Label(
            User_Settings_frame,
            text="Themes",
            style="Body.TLabel")
        themes_lbl.pack(anchor=W)

        themes_entry_var = StringVar()
        themes_entry = ttk.Combobox(
            User_Settings_frame,
            values=available_themes,
            style="Body.TCombobox",
            textvariable=themes_entry_var)
        themes_entry.pack(anchor=W)

        fields["Theme"] = themes_entry_var





        # Leech point
        leechpoint_lbl = ttk.Label(
            User_Settings_frame,
            text="Leech Point",
            style="Body.TLabel")
        leechpoint_lbl.pack(anchor=W)

        leechpoint_var = IntVar()
        leechpoint_entry = ttk.Spinbox(
            User_Settings_frame,
            from_=0,
            to=50,
            style="Body.TSpinbox",
            textvariable=leechpoint_var
            )
        leechpoint_entry.pack(anchor=W)

        fields["Leech_Point"] = leechpoint_var




        # Suspend leeches
        suspend_leeches_lbl = ttk.Label(
            User_Settings_frame,
            text="Suspend cards when they pass leechpoint",
            style="Body.TLabel")
        suspend_leeches_lbl.pack(anchor=W)

        suspend_leeches_var = IntVar()
        suspend_leeches_entry = ttk.Checkbutton(
            User_Settings_frame,
            style="Body.TCheckbutton",
            variable=suspend_leeches_var)
        suspend_leeches_entry.pack(anchor=W)

        fields["Suspend_Leech"] = suspend_leeches_var





        # Learning steps
        available_learning_steps = ["1, 3", "2, 3", "1,2,3,4", "1,1,2", "1,2,3"]

        learning_steps_lbl = ttk.Label(
            User_Settings_frame,
            text="Learning Steps",
            style="Body.TLabel")
        learning_steps_lbl.pack(anchor=W)

        learning_steps_var = StringVar()
        learning_steps_entry = ttk.Combobox(
            User_Settings_frame,
            values=available_learning_steps,
            style="Body.TCombobox",
            textvariable=learning_steps_var)
        learning_steps_entry.pack(anchor=W)

        fields["Learning_Steps"] = learning_steps_var





        # Hide rate buttons
        hide_bar_in_review_lbl = ttk.Label(
            User_Settings_frame,
            text="Hide Buttons in review (use keybinds)",
            style="Body.TLabel")
        hide_bar_in_review_lbl.pack(anchor=W)

        hide_bar_in_review_var = IntVar()
        hide_bar_in_review_entry = ttk.Checkbutton(
            User_Settings_frame,
            style="Body.TCheckbutton",
            variable=hide_bar_in_review_var)
        hide_bar_in_review_entry.pack(anchor=W)

        fields["No_Review_Buttons"] = hide_bar_in_review_var





        # Hide interval
        hide_interval_in_review_lbl = ttk.Label(
            User_Settings_frame,
            text="Hide interval in review",
            style="Body.TLabel")
        hide_interval_in_review_lbl.pack(anchor=W)

        hide_interval_in_review_var = IntVar()
        hide_interval_in_review_entry = ttk.Checkbutton(
            User_Settings_frame,
            style="Body.TCheckbutton",
            variable=hide_interval_in_review_var)
        hide_interval_in_review_entry.pack(anchor=W)

        fields["No_Interval_In_Review"] = hide_interval_in_review_var


        done_btn = ttk.Button(
            User_Settings_frame,
            text="DONE !",
            style="Body.TButton",
            command= lambda: done(fields)
        )
        done_btn.pack(anchor=W)


        user_settings_data = Data.get_file_data("user_settings")

        themes_entry_var.set(user_settings_data["Theme"])
        leechpoint_var.set(str(user_settings_data["Leech_Point"]))
        learning_steps_var.set(user_settings_data["Learning_Steps"])


        suspend_leeches_var.set(user_settings_data["Suspend_Leech"])
        hide_bar_in_review_var.set(user_settings_data["No_Review_Buttons"])
        hide_interval_in_review_var.set(user_settings_data["No_Interval_In_Review"])

        learning_steps_entry.config(state="readonly")
        themes_entry.config(state="readonly")



    def done(fields):

        def get_values(Entries):
            values = Entries.copy()
            for Entry in Entries.keys():
                    values[Entry] = Entries[Entry].get()          
            return(values)
        
        values = get_values(fields)
        configure_styles(theme[values["Theme"]])
        mainwindow.config(bg=theme[values["Theme"]]["Background"])
        Data.save_whole_dict("user_settings",values)

        mainwindow.option_add("*Toplevel.background", theme[values["Theme"]]["Background"])
        decksbuttonpressed()




    # window config
    settings_frame = Toplevel()
    settings_frame.title("Settings")
    settings_frame.geometry("240x470")

    draw_elements(settings_frame)

    

# Draw menu bar at the top of the screen

def decks_window_buttons(mainwindow, selected_theme):


    def build_menubar(mainwindow, selected_theme):
        menubar = Menu(mainwindow, background=selected_theme["WidgetBackground"],foreground=selected_theme["WidgetForeground"])

        def make_menu(label):
            
            # Styling 
            m = Menu(menubar, tearoff=0)
            menubar.add_cascade(label=label, menu=m)
            return m

        # --- File ---
        file_menu = make_menu("File")
        file_menu.add_command(label="Import", command=None)
        file_menu.add_command(label="Export", command=None)

        # --- Edit ---
        edit_menu = make_menu("Edit")
        edit_menu.add_command(label="Card Types", command=lambda: Card_Types_View())
        edit_menu.add_command(label="Preferences",command=lambda: User_Settings_View())

        # --- Help ---
        help_menu = make_menu("Help")
        help_menu.add_command(label="Help", command=lambda: Help_View(selected_theme))

        # --- Decks ---
        decks_menu = make_menu("Decks")
        decks_menu.add_command(label="Decks", command=lambda: decksbuttonpressed())
        decks_menu.add_command(label="Add Deck", command=lambda: Add_Deck_View())

        # --- Add ---
        add_menu = make_menu("Add")
        add_menu.add_command(label="Add Card",
                            command=lambda: Add_Card_View.open_add_card_menu())

        # --- View ---
        view_menu = make_menu("View")
        view_menu.add_command(label="View",
                            command=lambda: Card_View.open_card_view_menu())
        view_menu.add_command(label="Stats",
                            command=lambda: Stats.Open_stat_view(mainwindow))

        mainwindow.config(menu=menubar)

    build_menubar(mainwindow, selected_theme)
# List all the decks

def decks_list_elements():
    deck_list_from_file = Data.get_file_data("decks")
    
    MainButtons = []
    OptionButtons = []

    for deck in deck_list_from_file:

        m_btn = ttk.Button(mainwindow,
                    text=deck,
                    width=35,
                    style="Body.TButton",
                    command=lambda d=deck: draw_deck_overveiw(d))

        option_btn = ttk.Button(mainwindow,
                    text=". . .",
                    width=2,
                    style="Body.TButton",
                    command=lambda d=deck: draw_deck_options(d))

        MainButtons.append(m_btn)
        OptionButtons.append(option_btn)
    
    x_origin = 300
    initial_y_origin = 100
    counter = 0

    for element in range(0,len(MainButtons)):
        # draw all of users decks
        MainButtons[element].place(x=x_origin,y=counter+initial_y_origin)
        OptionButtons[element].place(x=x_origin+260,y=counter+initial_y_origin)
    
        counter += 45



# Preview before reveiwing

def draw_deck_overveiw(deck):

    #----------- Functions -------------------

    # clear frame

    clear_main_frame()
    
    brand_new_cards,cards_to_review, queue_of_cards = what_cards_need_to_be_reviewed(deck)

    # Key binds 

    mainwindow.bind("<Return>",lambda event: Review(queue_of_cards,deck).show_card())
    mainwindow.bind("<space>", lambda event: Review(queue_of_cards,deck).show_card())
    
    # -----------Elements instantination---------------
    

    brand_new_cards_lbl = ttk.Label(mainwindow,
                                    text=("New Cards: "+str(len(brand_new_cards))),
                                    style="Body.TLabel")
    
    cards_to_review_lbl = ttk.Label(mainwindow,
                                    text=("Cards To Reveiw: "+str(len(cards_to_review))),
                                    style="Body.TLabel")
    
    start_review_button = ttk.Button(mainwindow,
                                text="REVIEW ! !",
                                style="Body.TButton",
                                command=lambda: Review(queue_of_cards,deck).show_card(),)
    
    deck_label = ttk.Label(mainwindow,
                       text=deck,
                       style="Body.TLabel")

    # ----------placing elements---------------

    start_review_button.place(x=300,y=300)
    deck_label.place(x=0,y=0)
    brand_new_cards_lbl.place(x=100,y=100)
    cards_to_review_lbl.place(x=100,y=140)

# Main review logic

class Review:
    def __init__(self,queue,deck):
        self.queue = queue
        self.index = 0
        self.deck = deck
        data = Data.get_file_data("user_settings")
        self.HideButtons = data["No_Review_Buttons"]
        self.HideInterval= data["No_Interval_In_Review"]

    
    def card(self):
        return self.queue[self.index]
    card = property(card)

    def show_card(self):

        # unbind
        mainwindow.unbind("<Return>")
        mainwindow.unbind("<space>")

        brand_new_cards,cards_to_review, queue_of_cards = what_cards_need_to_be_reviewed(self.deck)
        if self.index >= len(self.queue):
            if len(queue_of_cards) == 0:
                self.finish()
                return
            else:
                self.queue = queue_of_cards
                self.index = 0

        self.front, self.back, self.type = get_card_data(self.card)
        
        self.draw_front()
        

    def draw_front(self):
        clear_main_frame()

        # ----- key binds -----
                
        # clear previous binds
        
        mainwindow.unbind("<Key-1>")
        mainwindow.unbind("<Key-0>")
        
        # bind new 
                
        mainwindow.bind("<Return>", lambda event: self.draw_back())
        mainwindow.bind("<space>",  lambda event: self.draw_back())


        self.start = time.time()
        #---------- Load elements ----------------


        # styling



        front_field_frame = ttk.Frame(mainwindow, width = 300, height = 100)
        front_field_frame.pack_propagate(False)
        front_field = ttk.Label(front_field_frame, 
              text=self.front,
              style="Body.TLabel",
              justify="center",
              anchor="center",
              wraplength=400)
        if self.HideButtons == 0:
            Flip_btn = ttk.Button(mainwindow,
                    text="Reveal",
                    padding=(3,5),
                    style="Body.TButton",
                    command=self.draw_back)
            Flip_btn.pack(side="bottom")
        
        #---------- Draw elements ----------------
        front_field_frame.pack(fill=BOTH,expand=True)
        front_field.pack(anchor=CENTER,fill=BOTH,expand=True)
        



    def draw_back(self, event=None):
        clear_main_frame()
        # --- key binds ----

        # clear previous keybinds

        mainwindow.unbind("<Return>")
        mainwindow.unbind("<space>")

        # bind new keybinds

        mainwindow.bind("<Key-1>",lambda event: self.rate(1))
        mainwindow.bind("<Key-0>",lambda event: self.rate(0))

        #---------- Load elements ----------------

        buttons = ttk.Frame(mainwindow,
                            style="Frame.TFrame")

        back_field_frame = ttk.Frame(mainwindow, width=300, height=100)
        back_field_frame.pack_propagate(False)

        back_field = ttk.Label(back_field_frame, 
              text=self.back,
              style="Body.TLabel",
              justify="center",
              anchor="center",
              wraplength=400)

        if self.HideButtons == 0:

            pass_btn = ttk.Button(buttons, 
                            text="Pass",
                            style="Body.TButton",
                            command=lambda: self.rate(1))
            pass_btn.pack(side=LEFT, padx=5)

            fail_btn = ttk.Button(buttons, 
                            
                            text="Fail", 
                            style="Body.TButton",
                            command=lambda: self.rate(0))
            fail_btn.pack  (side=LEFT,pady=5)

        if self.HideInterval == 0:
            card_schedule_data = Data.get_file_data("schedule")[str(self.card)]

            Interval_ = card_schedule_data["Interval"]
            
            current_interval = ttk.Label(mainwindow,
                                    text=str(Interval_)+" Days",
                                    style="Body.TLabel")
            current_interval.pack(side="bottom")



                                 
        #---------- Draw elements ----------------

        back_field_frame.pack(anchor="center", fill="both",expand=True)

        back_field.pack(anchor="center", fill="both",expand=True)


        

    def rate(self, rating):

        # stop timer

        time_taken = time.time() - self.start

        # get existing card schedule data

        all_schedule_data = Data.get_file_data("schedule")
        card_schedule_data = Data.get_file_data("schedule")[str(self.card)]

        # split existing card schedule data

        Interval = card_schedule_data["Interval"]
        Ease = card_schedule_data["Ease"]
        Repeats = card_schedule_data["Repeats"]
        Lapses = card_schedule_data["Lapses"]
        LeechState = card_schedule_data["Leech"]
        SuspendState = card_schedule_data["Suspended"]


        new_schedule_data = Scheduler.schedule(Interval,Ease,Repeats,Lapses,LeechState,SuspendState,rating)
        
        all_schedule_data[str(self.card)] = new_schedule_data
        
        Data.save_to_file("schedule",all_schedule_data)
        

        # get old stats data
        all_stats = Data.get_file_data("stats")

        # get data for new stats entry
        time_of_day = datetime.datetime.now().strftime("%H:%M:%S")
        todays_date = datetime.date.today()
        todays_date = str(todays_date)
        all_stats.setdefault(todays_date, {})

        # build stats entry list    
        all_stats[todays_date].setdefault(str(self.card), []).append(
        [time_taken,
        rating, 
        time_of_day])

        # write new stats data
        Data.save_to_file("stats",all_stats)

        # pointer to next card
        self.index += 1

        # show the next card

        self.show_card()

    def finish(self):

        clear_main_frame()

        Title = ttk.Label(mainwindow,
                        text="Complete",
                        style="Body.TLabel")
        Title.pack()
        # draw "review complete" screen


# Calling functions 

def main(mainwindow):
    Data.load_files_startup()
    # get preference
    user_settings_data = Data.get_file_data("user_settings")
    selected_theme = theme[user_settings_data["Theme"]]
    configure_styles(selected_theme)
    # set mainwindow background
    mainwindow.config(background=selected_theme["Background"])
    # set all frames background
    mainwindow.option_add("*Toplevel.background", selected_theme["Background"])
    decks_window_buttons(mainwindow,selected_theme)
    decks_list_elements()
    heatmap()
    
    mainwindow.mainloop()


main(mainwindow)
