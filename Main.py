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
    decks.add_command(label="Add Deck",command=lambda:Add_Deck_View())

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


def Add_Deck_View():
    
    # main window settings 
    Add_Deck_view = Toplevel()
    Add_Deck_view.title("Add Deck")
    Add_Deck_view.geometry("200x50")


    def pressed_add_deck(Deck_Entry):
        
        New_Deck = {Deck_Entry.get(): []}

        Data.save_file("decks",New_Deck)
        decks_list_elements()


    def draw_elements(Add_Deck_view):
        
        Title = Button(Add_Deck_view,
                      text="Add Deck",
                       command=lambda: pressed_add_deck(Deck_Entry))
        
        Deck_Entry = Entry(Add_Deck_view)
                      
        Title.place(x=0,y=20)
        Deck_Entry.place(x=0,y=0)
    

    draw_elements(Add_Deck_view)
    



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

        print(cards_to_review)

        # combine new and to revise into list

        queue_of_cards = brand_new_cards + cards_to_review

        return brand_new_cards,cards_to_review, queue_of_cards


def draw_deck_overveiw(deck):

    #----------- Functions -------------------

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


    Delete_deck_btn = Button(deck_options,
                    text="Delete Deck",
                    bg="white",
                    relief="flat",
                    command=lambda: Delete_Deck(deck),
                    font=(12))

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
        

    Delete_deck_btn.pack()
    
    

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
            brand_new_cards,cards_to_review, queue_of_cards = what_cards_need_to_be_reviewed(self.deck)
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

        #---------- Load elements ----------------

        front_field = Message(mainwindow, 
              text=self.front, 
              font=(100), 
              background="white")
        
        Flip_btn = Button(mainwindow,
                text="Flip!!!", 
                command=self.draw_back)
        
        #---------- Draw elements ----------------
        front_field.place(x=100, y=100)
        Flip_btn.place(x=300, y=550)

    def draw_back(self):
        clear_main_frame()

        #---------- Load elements ----------------

        back_field = Message(mainwindow,
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

        # ------------------ TEMP ------------------
        card_schedule_data = Data.get_file_data("schedule")[str(self.card)]

        Interval_ = card_schedule_data["Interval"]
        
        current_interval = Label(mainwindow,
                                 text=Interval_)

        current_interval.place(x=300,y=500)
        # ------------------ TEMP ------------------



                                 
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
        Lapses = card_schedule_data["Lapses"]

        # Ease is the difficulty of the card
        # Interval is days since last review
        # Repeats is the total amount of times the card has been seen
        

        if rating == 0:
            Interval = 0
            Ease = max(1.3, Ease - 0.2)

        if rating == 1:
            # learning steps 
            if Repeats == 0:
                Interval = 1
            elif Repeats == 1:
                Interval = 3
            # difficulty is then based on ease
            else:
                Interval = round(Interval * Ease)

            Ease += 0.05
            
            # calculate the date at which the card should be reviewed next 

        Leech_Point = 8

        if Lapses >= Leech_Point:
            LeechState = True
        else:
            LeechState = False

        New_Due = datetime.date.today() + datetime.timedelta(days=Interval)

        New_Due = str(New_Due)
        
        New_Repeats = Repeats + 1
        
        new_schedule_data = {
            "Due":New_Due,
            "Interval":Interval,
            "Ease":Ease,
            "Repeats":New_Repeats,
            "Lapses":Lapses,
            "Leech":LeechState
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
