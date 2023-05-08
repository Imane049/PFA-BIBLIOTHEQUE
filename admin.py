import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import random
import string
import functions
import login
import qsqds
import book_functions
import client_functions



##set root_admin
def root_admin():
    root_admin= tk.Tk()
    root_admin.geometry("800x500")
    style = ThemedStyle(root_admin)
    print("done1")
    style.set_theme("breeze")
    print("done2")

    tabControl=ttk.Notebook(root_admin)

    ManageClients_tab=ttk.Frame(tabControl)
    ManageBooks_tab=ttk.Frame(tabControl)
    Managerentals_tab=ttk.Frame(tabControl)
    ManageAccount_tab=ttk.Frame(tabControl)

    tabControl.add(ManageClients_tab, text="Manage adherents")
    tabControl.add(ManageBooks_tab, text="Manage books")
    tabControl.add(Managerentals_tab, text="Manage rentals")
    tabControl.add(ManageAccount_tab, text="Manage account")

    tabControl.pack(expand=1, fill="both")


##SET MANAGEACCOUNT_TAB



##set ManageClients_tab
    tabControl1=ttk.Notebook(ManageClients_tab)

    addClient_tab=ttk.Frame(tabControl1)
    browseClients_tab=ttk.Frame(tabControl1)


    tabControl1.add(addClient_tab, text="Add Client")
    tabControl1.add(browseClients_tab, text="Browse Clients")

    tabControl1.pack(expand=1, fill="both")

##set ADD Client tab
    personalname_label = ttk.Label(addClient_tab, text="Full Name :")
    personalname_label.pack()
    personalname_entry = ttk.Entry(addClient_tab)
    personalname_entry.pack()

    familyname_label = ttk.Label(addClient_tab, text="Full Name :")
    familyname_label.pack()
    familyname_entry = ttk.Entry(addClient_tab)
    familyname_entry.pack()

    age_label = ttk.Label(addClient_tab, text="Age :")
    age_label.pack()
    age_entry = ttk.Entry(addClient_tab)
    age_entry.pack()

    adress_label = ttk.Label(addClient_tab, text="Adress :")
    adress_label.pack()
    adress_entry = ttk.Entry(addClient_tab)
    adress_entry.pack()

    phone_label = ttk.Label(addClient_tab, text="Phone :")
    phone_label.pack()
    phone_entry = ttk.Entry(addClient_tab)
    phone_entry.pack()

    email_label = ttk.Label(addClient_tab, text="Email :")
    email_label.pack()
    email_entry = ttk.Entry(addClient_tab)
    email_entry.pack()

    addClient_button = ttk.Button(addClient_tab, text="add", command=lambda: addClient(ClientTree, personalname_entry,familyname_entry,age_entry, adress_entry, phone_entry, email_entry))
    addClient_button.pack()


##set manage account
    id=session[0]
    client=conn.cursor().execute("select * from bibliothecaire where bibliothecaire_id = ?", (id,)).fetchone()
    bibliothecaire_label = ttk.Label(ManageAccount_tab, text="Nom Bibliothecaire :")
    bibliothecaire_label.pack()
    bibliothecaire_entry =ttk.Entry(ManageAccount_tab, textvariable=client[1])
    bibliothecaire_entry.insert(0, client[1])
    bibliothecaire_entry.pack()


    password_label = ttk.Label(ManageAccount_tab, text="Password :")
    password_label.pack()
    password_entry =ttk.Entry(ManageAccount_tab, textvariable=client[2])
    password_entry.insert(0, client[2])
    password_entry.pack()



    modifier_button = ttk.Button(ManageAccount_tab, text="Modifier Compte", command=lambda: (conn.execute("UPDATE BIBLIOTHECAIRE SET USERNAME = ?, PASSWORD= ? WHERE BIBLIOTHECAIRE_ID=?",(bibliothecaire_entry.get(),password_entry.get(),id))))
    modifier_button.pack()

    deconnexion_button = ttk.Button(ManageAccount_tab, text="Se deconnecter", command=lambda: (root_admin.destroy(), home_root() ))
    deconnexion_button.pack()

##set ManageBooks_tab
    tabControl2=ttk.Notebook(ManageBooks_tab)

    addBook_tab=ttk.Frame(tabControl2)
    browseBooks_tab=ttk.Frame(tabControl2)

    tabControl2.add(addBook_tab, text="Add Book")
    tabControl2.add(browseBooks_tab, text="Browse Books")

    tabControl2.pack(expand=1, fill="both")



##set ADD BOOK TAB
    title_label = ttk.Label(addBook_tab, text="Book Title :")
    title_label.pack()
    title_entry = ttk.Entry(addBook_tab)
    title_entry.pack()

    author_label = ttk.Label(addBook_tab, text="Author Name :")
    author_label.pack()
    author_entry = ttk.Entry(addBook_tab)
    author_entry.pack()

    genre_label = ttk.Label(addBook_tab, text="Genre :")
    genre_label.pack()
    genre_entry = ttk.Entry(addBook_tab)
    genre_entry.pack()

    language_label = ttk.Label(addBook_tab, text="Language :")
    language_label.pack()
    language_entry = ttk.Entry(addBook_tab)
    language_entry.pack()

    year_label = ttk.Label(addBook_tab, text="year :")
    year_label.pack()
    year_entry = ttk.Entry(addBook_tab)
    year_entry.pack()

    ISBN_label = ttk.Label(addBook_tab, text="ISBN Year :")
    ISBN_label.pack()
    ISBN_entry = ttk.Entry(addBook_tab)
    ISBN_entry.pack()

    label = ttk.Label(addBook_tab, text="Contemplation sur place ?")
    label.pack()

    cpsp = tk.IntVar()

    option1 = tk.Radiobutton(addBook_tab, text="oui", variable=cpsp, value="1")
    option1.pack()

    option2 = tk.Radiobutton(addBook_tab, text="non", variable=cpsp, value="0")
    option2.pack()


    label_image_path = ttk.Label(addBook_tab, text="File Path:")
    label_image_path.pack()

    entry_image_path = ttk.Entry(addBook_tab)
    entry_image_path.pack()

    button_image_browse = ttk.Button(addBook_tab, text="Browse", command= lambda : browse_file(entry_image_path))
    button_image_browse.pack()


    addBook_button = ttk.Button(addBook_tab, text="add book", command=lambda: addBook(BookTree, title_entry,author_entry,genre_entry, language_entry, year_entry, ISBN_entry, cpsp, entry_image_path))
    addBook_button.pack()





##set Managerentals_tab
    tabControl3=ttk.Notebook(Managerentals_tab)

    addrental_tab=ttk.Frame(tabControl3)
    return_tab=ttk.Frame(tabControl3)
    browseRentals_tab=ttk.Frame(tabControl3)

    tabControl3.add(addrental_tab, text="Add rental")
    tabControl3.add(return_tab, text="Book Return")
    tabControl3.add(browseRentals_tab, text="Browse Rentals")
    tabControl3.add(return_tab, text="Book Return")

    tabControl3.pack(expand=1, fill="both")

##set ADD rental TAB
    client_label = ttk.Label(addrental_tab, text="Client id :")
    client_label.pack()
    client_entry = ttk.Entry(addrental_tab)
    client_entry.pack()

    book_label = ttk.Label(addrental_tab, text="Book id :")
    book_label.pack()
    book_entry = ttk.Entry(addrental_tab)
    book_entry.pack()

    addrental_button = ttk.Button(addrental_tab, text="add resrevation", command=lambda: addrental(RentalTree, client_entry, book_entry))
    addrental_button.pack()
##return
    client_label = ttk.Label(return_tab, text="Client id :")
    client_label.pack()
    client_entry = ttk.Entry(return_tab)
    client_entry.pack()

    book_label = ttk.Label(return_tab, text="Book id :")
    book_label.pack()
    book_entry = ttk.Entry(return_tab)
    book_entry.pack()

    addrental_button = ttk.Button(return_tab, text="register return", command=lambda: Return(client_entry,book_entry))
    addrental_button.pack()

##SET BROWSECLIENTS TAB

    search_label = ttk.Label(browseClients_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    search_entry = ttk.Entry(browseClients_tab)
    search_entry.pack(side="top", fill="x")

    search_button = ttk.Button(browseClients_tab, text="Search", command=lambda : searchClient(search_entry, ClientTree))
    search_button.pack(side="top", padx=5, pady=5)

    ClientTree = ttk.Treeview(browseClients_tab, columns=('ID', 'Nom et Prénom', 'Age', 'Adresse', 'N° de téléphone', 'Email'))

    ClientTree.heading('ID', text='ID')
    ClientTree.heading('Nom et Prénom', text='Nom et Prénom')
    ClientTree.heading('Age', text='Age')
    ClientTree.heading('Adresse', text='Adresse')
    ClientTree.heading('N° de téléphone', text='N° de téléphone')
    ClientTree.heading('Email', text='Email')

    scrollbar = ttk.Scrollbar(browseClients_tab, orient='horizontal', command=ClientTree.xview)
    scrollbar.pack(side='bottom', fill='x')

    ClientTree.configure(xscrollcommand=scrollbar.set)


    scrollbary = ttk.Scrollbar(browseClients_tab, orient='vertical', command=ClientTree.yview)
    scrollbary.pack(side='right', fill='y')

    ClientTree.configure(yscrollcommand=scrollbary.set)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENT")
    clients = cursor.fetchall()
    for client in clients:
        ClientTree.insert("", "end", values=(client[0],client[2]+client[1], client[4], client[5],client[6], client[7]))


    ClientTree.bind("<<TreeviewOpen>>", lambda event: showClientInfo(ClientTree))

    ClientTree.pack()

##SET BROWSEBOOKS TAB
    search_label = ttk.Label(browseBooks_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    searchbook_entry = ttk.Entry(browseBooks_tab)
    searchbook_entry.pack(side="top", fill="x")

    search_button = ttk.Button(browseBooks_tab, text="Search", command=lambda : searchBook(searchbook_entry, BookTree))
    search_button.pack(side="top", padx=5, pady=5)

    search_options_frame = tk.Frame(browseBooks_tab)

    def show_search_options(frame):
        if not frame.winfo_ismapped():
            frame.pack(side='top', fill='x', padx=5, pady=5)
        else:
            if frame.pack_info():
                frame.pack_forget()
            else:
                frame.pack(side="top", fill="x", padx=5, pady=5)

    more_options_button = ttk.Button(browseBooks_tab, text="More options", command=lambda: show_search_options(search_options_frame))
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


    BookTree = ttk.Treeview(browseBooks_tab, columns=('ID','ISBN', 'Titre', 'Auteur', 'Genre', 'Langue', 'année', 'Contemplation sur place'))

    BookTree.heading('ID', text='ID')
    BookTree.heading('ISBN', text='ISBN')
    BookTree.heading('Titre', text='Titre')
    BookTree.heading('Auteur', text='Auteur')
    BookTree.heading('Genre', text='Genrea')
    BookTree.heading('Langue', text='Langue')
    BookTree.heading('année', text='année')
    BookTree.heading('Contemplation sur place', text='Contemplation sur place')

    scrollbar = ttk.Scrollbar(browseBooks_tab, orient='horizontal', command=BookTree.xview)
    scrollbar.pack(side='bottom', fill='x')

    BookTree.configure(xscrollcommand=scrollbar.set)

    scrollbary = ttk.Scrollbar(browseBooks_tab, orient='vertical', command=BookTree.yview)
    scrollbary.pack(side='right', fill='y')

    BookTree.configure(yscrollcommand=scrollbary.set)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOKS")
    books = cursor.fetchall()
    for book in books:
        BookTree.insert("", "end",  values=(book[0], book[7], book[1], book[2], book[3],book[4], book[5], "oui" if book[6]==1 else "non"))

    BookTree.bind("<<TreeviewOpen>>", lambda event: showBookInfo(BookTree))
    selected_items = BookTree.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = ClientTree.item(selected_item)['values']
        selected_id = values[0]
        cursor.execute("SELECT * FROM BOOKS WHERE ID = ?", (selected_id,))
        book=cursor.fetchone()
        print(book)

    BookTree.pack()



##SET BROWSE REntals TAB
    search_label = ttk.Label(browseRentals_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    searchrental_entry = ttk.Entry(browseRentals_tab)
    searchrental_entry.pack(side="top", fill="x")

    RentalTree = ttk.Treeview(browseRentals_tab, columns=('ID Client','Nom Client', 'ID Livre', 'Titre Livre', "Date D'emprunt", 'Durée de l\'emprunt', 'Retard', 'Livre résérvé'))

    search_button = ttk.Button(browseRentals_tab, text="Search", command=lambda : searchRental( searchrental_entry, RentalTree))
    search_button.pack(side="top", padx=5, pady=5)



    RentalTree.heading('ID Client', text='ID Client')
    RentalTree.heading('Nom Client', text='Nom Client')
    RentalTree.heading('ID Livre', text='ID Livre')
    RentalTree.heading('Titre Livre',  text='Titre Livre')
    RentalTree.heading("Date D'emprunt", text='Date D\'emprunt')
    RentalTree.heading( 'Retard',   text='Retard')
    RentalTree.heading( 'Livre résérvé',   text='Livre résérvé')

    scrollbar = ttk.Scrollbar(browseRentals_tab, orient='horizontal', command=RentalTree.xview)
    scrollbar.pack(side='bottom', fill='x')

    RentalTree.configure(xscrollcommand=scrollbar.set)


    scrollbary = ttk.Scrollbar(browseRentals_tab, orient='vertical', command=RentalTree.yview)
    scrollbar.pack(side='left', fill='y')

    RentalTree.configure(yscrollcommand=scrollbary.set)

    cursor = conn.cursor()
    cursor.execute("SELECT rentals.*, CLIENT.PERSONAL_NAME || ' ' || CLIENT.FAMILY_NAME, BOOKS.TITLE, rentalS.DATE_EMPRUNT, date(rentalS.DATE_EMPRUNT || '+{} days') < date('now') FROM (rentalS JOIN BOOKS ON rentalS.BOOK_ID=BOOKS.ID) JOIN CLIENT ON rentalS.CLIENT_ID=CLIENT.ID".format(delai_emprunt, delai_emprunt))


    rentals = cursor.fetchall()
    for rental in rentals:
        RentalTree.insert("", "end", values=(rental[1],rental[3],rental[0],rental[4], rental[5],"oui" if rental[6]==1 else "non"))

    RentalTree.pack()




    root_admin.mainloop()