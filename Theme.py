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
        "SelectionForeground": "#FFFFFF"},

        
    "Nord": {
        # Main window
        "Background": "#2E3440",     
        "Foreground": "#ECEFF4",       
    
        # Standard widget
        "WidgetBackground": "#3B4252",
        "WidgetForeground": "#E5E9F0",
        "Border": "#434C5E",
    
        # Interactive widget
        "Accent": "#88C0D0",           
        "AccentForeground": "#2E3440",
        "Hover": "#5E81AC",
        "Pressed": "#81A1C1",
    
        # Font
        "Font": ("Arial", 10),
    
        # Frame background
        "FrameBackground": "#2E3440",
    
        # Misc
        "Disabled": "#616E88",
        "Selection": "#88C0D0",
        "SelectionForeground": "#2E3440"},

    "Dracula": {
        "Background": "#282A36",
        "Foreground": "#F8F8F2",
    
        "WidgetBackground": "#44475A",
        "WidgetForeground": "#F8F8F2",
        "Border": "#6272A4",
    
        "Accent": "#BD93F9",
        "AccentForeground": "#282A36",
        "Hover": "#50FA7B",
        "Pressed": "#6272A4",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#282A36",
    
        "Disabled": "#6272A4",
        "Selection": "#44475A",
        "SelectionForeground": "#F8F8F2"},
    
    "Absolute_Black": {
        "Background": "#000000",
        "Foreground": "#FFFFFF",
    
        "WidgetBackground": "#0A0A0A",
        "WidgetForeground": "#FFFFFF",
        "Border": "#1A1A1A",
    
        "Accent": "#00AEEF",
        "AccentForeground": "#FFFFFF",
        "Hover": "#1E1E1E",
        "Pressed": "#333333",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#000000",
    
        "Disabled": "#666666",
        "Selection": "#00AEEF",
        "SelectionForeground": "#FFFFFF"},
    
    "Wheatgrass": {
        "Background": "#F8F7EE",
        "Foreground": "#3C3C2E",
    
        "WidgetBackground": "#EFEBD5",
        "WidgetForeground": "#3C3C2E",
        "Border": "#B8C48A",
    
        "Accent": "#7FA33E",
        "AccentForeground": "#FFFFFF",
        "Hover": "#DDE8BF",
        "Pressed": "#C7D79F",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#F8F7EE",
    
        "Disabled": "#888866",
        "Selection": "#7FA33E",
        "SelectionForeground": "#FFFFFF"},
    
    "Winter": {
        "Background": "#EAF3FA",
        "Foreground": "#1F2D3D",
    
        "WidgetBackground": "#DCEAF5",
        "WidgetForeground": "#1F2D3D",
        "Border": "#AFC7D9",
    
        "Accent": "#5E81AC",
        "AccentForeground": "#FFFFFF",
        "Hover": "#C9DDEE",
        "Pressed": "#B1CEE3",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#EAF3FA",
    
        "Disabled": "#7A8794",
        "Selection": "#5E81AC",
        "SelectionForeground": "#FFFFFF"},
    
    "Org_Mode": {
        "Background": "#FDF6E3",
        "Foreground": "#657B83",
    
        "WidgetBackground": "#EEE8D5",
        "WidgetForeground": "#586E75",
        "Border": "#93A1A1",
    
        "Accent": "#268BD2",
        "AccentForeground": "#FFFFFF",
        "Hover": "#DCECF8",
        "Pressed": "#BFD7EA",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#FDF6E3",
    
        "Disabled": "#93A1A1",
        "Selection": "#268BD2",
        "SelectionForeground": "#FFFFFF"},
    
    "NotMuch_Dark": {
        "Background": "#111111",
        "Foreground": "#E8E8E8",
    
        "WidgetBackground": "#1B1B1B",
        "WidgetForeground": "#E8E8E8",
        "Border": "#333333",
    
        "Accent": "#729FCF",
        "AccentForeground": "#FFFFFF",
        "Hover": "#222222",
        "Pressed": "#2C2C2C",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#111111",
    
        "Disabled": "#666666",
        "Selection": "#729FCF",
        "SelectionForeground": "#FFFFFF"},
    
    "NotMuch_Light": {
        "Background": "#FFFFFF",
        "Foreground": "#222222",
    
        "WidgetBackground": "#F6F6F6",
        "WidgetForeground": "#222222",
        "Border": "#D8D8D8",
    
        "Accent": "#3465A4",
        "AccentForeground": "#FFFFFF",
        "Hover": "#EEF4FB",
        "Pressed": "#D9E7F6",
    
        "Font": ("Arial", 10),
    
        "FrameBackground": "#FFFFFF",
    
        "Disabled": "#888888",
        "Selection": "#3465A4",
        "SelectionForeground": "#FFFFFF"}}


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




