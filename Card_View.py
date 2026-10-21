from tkinter import *
import Data

# ------------- Main Window configiration -------------------

def open_card_view_menu():
    card_view = Toplevel()
    card_view.title("Card View")
    card_view.geometry("600x450")
    draw_elements(card_view)


# --------------------------------------------------------------------------------
# ----------------------------- L O G I C ----------------------------------------
# --------------------------------------------------------------------------------

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

def format(values):
    string = ""
    for word in values:
        if len(word) > 12:
            word = word[:12] + ". . ."

        spaces = 22 - len(word)

        string = string + (word+(spaces*" "))

    return string
        
def decode_filters(entry):
        filters = {
            "Deck":None,
            "Card_Type":None,
            "Front":None,
            "Back":None,
            "Due":None,
            "Leech":None,
            "Ease":None,
            "Interval":None,
            "Repeats": None,
            "Lapses":None}

        # Entry should be in the form Deck:Deck1, Card_Type:Card1, Front:hello
        if entry == "":
            pass
        else:
            for item in entry.split(","):
                key, value = item.strip().split(":",1)
                key = key.strip()
                value = value.strip()
                filters[key] = value
    
        if filters["Interval"] is not None:
            filters["Interval"] = int(filters["Interval"])

        elif filters["Ease"] is not None:
            filters["Ease"] = float(filters["Ease"])

        elif filters["Repeats"] is not None:
            filters["Repeats"] = int(filters["Repeats"])

        elif filters["Lapses"] is not None:
            filters["Lapses"] = int(filters["Lapses"])

        elif filters["Leech"] is not None:
            filters["Leech"] = bool(filters["Leech"])

        return filters
# --------------------------------------------------------------------------------
# ----------------------------- D R A W I N G ------------------------------------
# --------------------------------------------------------------------------------



# main window settings 
def open_card_view_menu():
    card_view = Toplevel()
    card_view.title("Card View")
    card_view.geometry("600x450")
    draw_elements(card_view)

def draw_elements(card_view):

    def draw_main_area():

        def draw_filtered_cards(filters):

            listbox = Listbox(main_area,
                                height=20,
                                width=60,
                                bg="white",
                                activestyle="dotbox",
                                yscrollcommand=scroll_bar.set)

            listbox.delete(0, END)
            i = 0
            data = get_data()

            for card_id, card in data.items():

                # all checks if the card satisfies every filter
                matches = all(card[field] == value
                            
                            for field, value in filters.items()
                            # skips any filters that isnt selected (none)
                            if value is not None)
                if matches: # if the card satisfies every filters, adds the card
                    values = [
                        card["Deck"],
                        card["Front"],
                        card["Back"],
                        card["Due"]]
                    listbox.insert(i,format(values))
                    i += 1
            listbox.place(x=100,y=100)

        main_area = Frame(card_view)   
        Search_Bar = Entry(main_area,width=50)
        Submit_Btn = Button(main_area,width=10,command=lambda:draw_filtered_cards(decode_filters(Search_Bar.get())),text="Search" )
        scroll_bar = Scrollbar(main_area)
    
        Deck_Lbl = Label(main_area,text="Deck").place(x=100,y=60)
        Front_Lbl = Label(main_area,text="Front").place(x=180,y=60)
        Back_Lbl = Label(main_area,text="Back").place(x=270,y=60)
        Due_Lbl = Label(main_area, text="Due").place(x=360,y=60)

        main_area.pack(side="right",fill="both",expand=True)

        Search_Bar.place(x=100,y=25)
        Submit_Btn.place(x=350,y=25)
        scroll_bar.pack(side=RIGHT,fill=Y)

        draw_filtered_cards(decode_filters(Search_Bar.get()))  
        return Search_Bar
        
    def draw_sidebar(Search_bar):

        sidebar = Frame(card_view)
        sidebar.pack(side="left",fill=Y)

        label = Label(sidebar,text="Filters")
        label.pack()

        def deck_panel():
            deck_btn = Button(sidebar,text="Decks", command=lambda: toggle_decks())
            deck_btn.pack(fill="x")
            deck_filters = Frame(sidebar)

            decks = Data.get_file_data("decks")
            for deck in decks:
                Button(deck_filters,
                    text=deck, 
                    command =lambda d=deck: 
                    (Search_bar.delete(0,END), 
                        Search_bar.insert(0,"Deck:"+d))).pack(fill="x",padx=10,pady=2)

            def toggle_decks():
                if deck_filters.winfo_manager():
                    deck_filters.pack_forget()
                    deck_btn.config(text="Decks . . .")
                else:
                    deck_filters.pack(fill="x")
                    deck_btn.config(text="Decks")

        deck_panel()


    Search_bar = draw_main_area()
    draw_sidebar(Search_bar)
