from tkinter import *
import Card_View 
import Add_Card_View
import Data
from datetime import date
import datetime




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
                    brand_new_cards.append(card_id)
            return brand_new_cards
        
        def find_due_today_or_earlier(cards_schedule_data):

            cards_to_review = []
            
            daily_review_card_limit = 100
            
            count = 0

        
            for card_id, card_schedule in cards_schedule_data.items():
                
                if count >= daily_review_card_limit:
                    break
                
                if card_schedule["Due"] == str(date.today()):
                    print("FOUND ONE")
                    cards_to_review.append(card_id)
                print("-"*10)
                print(card_id)
                print(card_schedule)
                    
            return cards_to_review

    
        # get all the card IDs in the Deck
        deck_data = Data.get_file_data("decks")[deck]

        # for each of the cards in the deck. get the schedule data
        cards_schedule_data = get_schedule_data(deck_data)

        # pick brand_new_cards (ordered by card creation)
        brand_new_cards = pick_new_cards(cards_schedule_data)

        # find cards which are set to be reviewed today
        
        cards_to_review = find_due_today_or_earlier(cards_schedule_data)

        print(cards_to_review)

        # combine new and to revise into list

        queue_of_cards = brand_new_cards + cards_to_review

        return brand_new_cards,cards_to_review, queue_of_cards


def draw_deck_overveiw(deck):

    #----------- Functions -------------------


    #----------- Function calling -------------

    

    # clear frame

    clear_main_frame()
    
    brand_new_cards,cards_to_review, queue_of_cards = what_cards_need_to_be_reviewed(deck)
    
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
                                    command=lambda: Review(queue_of_cards,deck).show_card(),
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

    deck_options = Toplevel()
    deck_options.title((deck + " options"))
    deck_options.geometry("600x400")

    Delete_all_cards = Button(deck_options,
                    text="Delete_Cards",
                    bg="white",
                    relief="flat",
                    command=lambda: delt(),
                    font=(12))
    
    def delt():
        empty = {}
        Data.save_file("schedule", empty)
        Data.save_file("card_data", empty)
        Data.save_file("decks", empty)

    Delete_all_cards.pack()
    
    

def get_card_data(current_card_being_reviewed):
        card_data = Data.get_file_data("card_data")[current_card_being_reviewed]
        front = card_data["Front"]
        back = card_data["Back"]
        type = card_data["Card_Type"]
        return front,back,type

class Review:
    def __init__(self,queue,deck):
        self.queue = queue
        self.index = 0
        self.deck = deck

    
    def card(self):
        return self.queue[self.index]
    card = property(card)

    def show_card(self):
        if self.index >= len(self.queue):
            self.finish()
            return
        self.front, self.back, self.type = get_card_data(self.card)
        self.draw_front()

    def draw_front(self):
        clear_main_frame()

        #---------- Load elements ----------------

        front_field = Label(mainwindow, 
              text=self.front, 
              font=(100), 
              background="white")
        
        back_field = Button(mainwindow,
                text="Flip!!!", 
                command=self.draw_back)
        
        #---------- Draw elements ----------------
        front_field.place(x=100, y=100)
        back_field.place(x=300, y=550)

    def draw_back(self):
        clear_main_frame()

        #---------- Load elements ----------------

        back_field = Label(mainwindow,
                           text=self.back, 
                           font=(100), 
                           background="white")

        pass_btn = Button(mainwindow, 
                          text="Pass", 
                          width=7, 
                          height=3,
                          command=lambda: self.rate(1))
        
        fail_btn = Button(mainwindow, 
                          text="Fail", 
                          width=7, 
                          height=3,
                          command=lambda: self.rate(0))

        #---------- Draw elements ----------------

        back_field.place(x=100, y=100)
        pass_btn.place(x=250, y=550)
        fail_btn.place(x=350, y=550)

    def rate(self, rating):

        all_schedule_data = Data.get_file_data("schedule")
        card_schedule_data = Data.get_file_data("schedule")[str(self.card)]

        # algorithm which adjusts schedule based on rating

        #input interval, ease, repeats

        Interval = card_schedule_data["Interval"]
        Ease = card_schedule_data["Ease"]
        Repeats = card_schedule_data["Repeats"]

        # Ease is the difficulty of the card
        # Interval is days since last review
        # Repeats is the total amount of times the card has been seen
        
        if rating == 0:
            New_Ease = Ease + 0.2

        if rating == 1:
            New_Ease = Ease - 0.2


        Days_till_next_review = New_Ease * Interval
        
        # calculate the date at which the card should be reviewed next 

        New_Due = datetime.date.today() + datetime.timedelta(days=Days_till_next_review)
        New_Due = str(New_Due)
        
        New_Repeats = Repeats + 1
        
        new_schedule_data = {
            "Due":New_Due,
            "Interval":Days_till_next_review,
            "Ease":New_Ease,
            "Repeats":New_Repeats
        }

        # change cards old schedule data to new

        all_schedule_data[str(self.card)] = new_schedule_data
        
        Data.save_file("schedule",all_schedule_data)

        queue_of_cards = what_cards_need_to_be_reviewed(self.deck)

        self.index += 1
        self.show_card()

    def finish(self):
        clear_main_frame()
        
        Title = Label(mainwindow,
                        text="Complete",
                        bg="white",
                        relief="flat",
                        font=(12))
        Title.pack()
        # draw "review complete" screen




def main():
    Data.load_files_startup()
    decks_window_buttons()
    decks_list_elements()
    mainwindow.mainloop()


main()
