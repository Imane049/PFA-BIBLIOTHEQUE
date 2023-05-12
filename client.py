import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import sys
sys.path.append(r"C:\Users\Imane\Desktop\Nouveau dossier (3)")
import functions
import admin
import qsqds
import book_functions
import client_functions
import login





##set root_client
def client_root():
    root_client= tk.Tk()
    root_client.geometry("800x500")

    style = ThemedStyle(root_client)
    print("done1")
    style.set_theme("breeze")
    print("done2")


    tabControl=ttk.Notebook(root_client)

    BrowseBooks_tab=ttk.Frame(tabControl)
    browserentals_tab=ttk.Frame(tabControl)
    ManageAccount_tab=ttk.Frame(tabControl)

    tabControl.add(BrowseBooks_tab, text="Browse Books")
    tabControl.add(browserentals_tab, text="Manage reservations")
    tabControl.add(ManageAccount_tab, text="Manage account")

    tabControl.pack(expand=1, fill="both")

##SET BrowseBooks TAB
    search_label = ttk.Label(BrowseBooks_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    searchbook_entry =ttk.Entry(BrowseBooks_tab)
    searchbook_entry.pack(side="top", fill="x")

    search_button = ttk.Button(BrowseBooks_tab, text="Search", command=lambda : searchBook(searchbook_entry, BookTree))
    search_button.pack(side="top", padx=5, pady=5)


    search_options_frame = tk.Frame(BrowseBooks_tab)

    def show_search_options(frame):
        if not frame.winfo_ismapped():
            frame.pack(side='top', fill='x', padx=5, pady=5)
        else:
            if frame.pack_info():
                frame.pack_forget()
            else:
                frame.pack(side="top", fill="x", padx=5, pady=5)

    more_options_button = ttk.Button(BrowseBooks_tab, text="More options", command=lambda: show_search_options(search_options_frame))
    more_options_button.pack(side="top")

    search_type = tk.StringVar()
    isbn_checkbutton = ttk.Radiobutton(search_options_frame, text="ISBN", variable=search_type, value="isbn")
    isbn_checkbutton.pack(side="left", padx=2)

    author_checkbutton = ttk.Radiobutton(search_options_frame, text="Author", variable=search_type, value="author")
    author_checkbutton.pack(side="left", padx=2)

    genre_checkbutton = ttk.Radiobutton(search_options_frame, text="Genre", variable=search_type, value="genre")
    genre_checkbutton.pack(side="left", padx=2)

    year_checkbutton = ttk.Radiobutton(search_options_frame, text="year", variable=search_type, value="year")
    year_checkbutton.pack(side="left", padx=2)


    language_checkbutton = ttk.Radiobutton(search_options_frame, text="Language", variable=search_type, value="language")
    language_checkbutton.pack(side="left", padx=2)

    search_label1 = ttk.Label(search_options_frame, text="Search:")
    search_label1.pack(side="top",fill="x", padx=5, pady=5)

    searchbook_entry1 =ttk.Entry(search_options_frame)
    searchbook_entry1.pack(side="top", fill="x")

    search_button1 = ttk.Button(search_options_frame, text="Search", command=lambda : searchBook1(search_type, searchbook_entry1, BookTree))
    search_button1.pack(side="top", padx=5, pady=5)

    BookTree = ttk.Treeview(BrowseBooks_tab, columns=('ID','ISBN', 'Titre', 'Auteur', 'Genre', 'Langue', 'année', 'Contemplation sur place'))

    BookTree.heading('ID', text='ID')
    BookTree.heading('ISBN', text='ISBN')
    BookTree.heading('Titre', text='Titre')
    BookTree.heading('Auteur', text='Auteur')
    BookTree.heading('Genre', text='Genrea')
    BookTree.heading('Langue', text='Langue')
    BookTree.heading('année', text='année')
    BookTree.heading('Contemplation sur place', text='Contemplation sur place')

    scrollbar = ttk.Scrollbar(BrowseBooks_tab, orient='horizontal', command=BookTree.xview)
    scrollbar.pack(side='bottom', fill='x')

    BookTree.configure(xscrollcommand=scrollbar.set)

    scrollbary = ttk.Scrollbar(BrowseBooks_tab, orient='vertical', command=BookTree.yview)
    scrollbary.pack(side='right', fill='y')

    BookTree.configure(yscrollcommand=scrollbary.set)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOKS")
    books = cursor.fetchall()
    for book in books:
        BookTree.insert("", "end",  values=(book[0], book[7], book[1], book[2], book[3],book[4], book[5], "oui" if book[6]==1 else "non"))

    BookTree.bind("<<TreeviewOpen>>", lambda event: showBookInfoClient(BookTree))
    selected_items = BookTree.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = ClientTree.item(selected_item)['values']
        selected_id = values[0]


    BookTree.pack()
    modifier_button = ttk.Button(BrowseBooks_tab, text="Reserver", command=lambda: reserver(selected_id))
    modifier_button.pack()



##SET BROWSE rentals TAB
    search_label = ttk.Label(browserentals_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    searchrental_entry = ttk.Entry(browserentals_tab)
    searchrental_entry.pack(side="top", fill="x")

    RentalTree = ttk.Treeview(browserentals_tab, columns=('ID Livre','ISBN Livre', 'Titre Livre', "Date D'emprunt", 'Durée de l\'emprunt', 'Retard', 'Livre résérvé'))


    RentalTree.heading('ID Livre', text='ID Livre')
    RentalTree.heading('ISBN Livre', text='ISBN Livre')
    RentalTree.heading('Titre Livre',  text='Titre Livre')
    RentalTree.heading("Date D'emprunt", text='Date D\'emprunt')
    RentalTree.heading( 'Retard',   text='Retard')
    RentalTree.heading( 'Livre résérvé',   text='Livre résérvé')

    scrollbar = ttk.Scrollbar(browserentals_tab, orient='horizontal', command=RentalTree.xview)
    scrollbar.pack(side='bottom', fill='x')

    RentalTree.configure(xscrollcommand=scrollbar.set)


    scrollbary = ttk.Scrollbar(browserentals_tab, orient='vertical', command=RentalTree.yview)
    scrollbar.pack(side='left', fill='y')

    RentalTree.configure(yscrollcommand=scrollbary.set)

    cursor = conn.cursor()
    cursor.execute("SELECT rentals.*, BOOKS.ISBN, BOOKS.TITLE, rentals.DATE_EMPRUNT,  date(rentals.DATE_EMPRUNT, '+{} days') < date('now') FROM rentals JOIN BOOKS ON rentals.BOOK_ID=BOOKS.ID where rentals.CLIENT_ID= ?".format(delai_emprunt),(session[0],))

    rentals = cursor.fetchall()
    for rental in rentals:
        print(rental)
        RentalTree.insert("", "end", values=(rental[0],rental[3],rental[4], rental[5],"oui" if rental[6]==1 else "non"))

    RentalTree.pack()

##set manage account
    id=session[0]
    client=conn.cursor().execute("select * from client where id = ?", (id,)).fetchone()
    personalname_label = ttk.Label(ManageAccount_tab, text="Personal Name :")
    personalname_label.pack()
    personalname_entry =ttk.Entry(ManageAccount_tab, textvariable=client[1])
    personalname_entry.insert(0, client[1])
    personalname_entry.pack()

    familyname_label = ttk.Label(ManageAccount_tab, text="Family Name :")
    familyname_label.pack()
    familyname_entry =ttk.Entry(ManageAccount_tab, textvariable=client[2])
    familyname_entry.insert(0, client[2])
    familyname_entry.pack()

    username_label = ttk.Label(ManageAccount_tab, text="Username Name :")
    username_label.pack()
    username_entry =ttk.Entry(ManageAccount_tab  ,textvariable= client[8])
    username_entry.insert(0, client[8])
    username_entry.pack()

    password_label = ttk.Label(ManageAccount_tab, text="Password :")
    password_label.pack()
    password_entry =ttk.Entry(ManageAccount_tab, textvariable=client[3])
    password_entry.insert(0, client[3])
    password_entry.pack()

    age_label = ttk.Label(ManageAccount_tab, text="Age :")
    age_label.pack()
    age_entry =ttk.Entry(ManageAccount_tab, textvariable=client[4])
    age_entry.insert(0, client[4])
    age_entry.pack()

    adress_label = ttk.Label(ManageAccount_tab, text="Adress :")
    adress_label.pack()
    adress_entry =ttk.Entry(ManageAccount_tab, textvariable=client[5])
    adress_entry.insert(0, client[5])
    adress_entry.pack()

    phone_label = ttk.Label(ManageAccount_tab, text="Phone :")
    phone_label.pack()
    phone_entry =ttk.Entry(ManageAccount_tab, textvariable=client[6])
    phone_entry.insert(0, client[6])
    phone_entry.pack()

    email_label = ttk.Label(ManageAccount_tab, text="Email :")
    email_label.pack()
    email_entry =ttk.Entry(ManageAccount_tab, textvariable=client[7])
    email_entry.insert(0, client[7])
    email_entry.pack()

    modifier_button = ttk.Button(ManageAccount_tab, text="Modifier Compte", command=lambda: modifyaccount(client[0], personalname_entry, familyname_entry, username_entry, age_entry, password_entry, adress_entry, phone_entry, email_entry))
    modifier_button.pack()
    supprimer_button = ttk.Button(ManageAccount_tab, text="Supprimer Compte", command=lambda: (delaccount(client[0]),  root_client.destroy(), tk.Topkevel(acceuil.root) ))
    supprimer_button.pack()
    deconnexion_button = ttk.Button(ManageAccount_tab, text="Se deconnecter", command=lambda: (root_client.destroy(), home_root() ))
    deconnexion_button.pack()
    root_client.mainloop()

    cursor = conn.cursor()
    cursor.execute("SELECT rentals.*, BOOKS.TITLE, rentals.DATE_EMPRUNT, date(rentals.DATE_EMPRUNT, '+{} days') < date('now') FROM (rentals JOIN BOOKS ON rentals.BOOK_ID=BOOKS.ID) JOIN CLIENT ON rentals.CLIENT_ID=CLIENT.ID WHERE CLIENT_ID = ? ".format(delai_emprunt), (session[0],))
    result = cursor.fetchone()
    if result and result[4] == 1:
        messagebox.showinfo("RETARD", "Vous avez un retard de retour à la librairie concernant le livre {}. \nNous vous prions de bien vouloir les retourner dès que possible afin d'éviter toute pénalité.".format(result[3]))
    else:
        print("pas de retard")



def delaccount(id):
    answer = messagebox.askquestion("Confirmation", "Vous etes sur le point de supprimer votre compte!!  \n Cette fenetre sera fermée  \nEtes vous sur de continuer? \n Cette fenetre sera fermée aprés")
    if answer=="yes":
        client=conn.cursor().execute("select * from client where id = ?", (id,)).fetchone()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM CLIENT WHERE ID=?", (id,))
        conn.commit()
        messagebox.showinfo("Info", "Account deleted successfully!")





def modifyaccount(id, personalname_entry, familyname_entry, username_entry, age_entry, password_entry, adress_entry, phone_entry, email_entry):
    personalname = personalname_entry.get()
    familyname = familyname_entry.get()
    username=username_entry.get()
    password=password_entry.get()
    adress = adress_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    age=age_entry.get()
    cursor = conn.cursor()
    cursor.execute("UPDATE CLIENT SET PERSONAL_NAME=?, FAMILY_NAME=?, USERNAME=?, AGE=?, PASSWORD=?, ADDRESS=?, PHONE=?, EMAIL=? WHERE ID=?", (personalname, familyname, username, age, password, adress, phone, email,id ))

    conn.commit()
    messagebox.showinfo("Info", "Account modified successfully!")


