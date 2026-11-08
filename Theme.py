from tkinter import ttk

theme = {
    "Brilliant_White": {

        # Main window
        "Background": "#FFFFFF",
        "Foreground": "#222222",

        # Standard widget
        "WidgetBackground": "#F5F5F5",
        "WidgetForeground": "#222222",
        "Border": "#DDDDDD",

        # Interactive widget
        "Accent": "#0078D4",
        "AccentForeground": "#FFFFFF",
        "Hover": "#E5F1FB",
        "Pressed": "#D0E5F5",

        # Font
        "Font": ("Arial", 10),

        # Frame background
        "FrameBackground": "#FFFFFF",

        # Misc
        "Disabled": "#999999",
        "Selection": "#0078D4",
        "SelectionForeground": "#FFFFFF"
    }}


def configure_styles(selected_theme):
    
    style = ttk.Style()

    style.theme_use("clam")
    
    # Frames
    style.configure(
        "Frame.TFrame",
        background=selected_theme["FrameBackground"],
        borderwidth=0)

    # Labels
    style.configure(
        "Body.TLabel",
        background=selected_theme["Background"],
        foreground=selected_theme["Foreground"],
        font=selected_theme["Font"])

    # Buttons
    style.configure(
        "Body.TButton",
        background=selected_theme["WidgetBackground"],
        foreground=selected_theme["WidgetForeground"],
        font=selected_theme["Font"],
        padding=5,
        borderwidth=1,
        relief="flat")

    style.map(
        "Body.TButton",
        background=[
            ("pressed", selected_theme["Pressed"]),
            ("active", selected_theme["Hover"])],
        foreground=[
            ("disabled", selected_theme["Disabled"])])

    # Primary Buttons
    style.configure(
        "Primary.TButton",
        background=selected_theme["Accent"],
        foreground=selected_theme["AccentForeground"],
        font=selected_theme["Font"],
        padding=5,
        borderwidth=0)

    style.map(
        "Primary.TButton",
        background=[
            ("pressed", selected_theme["Pressed"]),
            ("active", selected_theme["Hover"])])

    # Entries
    style.configure(
        "Body.TEntry",
        fieldbackground=selected_theme["WidgetBackground"],
        foreground=selected_theme["WidgetForeground"],
        insertcolor=selected_theme["WidgetForeground"],
        bordercolor=selected_theme["Border"],
        lightcolor=selected_theme["Border"],
        darkcolor=selected_theme["Border"],
        padding=5)

    # Comboboxes
    style.configure(
        "Body.TCombobox",
        fieldbackground=selected_theme["WidgetBackground"],
        background=selected_theme["WidgetBackground"],
        foreground=selected_theme["WidgetForeground"],
        arrowcolor=selected_theme["Foreground"],
        padding=5)

    style.map(
        "Body.TCombobox",
        fieldbackground=[
            ("readonly", selected_theme["WidgetBackground"])],
        foreground=[
            ("readonly", selected_theme["WidgetForeground"])],
        selectbackground=[
            ("readonly", selected_theme["Selection"])],
        selectforeground=[
            ("readonly", selected_theme["SelectionForeground"])])

    # Checkbuttons
    style.configure(
        "Body.TCheckbutton",
        background=selected_theme["Background"],
        foreground=selected_theme["Foreground"],
        font=selected_theme["Font"])

    style.map(
        "Body.TCheckbutton",
        background=[
            ("active", selected_theme["Background"])],
        foreground=[
            ("disabled", selected_theme["Disabled"])])

    # Spinboxes
    style.configure(
        "Body.TSpinbox",
        fieldbackground=selected_theme["WidgetBackground"],
        foreground=selected_theme["WidgetForeground"],
        arrowcolor=selected_theme["Foreground"],
        padding=5)




