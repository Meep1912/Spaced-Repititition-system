from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from Theme import theme
import Data
# main window settings 


def draw_elements(User_Settings_frame):
    
    # Available fonts
    available_fonts = ["Arial"]

    # get existing data

    user_settings_data = Data.get_file_data("user_settings")

    







    fields = {}

    font_type_lbl = ttk.Label(
        User_Settings_frame,
        text="Font Type",
        style="Body.TLabel" )
    font_type_lbl.pack(anchor=W)

    font_type_var = StringVar()
    font_type_entry = ttk.Combobox(
        User_Settings_frame,
        values=available_fonts,
        style="Body.TCombobox")
    font_type_entry.pack(anchor=W)

    fields["font_type"] = font_type_entry



    # Themes
    available_themes = []    
    for value in theme.keys():
        available_themes.append(value)


    themes_lbl = ttk.Label(
        User_Settings_frame,
        text="Themes",
        style="Body.TLabel")
    themes_lbl.pack(anchor=W)

    themes_entry_var = StringVar()
    themes_entry = ttk.Combobox(
        User_Settings_frame,
        values=available_themes,
        style="Body.TCombobox",
        textvariable=themes_entry_var)
    themes_entry.pack(anchor=W)

    fields["theme"] = themes_entry_var





    # Leech point
    leechpoint_lbl = ttk.Label(
        User_Settings_frame,
        text="Leech Point",
        style="Body.TLabel")
    leechpoint_lbl.pack(anchor=W)

    leechpoint_var = IntVar()
    leechpoint_entry = ttk.Spinbox(
        User_Settings_frame,
        from_=0,
        to=50,
        style="Body.TSpinbox",
        textvariable=leechpoint_var
        )
    leechpoint_entry.pack(anchor=W)

    fields["leechpoint"] = leechpoint_var




    # Suspend leeches
    suspend_leeches_lbl = ttk.Label(
        User_Settings_frame,
        text="Suspend cards when they pass leechpoint",
        style="Body.TLabel")
    suspend_leeches_lbl.pack(anchor=W)

    suspend_leeches_var = IntVar()
    suspend_leeches_entry = ttk.Checkbutton(
        User_Settings_frame,
        style="Body.TCheckbutton",
        variable=suspend_leeches_var)
    suspend_leeches_entry.pack(anchor=W)

    fields["suspend_leech"] = suspend_leeches_var





    # Learning steps
    available_learning_steps = ["1D, 3D", "2D, 3D", "1D,2D,3D,4D", "1D,1D,2D", "1D,2D,3D"]

    learning_steps_lbl = ttk.Label(
        User_Settings_frame,
        text="Learning Steps",
        style="Body.TLabel")
    learning_steps_lbl.pack(anchor=W)

    learning_steps_var = StringVar()
    learning_steps_entry = ttk.Combobox(
        User_Settings_frame,
        values=available_learning_steps,
        style="Body.TCombobox",
        textvariable=learning_steps_var)
    learning_steps_entry.pack(anchor=W)

    fields["learning_steps"] = learning_steps_var





    # Hide rate buttons
    hide_bar_in_review_lbl = ttk.Label(
        User_Settings_frame,
        text="Hide Buttons in review (use keybinds)",
        style="Body.TLabel")
    hide_bar_in_review_lbl.pack(anchor=W)

    hide_bar_in_review_var = IntVar()
    hide_bar_in_review_entry = ttk.Checkbutton(
        User_Settings_frame,
        style="Body.TCheckbutton",
        variable=hide_bar_in_review_var)
    hide_bar_in_review_entry.pack(anchor=W)

    fields["no_review_buttons"] = hide_bar_in_review_var






    # Hide interval
    hide_interval_in_review_lbl = ttk.Label(
        User_Settings_frame,
        text="Hide interval in review",
        style="Body.TLabel")
    hide_interval_in_review_lbl.pack(anchor=W)

    hide_interval_in_review_var = IntVar()
    hide_interval_in_review_entry = ttk.Checkbutton(
        User_Settings_frame,
        style="Body.TCheckbutton",
        variable=hide_bar_in_review_var)
    hide_interval_in_review_entry.pack(anchor=W)

    fields["no_interval_in_review"] = hide_interval_in_review_var


    done_btn = ttk.Button(
        User_Settings_frame,
        text="DONE !",
        style="Body.TButton",
        command= lambda: done(fields)
    )
    done_btn.pack(anchor=W)



def done(fields):

    def get_values(Entries):
        values = Entries.copy()
        for Entry in Entries.keys():
            values[Entry] = Entries[Entry].get()          
        return(values)
    
    values = get_values(fields)

    Data.save_whole_dict("user_settings",values)







def Draw_User_Settings_View(mainwindow, selected_theme):

    # window config
    settings_root = ctk.CTkToplevel(mainwindow)
    settings_root.title("Settings")
    settings_root.config(background=selected_theme["Background"])
    height_ = 500
    width_ = 600
    settings_root.geometry(str(height_) + "x" + str(width_))
    User_Settings_frame = ctk.CTkScrollableFrame(settings_root, width=width_-50,height=height_-50, fg_color=selected_theme["Background"])
    User_Settings_frame.pack(fill="both", expand=True, padx=10,pady=10)


    # focus window
    settings_root.after(100, settings_root.focus)

    draw_elements(User_Settings_frame)
