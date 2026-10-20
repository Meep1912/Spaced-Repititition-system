from tkinter import *
import Data




# main window settings 
def open_card_view_menu():
    card_view = Toplevel()
    card_view.title("Card View")
    card_view.geometry("600x450")
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

def sizing(string):

     X = len(string)
     if X > 12:
         return(string[:12] + ". . .")
     else:
         return(string)




def draw_elements(card_view):

    Search_Bar = Entry(card_view,width=50)
    Search_Bar.place(x=100,y=25)

    data = get_data()

    offset = 0

    scroll_bar = Scrollbar(card_view)
    scroll_bar.pack(side=RIGHT,fill=Y)

    # Deck Label
    Deck_Lbl = Label(card_view,text="Deck").place(x=100,y=60)
    # Front Label
    Front_Lbl = Label(card_view,text="Front").place(x=180,y=60)
    # Back Label
    Back_Lbl = Label(card_view,text="Back").place(x=270,y=60)
    # Due Label
    Due_Lbl = Label(card_view, text="Due").place(x=360,y=60)


    listbox = Listbox(card_view,
                    height=20,
                    width=60,
                    bg="white",
                    activestyle="dotbox",
                    yscrollcommand=scroll_bar.set)
    
    i = 0

    for card_id, card in data.items():

        deck_selected
        

        deck = sizing(card["Deck"])
        front = sizing(card["Front"])
        back = sizing(card["Back"])
        due = sizing(card["Due"])

        def spacing(string):
            spaces = 22 - len(string) 
            return spaces
        
        text = deck + " "*spacing(deck) + front + " "*spacing(front) + back + " "*spacing(back) + due + " "*spacing(due)
        
        listbox.insert(i,text)
    
        i += 1

    listbox.place(x=100,y=100)
    pass