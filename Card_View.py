from tkinter import *




# main window settings 
def open_card_view_menu():
    card_view = Toplevel()
    card_view.title("Project")
    card_view.geometry("600x400")
    draw_elements(card_view)

def draw_elements(card_view):
    Search_Bar = Entry(card_view,
                       )
    pass