from tkinter import *
import Card_View 
import Add_Card_View
import Data
from datetime import date



# ------------- Window configiration -------------------
mainwindow = Tk()
canvas = Canvas()
mainwindow.title("S.R.S")
mainwindow.geometry("600x600")
mainwindow.config(bg="white")

# ----------------- Functions ----------------

def decks_window_buttons():
    menubar = Menu(mainwindow)

    # --- File ---
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File",menu=file)

    file.add_command(label="Import",command=None)
    file.add_command(label="Export",command=None)
                            
    # --- Edit ---

    edit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit",menu=edit)

    edit.add_command(label="Edit",command=None)

    # --- Help ---

    help = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help",menu=help)

    help.add_command(label="Help",command=None)

    # --- Decks --- 

    decks = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Decks",menu=decks)

    decks.add_command(label="Decks",command=lambda:decksbuttonpressed())

    # --- Add --- 

    add  = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Add",menu=add)

    add.add_command(label="Add",command=lambda: Add_Card_View.open_add_card_menu())

    # ---View --- 

    view = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View",menu=view)

    view.add_command(label="View",command=lambda: Card_View.open_card_view_menu())

    mainwindow.config(menu=menubar)

# taskbar buttons

def filebuttonpressed():
    pass
def editbuttonpressed():
    pass
def veiwbuttonpressed():
    pass
def toolsbuttonpressed():
    pass
def helpbuttonpressed():
    pass
def decksbuttonpressed():
    clear_main_frame()
    decks_list_elements()

def decks_list_elements():
    deck_list_from_file = Data.get_file_data("decks")
    
    MainButtons = []
    OptionButtons = []

    for deck in deck_list_from_file:

        M_Btn = Button(mainwindow,
                     text=deck,
                     command=lambda d=deck: draw_deck_overveiw(d),
                    width=35)

        Option_Btn = Button(mainwindow,
                            text=". . . ",
                            command=lambda d=deck: draw_deck_options(d),
                            width=2)
    
        MainButtons.append(M_Btn)
        OptionButtons.append(Option_Btn)
    
    x_origin = 100
    initial_y_origin = 100
    counter = 0

    for element in range(0,len(MainButtons)):

        MainButtons[element].place(x=x_origin,y=counter+initial_y_origin)
        OptionButtons[element].place(x=x_origin+260,y=counter+initial_y_origin)
    
        counter += 30

def clear_main_frame():
    for widget in mainwindow.winfo_children():
        if widget.winfo_class() == "Menu":
            pass
        else:
            widget.destroy()

def draw_deck_overveiw(deck):

    #----------- Functions -------------------
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
                brand_new_cards.append(card_id)
        return brand_new_cards
    def find_due_today_or_earlier(cards_schedule_data):

        cards_to_review = []
        daily_review_card_limit = 10
        count = 0 
        
        for card_id, card_schedule in cards_schedule_data.items():
            if count >= daily_review_card_limit:
                break
            if card_schedule["Due"] == date.today():
                cards_to_review.append(card_id)
        return cards_to_review

    #----------- Function calling -------------

    # get all the card IDs in the Deck
    deck_data = Data.get_file_data("decks")[deck]

    # for each of the cards in the deck. get the schedule data
    cards_schedule_data = get_schedule_data(deck_data)

    # pick brand_new_cards (ordered by card creation)
    brand_new_cards = pick_new_cards(cards_schedule_data)

    # find cards which are set to be reviewed today
    cards_to_review = find_due_today_or_earlier(cards_schedule_data)

    # -----------Elements instantination---------------

    brand_new_cards_lbl = Label(mainwindow,
                                text=("New Cards: "+str(len(brand_new_cards))),
                                font=(100),
                                bg="white",
                                )
    cards_to_review_lbl = Label(mainwindow,
                                text=("Cards To Reveiw: "+str(len(cards_to_review))),
                                font=(100),
                                bg="white",
                                )
    cards_learning      = Label(mainwindow,)

    start_review_button = Button(mainwindow,
                                 height=5,
                                 width=30,
                                 text="REVIEW ! !",
                                 command=lambda: draw_review(brand_new_cards,cards_to_review),
                                 bg="white")
    deck_label = Label(mainwindow,
                       text=deck,
                       font=(500),
                       height=2,
                       width=10,
                       relief="flat",
                       underline=100,
                       bg="white")

    # ----------Clear existing stuff-------
    clear_main_frame()
    # ----------placing elements---------------
    start_review_button.place(x=200,y=200)
    deck_label.place(x=0,y=0)
    brand_new_cards_lbl.place(x=100,y=100)
    cards_to_review_lbl.place(x=100,y=140)
        
def draw_deck_options(deck):
    # main window settings 

    card_view = Toplevel()
    card_view.title((deck + " options"))
    card_view.geometry("600x400")

def draw_review(brand_new_cards,cards_to_revise):
    
    # create a queue of cards which need to be reviewd
    
    # Front view
    # Back view
    # pass button
    # fail button

    clear_main_frame()

    pass


# ---------- Calling Functions --------------------------
Data.load_files_startup()
decks_window_buttons()
decks_list_elements()
mainwindow.mainloop()