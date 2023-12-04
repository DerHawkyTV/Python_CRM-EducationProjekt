import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('CRM-System')

        self.db = Database()

        # Eingabefelder erstellen
        self.label_name = tk.Label(root, text='Name:')
        self.label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_email = tk.Label(root, text='Email:')
        self.label_email.grid(row=1, column=0, padx=10, pady=10)
        self.entry_email = tk.Entry(root)
        self.entry_email.grid(row=1, column=1, padx=10, pady=10)

        self.label_phone = tk.Label(root, text='Telefon:')
        self.label_phone.grid(row=2, column=0, padx=10, pady=10)
        self.entry_phone = tk.Entry(root)
        self.entry_phone.grid(row=2, column=1, padx=10, pady=10)

        self.label_address = tk.Label(root, text='Adresse:')
        self.label_address.grid(row=3, column=0, padx=10, pady=10)
        self.entry_address = tk.Entry(root)
        self.entry_address.grid(row=3, column=1, padx=10, pady=10)

        self.label_birthdate = tk.Label(root, text='Geburtsdatum:')
        self.label_birthdate.grid(row=4, column=0, padx=10, pady=10)
        self.entry_birthdate = tk.Entry(root)
        self.entry_birthdate.grid(row=4, column=1, padx=10, pady=10)

        self.label_notes = tk.Label(root, text='Anmerkungen:')
        self.label_notes.grid(row=5, column=0, padx=10, pady=10)
        self.entry_notes = tk.Entry(root)
        self.entry_notes.grid(row=5, column=1, padx=10, pady=10)

        # Buttons erstellen
        self.button_add = tk.Button(root, text='Kunden hinzufügen', command=self.add_customer)
        self.button_add.grid(row=6, column=0, columnspan=2, pady=10)

        self.button_edit = tk.Button(root, text='Kunden bearbeiten', command=self.edit_customer)
        self.button_edit.grid(row=7, column=0, columnspan=2, pady=10)

        self.button_print = tk.Button(root, text='Kunden drucken', command=self.print_customer)
        self.button_print.grid(row=8, column=0, columnspan=2, pady=10)

        # Treeview für die Anzeige der Kunden
        columns = ('ID', 'Name', 'Email', 'Telefon', 'Adresse', 'Geburtsdatum', 'Anmerkungen')
        self.tree = ttk.Treeview(root, columns=columns, show='headings')

        # Setze die Überschriften
        for col in columns:
            self.tree.heading(col, text=col)

        # Fülle die Kundenanzeige
        self.display_customers()

        self.tree.grid(row=9, column=0, columnspan=2, pady=10)

        # Event, um auf Doppelklick in der Treeview zu reagieren
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def add_customer(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        birthdate = self.entry_birthdate.get()
        notes = self.entry_notes.get()

        if name and email and phone:
            self.db.add_customer(name, email, phone, address, birthdate, notes)
            messagebox.showinfo('Erfolg', 'Kunde hinzugefügt!')
            self.clear_entries()
            self.display_customers()
        else:
            messagebox.showerror('Fehler', 'Bitte füllen Sie alle Felder aus.')

    def edit_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Fehler', 'Bitte wählen Sie einen Kunden aus, den Sie bearbeiten möchten.')
            return

        customer_id = self.tree.item(selected_item, 'values')[0]
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        birthdate = self.entry_birthdate.get()
        notes = self.entry_notes.get()

        if name and email and phone:
            self.db.edit_customer(customer_id, name, email, phone, address, birthdate, notes)
            messagebox.showinfo('Erfolg', 'Kunde bearbeitet!')
            self.clear_entries()
            self.display_customers()
        else:
            messagebox.showerror('Fehler', 'Bitte füllen Sie alle Felder aus.')

    def print_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Fehler', 'Bitte wählen Sie einen Kunden aus, den Sie drucken möchten.')
            return

        customer_info = self.tree.item(selected_item, 'values')
        customer_details = f'''
        Kundeninformationen:
        ID: {customer_info[0]}
        Name: {customer_info[1]}
        Email: {customer_info[2]}
        Telefon: {customer_info[3]}
        Adresse: {customer_info[4]}
        Geburtsdatum: {customer_info[5]}
        Anmerkungen: {customer_info[6]}
        '''

        # Druckdialog anzeigen
        print_text = simpledialog.askstring("Drucken", "Kundeninformationen drucken?", initialvalue=customer_details)
        if print_text:
            # Hier könnten Sie den Text drucken oder speichern, je nach Ihren Anforderungen
            print("Drucken:", print_text)

    def display_customers(self):
        rows = self.db.get_all_customers()

        # Lösche vorherige Einträge in der Anzeige
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Füge Kunden zur Anzeige hinzu
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def clear_entries(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.entry_address.delete(0, 'end')
        self.entry_birthdate.delete(0, 'end')
        self.entry_notes.delete(0, 'end')

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.populate_entries(values)

    def populate_entries(self, values):
        self.clear_entries()
        if values:
            self.entry_name.insert(0, values[1])
            self.entry_email.insert(0, values[2])
            self.entry_phone.insert(0, values[3])
            self.entry_address.insert(0, values[4])
            self.entry_birthdate.insert(0, values[5])
            self.entry_notes.insert(0, values[6])

    def close_db_connection(self):
        self.db.close_connection()
