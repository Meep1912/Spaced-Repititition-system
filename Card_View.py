from tkinter import *
import Data




# main window settings 
def open_card_view_menu():
    card_view = Toplevel()
    card_view.title("Card View")
    card_view.geometry("600x400")
    draw_elements(card_view)

def get_data():
    card_data = Data.get_file_data("card_data")
    schedule = Data.get_file_data("schedule")
    decks = Data.get_file_data("decks")

    # merged dictionaryies = |


    combined =  {k: card_data[k] | schedule[k] for k in card_data}

    for deck in decks:
        for card in decks[deck]:
            combined[card]["Deck"] = deck

    return combined

    
def draw_elements(card_view):

    Search_Bar = Entry(card_view,width=50)
    Search_Bar.place(x=100,y=25)

    data = get_data()

    offset = 0

    # Deck Label
    Deck_Lbl = Label(card_view,text="Deck").place(x=100,y=60)
    # Front Label
    Front_Lbl = Label(card_view,text="Front").place(x=160,y=60)
    # Due Label
    Due_Lbl = Label(card_view, text="Due").place(x=320,y=60)


    
    for card_id, card in data.items():

        Card_Deck_Lbl = Label(card_view,
                       text=card["Deck"]).place(x=100,y=offset+100)
        Card_Front_Lbl = Label(card_view,
                       text=card["Front"]).place(x=160,y=offset+100)
        Card_Due_Lbl = Label(card_view,
                        text=card["Due"]).place(x=320,y=offset+100)
        
        offset += 20

    pass