from tkinter import *
import Card_View 
import Add_Card_View

# button functions
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
    pass


mainwindow = Tk()
canvas = Canvas()
mainwindow.title("Project")
mainwindow.geometry("600x600")
mainwindow.config(bg="white")


def decks_window_buttons():
    home_file_button = Button(mainwindow,
                        text="file",
                        command=filebuttonpressed,
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))

    home_edit_button = Button(mainwindow,
                        text="edit",
                        command=filebuttonpressed,
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))


    home_help_button = Button(mainwindow,
                        text="help",
                        command=filebuttonpressed,
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))


    home_decks_button = Button(mainwindow,
                        text="decks",
                        command=0,
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))


    home_add_button = Button(mainwindow,
                        text="add",
                        command=lambda: Add_Card_View.open_add_card_menu(),
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))


    home_view_button = Button(mainwindow,
                        text="view",
                        command=lambda: Card_View.open_card_view_menu(),
                        underline=0,
                        bg="white",
                        relief="flat",
                        font=(12))

    home_file_button.pack(anchor="n",side="left")
    home_view_button.pack(anchor="n",side="left")
    home_edit_button.pack(anchor="n",side="left")
    home_help_button.pack(anchor="n",side="left")
    home_decks_button.pack(anchor="n",side="left")
    home_add_button.pack(anchor="n",side="left")
    
decks_window_buttons()
mainwindow.mainloop()