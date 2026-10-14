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

    # combine new and to revise into list

    queue_of_cards = brand_new_cards + cards_to_review

    # clear frame

    clear_main_frame()
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
    current_queue_item = 0
    start_review_button = Button(mainwindow,
                                    height=5,
                                    width=30,
                                    text="REVIEW ! !",
                                    command=lambda: start_review(queue_of_cards,current_queue_item),
                                    bg="white")
    deck_label = Label(mainwindow,
                       text=deck,
                       font=(500),
                       height=2,
                       width=10,
                       relief="flat",
                       underline=100,
                       bg="white")

    # ----------placing elements---------------

    start_review_button.place(x=300,y=300)
    deck_label.place(x=0,y=0)
    brand_new_cards_lbl.place(x=100,y=100)
    cards_to_review_lbl.place(x=100,y=140)
def draw_deck_options(deck):
    # main window settings 

    card_view = Toplevel()
    card_view.title((deck + " options"))
    card_view.geometry("600x400")


def get_card_data(current_card_being_reviewed):
        card_data = Data.get_file_data("card_data")[current_card_being_reviewed]
        front = card_data["Front"]
        back = card_data["Back"]
        type = card_data["Card_Type"]
        return front,back,type

def start_review(queue_of_cards,current_queue_item):

    # get current card 
    current_card_being_reviewed = queue_of_cards[current_queue_item]
    # -------get the card data of the current card being reviewed--------
    front,back,type = get_card_data(current_card_being_reviewed)


    #----------- Draw the front of the card ----------------

    draw_front(queue_of_cards,current_card_being_reviewed,current_queue_item,front,back)

def draw_front(queue_of_cards,current_card_being_reviewed,current_queue_item,front,back):
        
        clear_main_frame()
        front_field = Label(mainwindow,text=front,font=(100),background="white")
        flip_button = Button(mainwindow,
                             text="Flip!!!",
                             command=lambda:draw_back(current_card_being_reviewed,back))
        front_field.place(x=100,y=100)
        flip_button.place(x=300,y=550)

def draw_back(queue_of_cards,current_card_being_reviewed,current_queue_item,back):

        clear_main_frame()
        back_field_text = Label(mainwindow,text=back,font=(100),background="white")
        pass_button = Button(mainwindow,text="Pass",width=7,height=3,command=lambda: rate_card(current_card_being_reviewed,1))  
        fail_button = Button(mainwindow,text="Fail",width=7,height=3,command=lambda: rate_card(current_card_being_reviewed,0))

        back_field_text.place(x=100,y=100)
        pass_button.place(x=250,y=550)
        fail_button.place(x=350,y=550)

def rate_card(queue_of_cards,current_card_being_reviewed,current_queue_item,rating):

    Data.get_file_data("schedule")[current_card_being_reviewed]

    # algorithm which ajusts schedule based on rating

    current_card_being_reviewed += 1
    start_review(queue_of_cards,current_queue_item)



def main():
    Data.load_files_startup()
    decks_window_buttons()
    decks_list_elements()
    mainwindow.mainloop()


main()