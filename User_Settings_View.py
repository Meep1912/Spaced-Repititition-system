from tkinter import *
from tkinter import ttk
from Theme import theme
import Data
# main window settings 


def draw_elements(User_Settings_frame):
    
    # Available fonts
    available_fonts = ["Arial"]

    







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

    fields["Font"] = font_type_entry



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

    fields["Theme"] = themes_entry_var





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

    fields["Leech_Point"] = leechpoint_var




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

    fields["Suspend_Leech"] = suspend_leeches_var





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

    fields["Learning_Steps"] = learning_steps_var





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

    fields["No_Review_Buttons"] = hide_bar_in_review_var





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
        variable=hide_interval_in_review_var)
    hide_interval_in_review_entry.pack(anchor=W)

    fields["No_Interval_In_Review"] = hide_interval_in_review_var


    done_btn = ttk.Button(
        User_Settings_frame,
        text="DONE !",
        style="Body.TButton",
        command= lambda: done(fields)
    )
    done_btn.pack(anchor=W)


    user_settings_data = Data.get_file_data("user_settings")

    try:
        font_type_entry.insert(0,user_settings_data["Font"])
        themes_entry_var.set(user_settings_data["Theme"])
        leechpoint_var.set(str(user_settings_data["Leech_point"]))
        learning_steps_var.set(user_settings_data["Learning_Steps"])
        hide_bar_in_review_var.set(user_settings_data["No_Review_Buttons"])
        hide_interval_in_review_var.set(user_settings_data["No_Interval_In_Review"])
    except:
        font_type_entry.insert(0,"Arial")
        themes_entry_var.set("Brilliant_White")
        leechpoint_var.set("8")
        learning_steps_var.set("1D, 3D")
        hide_bar_in_review_var.set(0)
        hide_interval_in_review_var.set(0)

    learning_steps_entry.config(state="readonly")
    themes_entry.config(state="readonly")
    font_type_entry.config(state="readonly")




def done(fields):

    def get_values(Entries):
        values = Entries.copy()
        for Entry in Entries.keys():
            if Entry == "Font":
                values[Entry] = (Entries[Entry].get(), 10)
            else:
             values[Entry] = Entries[Entry].get()          
        return(values)
    
    values = get_values(fields)

    Data.save_whole_dict("user_settings",values)







def Draw_User_Settings_View(mainwindow, selected_theme):

    # window config
    settings_frame = Toplevel(mainwindow)
    settings_frame.title("Settings")
    settings_frame.geometry("200x600")

    draw_elements(settings_frame)
