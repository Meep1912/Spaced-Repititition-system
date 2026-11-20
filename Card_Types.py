import Data
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk

def Card_Types_View(mainwindow):
    window = Toplevel(mainwindow)
    window.title("Card Types")
    window.geometry("700x420")

    style = ttk.Style()
    bg = style.lookup("Body.TEntry", "fieldbackground")
    fg = style.lookup("Body.TEntry", "foreground")

    global front_entry, back_entry

    # ---------------- misc ----------------

    def cards_using(card_type):
        return [cid for cid, c in Data.get_file_data("card_data").items()
                if c.get("Card_Type") == card_type]

    def selected_type():
        sel = types_tree.selection()
        if not sel:
            return None
        return types_tree.item(sel[0], "values")[0]

    def refresh_types():
        types_tree.delete(*types_tree.get_children())
        for name in Data.get_file_data("card_types"):
            types_tree.insert("", "end", values=(name,))

    def clear_panel():
        for child in panel.winfo_children():
            child.destroy()

    # ---------------- left side ----------------
    left = ttk.Frame(window, style="Frame.TFrame")
    left.pack(side="left", anchor="n", padx=5, pady=5)

    types_tree = ttk.Treeview(left, selectmode="browse", style="Body.Treeview",
                              columns=("name",), show="headings")
    types_tree.column("name", width=150)
    types_tree.heading("name", text="Card type")
    types_tree.pack()

    # add functions

    def flash(btn, text, original):
        btn.config(text=text)
        window.after(800, lambda: btn.config(text=original))

    def add_type():
        new_type_string = new_type_entry.get().strip()
        if new_type_string == "":
            flash(add_type_btn, "Empty", "Add")
            return
        if new_type_string in Data.get_file_data("card_types"):
            flash(add_type_btn, "Exists", "Add")
            return
        Data.save_to_file("card_types", {new_type_string: {}})
        new_type_entry.delete(0, "end")
        refresh_types()

    
    # add entry and button
    add_row = ttk.Frame(left, style="Frame.TFrame") # frame to hold add buttons
     
    new_type_entry = ttk.Entry(add_row, style="Body.TEntry", width=14) # input for new name
    # button to confirm add
    add_type_btn = ttk.Button(add_row, text="Add", style="Body.TButton",command= lambda: add_type())

    add_row.pack(pady=(8, 2), fill="x")
    new_type_entry.pack(side="left", padx=2)
    add_type_btn.pack(side="left", padx=2)

    # rename / remove functions
    def rename_type():

        old = selected_type()

        if old is None:
            return
        new = simpledialog.askstring("Rename card type", "New name:",
                                     initialvalue=old, parent=window)
        if new is None: # if field is empty
            return     # cancel
        new = new.strip() 
        if new == "" or new == old: # if new is empty once stripped or same as the old one
            return # cancel
        if new in Data.get_file_data("card_types"): # if the name already exists
            messagebox.showerror("Rename", (new+"already exists."), parent=window)
            return

        card_types = Data.get_file_data("card_types")
        renamed = {}
        for key, value in card_types.items():
            if key == old:
                renamed[new] = value
            else:
                renamed[key] = value
        Data.save_whole_dict("card_types", renamed)

        users = cards_using(old)

        if users:
            all_cards = Data.get_file_data("card_data")

            updated_cards = {}
            for card_id, card in all_cards.items():
                if card_id in users:
                    new_card = dict(card)         
                    new_card["Card_Type"] = new
                    updated_cards[card_id] = new_card
                else:
                    updated_cards[card_id] = card

            Data.save_whole_dict("card_data", updated_cards)

        clear_panel()
        refresh_types()

    def remove_type():
        name = selected_type()
        if name is None:
            return
        in_use = cards_using(name)
        if in_use:
            messagebox.showerror(
                "Can't remove",
                f'{len(in_use)} card(s) use "{name}". Delete or change them first.',
                parent=window)
            return
        if not messagebox.askokcancel("Remove card type",
                                      f'Remove "{name}" and its fields?',
                                      icon="warning", parent=window):
            return
        Data.delete_in_file("card_types", name)
        clear_panel()
        refresh_types()

    btn_row = ttk.Frame(left, style="Frame.TFrame")

    btn_row.pack(pady=5)

    # rename / remove buttons

    ttk.Button(btn_row, text="Rename", style="Body.TButton",
               command=rename_type).pack(side="left", padx=2)
    
    ttk.Button(btn_row, text="Remove", style="Body.TButton",
               command=remove_type).pack(side="left", padx=2)
    

    # ---------------- right: fields panel ----------------
    panel = ttk.Frame(window, style="Frame.TFrame")
    panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)


    def show_fields():
        clear_panel()
        card_type_fields = Data.get_file_data("card_types")[card_type_selected]
        ttk.Label(panel, text="Fields of " + card_type_selected, style="Heading.TLabel").pack()
        fields_tree = ttk.Treeview(panel, selectmode="browse", style="Body.Treeview",
                                   columns=("field", "type"), show="headings", height=8)
        fields_tree.heading("field", text="field")
        fields_tree.heading("type", text="type")
        fields_tree.column("field", width=90)
        fields_tree.column("type", width=90)
        fields_tree.pack(side="left", anchor="n", padx=5)

        boxes = ttk.Frame(panel, style="Frame.TFrame")

        frnt_lbl = ttk.Label(boxes, text="Front of Card", style="Body.TLabel")

        front_entry = Text(boxes, height=4, width=20, background=bg, foreground=fg,
                           insertbackground=fg, font=("Segoe UI", 12))

        bck_lbl = ttk.Label(boxes, text="Back of Card", style="Body.TLabel")
        back_entry = Text(boxes, height=4, width=20, background=bg, foreground=fg,
                          insertbackground=fg, font=("Segoe UI", 12))

        save_button = ttk.Button(panel, text="Save", style="Body.TButton",
                                 command=lambda: save_field_configuration(save_button))


        boxes.pack(side="left", anchor="n")
        save_button.pack()
        frnt_lbl.pack(anchor="w")
        front_entry.pack()
        bck_lbl.pack(anchor="w")
        back_entry.pack()

        front_fields, back_fields = [], []
        for field, (side, field_type) in card_type_fields.items():
            fields_tree.insert("", "end", values=(field, field_type))
            if side in ("Front", "Both"):
                front_fields.append(field)
            if side in ("Back", "Both"):
                back_fields.append(field)
        front_entry.insert("1.0", "\n".join(front_fields))
        back_entry.insert("1.0", "\n".join(back_fields))

        field_row = ttk.Frame(boxes, style="Frame.TFrame")
        field_row.pack(pady=10, anchor="w")
        new_name = ttk.Entry(field_row, style="Body.TEntry", width=12)
        new_type = ttk.Combobox(field_row, style="Body.TCombobox", width=8,
                                values=["Text", "Image"], state="readonly")

        add_btn = ttk.Button(field_row, text="Add field", style="Body.TButton", command= lambda: add_field())
        new_name.pack(side="left", padx=2)
        new_type.pack(side="left", padx=2)
        add_btn.pack(side="left", padx=2)

        def add_field():
            name = new_name.get().strip()
            media_type = new_type.get().strip()
            if not name or not media_type:
                flash(add_btn, "Empty fields", "Add field")
                return
            existing = Data.get_file_data("card_types")[card_type_selected]
            if name in existing:
                flash(add_btn, "Name exists", "Add field")
                return
            Data.save_to_file("card_types",
                              {card_type_selected: {**existing, name: ["Front", media_type]}})
            fields_tree.insert("", "end", values=(name, media_type))
            front_entry.insert("end", ("\n" if front_entry.get("1.0", "end-1c") else "") + name)
            new_name.delete(0, "end")
            flash(add_btn, "Added", "Add field")

        # SAVE BUTTON
        def save_field_configuration(btn):

            fnt_entry_data = front_entry.get("1.0",END).split("\n")
            bck_entry_data = back_entry.get("1.0",END).split("\n")

            the_card_types_fields = Data.get_file_data("card_types")[card_type_selected]

            new_card_type_field_layout = {}

            for field in fnt_entry_data:
                if field in the_card_types_fields:
                    new_data = {field: ["Front", the_card_types_fields[field][1]]}
                    new_card_type_field_layout.update(new_data)

            for field in bck_entry_data:
                if field in the_card_types_fields:
                    new_data = {field: ["Back", the_card_types_fields[field][1]]}
                    new_card_type_field_layout.update(new_data)


            # replace card type in file with new_card_type_field_layout

            Data.delete_in_file("card_types", card_type_selected)

            # write cashe into file

            Data.save_to_file("card_types", {card_type_selected: new_card_type_field_layout})


        return front_entry, back_entry


    def on_type_select(event):
        global front_entry, back_entry, card_type_selected
        card_type_selected = selected_type()
        if card_type_selected is not None:
            front_field, back_field = show_fields()


    types_tree.bind("<<TreeviewSelect>>", on_type_select)
    refresh_types()


