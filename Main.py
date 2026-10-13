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
mainwindow.title("S.R.S")
mainwindow.geometry("600x600")
mainwindow.config(bg="white")


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

    decks.add_command(label="Decks",command=None)

    # --- Add --- 

    add  = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Add",menu=add)

    add.add_command(label="Add",command=lambda: Add_Card_View.open_add_card_menu())

    # ---View --- 

    view = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View",menu=view)

    view.add_command(label="View",command=lambda: Card_View.open_card_view_menu())

    mainwindow.config(menu=menubar)
    
decks_window_buttons()
mainwindow.mainloop()