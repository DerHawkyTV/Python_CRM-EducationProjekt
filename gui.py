import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
import matplotlib.pyplot as plt


class StatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()

        # Button zum Anzeigen von Statistiken
        self.button_show_stats = tk.Button(self, text="Statistiken anzeigen", command=self.show_statistics)
        self.button_show_stats.pack(pady=10)

    def show_statistics(self):
        # Holen Sie Ihre Daten von der Datenbank (Beispiel: Anzahl der Kunden pro Region)
        data = self.db.get_stats_by_region()

        # Erstellen Sie ein einfaches Balkendiagramm
        regions = [entry[0] for entry in data]
        counts = [entry[1] for entry in data]

        plt.bar(regions, counts)
        plt.xlabel('Regionen')
        plt.ylabel('Anzahl der Kunden')
        plt.title('Anzahl der Kunden pro Region')
        plt.show()


class EmailIntegration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = Database()

        # Eingabefeld für E-Mail-Adresse des Kunden
        self.label_email = tk.Label(self, text='E-Mail-Adresse des Kunden:')
        self.label_email.pack(pady=10)
        self.entry_customer_email = tk.Entry(self)
        self.entry_customer_email.pack(pady=10)

        # Button zum Senden der E-Mail
        self.button_send_email = tk.Button(self, text="E-Mail senden", command=self.send_email)
        self.button_send_email.pack(pady=10)

    def send_email(self):
        # Holen Sie die E-Mail-Adresse des ausgewählten Kunden
        selected_item = self.controller.tree.selection()
        if not selected_item:
            messagebox.showerror('Fehler', 'Bitte wählen Sie einen Kunden aus.')
            return

        customer_email = self.controller.tree.item(selected_item, 'values')[2]
        if not customer_email:
            messagebox.showerror('Fehler', 'Der ausgewählte Kunde hat keine E-Mail-Adresse.')
            return

        # E-Mail-Adresse des Kunden mit der Eingabeaufforderung ersetzen
        customer_email = simpledialog.askstring("E-Mail senden", "E-Mail-Adresse des Kunden:",
                                                initialvalue=customer_email)

        if customer_email:
            # Senden Sie die E-Mail
            subject = "Betreff der E-Mail"
            body = "Inhalt der E-Mail"

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = "absender@example.com"
            msg['To'] = customer_email

            try:
                # Stellen Sie eine Verbindung zum SMTP-Server her und senden Sie die E-Mail
                with smtplib.SMTP('smtp.example.com', 587) as server:
                    server.starttls()
                    server.login("benutzername", "passwort")
                    server.sendmail("absender@example.com", [customer_email], msg.as_string())

                messagebox.showinfo('Erfolg', 'E-Mail erfolgreich gesendet.')
            except Exception as e:
                messagebox.showerror('Fehler', f'Fehler beim Senden der E-Mail: {str(e)}')


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

        # Baumstruktur für Kunden anzeigen
        self.tree = ttk.Treeview(root,
                                 columns=('ID', 'Name', 'Email', 'Telefon', 'Adresse', 'Geburtsdatum', 'Anmerkungen'))
        self.tree.grid(row=0, column=2, rowspan=6, padx=10, pady=10)
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Email')
        self.tree.heading('#3', text='Telefon')
        self.tree.heading('#4', text='Adresse')
        self.tree.heading('#5', text='Geburtsdatum')
        self.tree.heading('#6', text='Anmerkungen')
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        # Kunden zur Baumstruktur hinzufügen
        self.display_customers()

        # Buttons für Aktionen
        self.button_add_customer = tk.Button(root, text='Kunde hinzufügen', command=self.add_customer)
        self.button_add_customer.grid(row=6, column=0, padx=10, pady=10)

        self.button_edit_customer = tk.Button(root, text='Kunde bearbeiten', command=self.edit_customer)
        self.button_edit_customer.grid(row=6, column=1, padx=10, pady=10)

        self.button_delete_customer = tk.Button(root, text='Kunde löschen', command=self.delete_customer)
        self.button_delete_customer.grid(row=6, column=2, padx=10, pady=10)

        # Fügen Sie die StatsPage und EmailIntegration zu Ihrer GUI-Klasse hinzu
        self.stats_page = StatsPage(root, self)
        self.stats_page.grid(row=11, column=0, columnspan=2, pady=10)

        self.email_integration = EmailIntegration(root, self)
        self.email_integration.grid(row=12, column=0, columnspan=2, pady=10)

    def add_customer(self):
        # Holen Sie Daten aus den Eingabefeldern
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        birthdate = self.entry_birthdate.get()
        notes = self.entry_notes.get()

        # Fügen Sie den Kunden zur Datenbank hinzu
        self.db.add_customer(name, email, phone, address, birthdate, notes)

        # Aktualisieren Sie die Anzeige der Kunden
        self.display_customers()

        # Löschen Sie die Eingabefelder
        self.clear_entries()

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

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Fehler', 'Bitte wählen Sie einen Kunden aus, den Sie löschen möchten.')
            return

        confirm = messagebox.askyesno('Bestätigen', 'Möchten Sie diesen Kunden wirklich löschen?')
        if confirm:
            customer_id = self.tree.item(selected_item, 'values')[0]
            self.db.delete_customer(customer_id)
            messagebox.showinfo('Erfolg', 'Kunde gelöscht!')
            self.clear_entries()
            self.display_customers()

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

    def close_db_connection(self):
        self.db.close_connection()


# Starte die Anwendung
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

