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
import client
from ttkthemes import ThemedStyle
import smtplib
##connection to database

conn=sqlite3.connect("bibliotheque.db")
print("database connected successfully")


##creation des tables admin et client
conn.execute("""CREATE TABLE IF NOT EXISTS BIBLIOTHECAIRE(BIBLIOTHECAIRE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
USERNAME TEXT NOT NULL,
PASSWORD TEXT NOT NULL)""")
#La bibliotheque a un seul admin
conn.execute("""CREATE TRIGGER IF NOT EXISTS enforce_single_row
BEFORE INSERT ON BIBLIOTHECAIRE
BEGIN
  SELECT
    CASE
      WHEN (SELECT COUNT(*) FROM BIBLIOTHECAIRE) >= 1 THEN
        RAISE(ABORT, 'Only one row is allowed in this table')
    END;
END;
""")
conn.execute("""INSERT INTO BIBLIOTHECAIRE(USERNAME, PASSWORD)
SELECT ? , ?
WHERE NOT EXISTS (SELECT 1 FROM BIBLIOTHECAIRE)""", ("admin", "pwd"))
print("table bibliothecaire connected successfully")
#conn.execute("""INSERT INTO BIBLIOTHECAIRE(USERNAME, PASSWORD) VALUES("admin","pwd")""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS CLIENT (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PERSONAL_NAME TEXT NOT NULL,
        FAMILY_NAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        AGE INTEGER,
        ADDRESS TEXT,
        PHONE INTEGER NOT NULL,
        EMAIL TEXT NOT NULL,
        USERNAME TEXT
    )
""")



conn.execute("""CREATE TABLE IF NOT EXISTS BOOKS (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT NOT NULL, AUTHOR TEXT NOT NULL, GENRE TEXT, LANGUAGE TEXT, year INTEGER , CONTEMPLATION_SUR_PLACE INTEGER CHECK (CONTEMPLATION_SUR_PLACE IN (0,1)), ISBN INTEGER NOT NULL, IMAGE BLOB)""")

conn.execute("""CREATE TABLE IF NOT EXISTS rentals (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

conn.execute("""CREATE TABLE IF NOT EXISTS reservations (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

delai_emprunt = 15
delai_reservation = 17
print("table client connected successfuly")


import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import random
import string
import sys
sys.path.append(r"C:\Users\Imane\Desktop\Nouveau dossier (3)")
import functions
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
    Statistics_tab=ttk.Frame(tabControl)


    tabControl.add(ManageClients_tab, text="Manage adherents")
    tabControl.add(ManageBooks_tab, text="Manage books")
    tabControl.add(Managerentals_tab, text="Manage rentals")
    tabControl.add(ManageAccount_tab, text="Manage account")
    tabControl.add(Statistics_tab, text="Statistics")


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
    browserentals_tab=ttk.Frame(tabControl3)

    tabControl3.add(addrental_tab, text="Add rental")
    tabControl3.add(return_tab, text="Book Return")
    tabControl3.add(browserentals_tab, text="Browse rentals")
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
        ClientTree.insert("", "end",text="", values=(client[0],client[2]+client[1], client[4], client[5],client[6], client[7]))


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
        BookTree.insert("", "end",text="",  values=(book[0], book[7], book[1], book[2], book[3],book[4], book[5], "oui" if book[6]==1 else "non"))

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



##SET BROWSE rentals TAB
    search_label = ttk.Label(browserentals_tab, text="Search:")
    search_label.pack(side="top",fill="x", padx=5, pady=5)

    searchrental_entry = ttk.Entry(browserentals_tab)
    searchrental_entry.pack(side="top", fill="x")

    RentalTree = ttk.Treeview(browserentals_tab, columns=('ID Client','Nom Client', 'ID Livre', 'Titre Livre', "Date D'emprunt", 'Durée de l\'emprunt', 'Retard', 'Livre résérvé'))

    search_button = ttk.Button(browserentals_tab, text="Search", command=lambda : searchRental( searchrental_entry, RentalTree))
    search_button.pack(side="top", padx=5, pady=5)



    RentalTree.heading('ID Client', text='ID Client')
    RentalTree.heading('Nom Client', text='Nom Client')
    RentalTree.heading('ID Livre', text='ID Livre')
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
    cursor.execute("SELECT rentals.*, CLIENT.PERSONAL_NAME || ' ' || CLIENT.FAMILY_NAME, BOOKS.TITLE, rentals.DATE_EMPRUNT, date(rentals.DATE_EMPRUNT || '+{} days') < date('now') FROM (rentals JOIN BOOKS ON rentals.BOOK_ID=BOOKS.ID) JOIN CLIENT ON rentals.CLIENT_ID=CLIENT.ID".format(delai_emprunt, delai_emprunt))


    rentals = cursor.fetchall()
    for rental in rentals:
        RentalTree.insert("", "end",text="", values=(rental[1],rental[3],rental[0],rental[4], rental[5],"oui" if rental[6]==1 else "non"))

    RentalTree.pack()




    root_admin.mainloop()


##login function
def login(home, username_entry, password_entry, login_type):
    user_type=login_type.get()
    username=username_entry.get()
    password=password_entry.get()
    cursor=conn.cursor()
    cursor.execute(''' SELECT * FROM {} WHERE USERNAME=? AND PASSWORD = ?'''.format(user_type), (username, password))
    identified=cursor.fetchone()

    if identified and user_type=="bibliothecaire":
        global session
        session=identified
        print(session)
        home.destroy()
        root_admin()
    elif identified and user_type=="client":
        session=identified
        print(session)
        home.destroy()
        client_root()
    else:
        messagebox.showinfo("Alert", "Wrong Username or password! \n Please try again")
"""" except Exception as e:
            messagebox.showinfo("Alert", "Erreur rencontrée! \n Veuillez réessayer ultiérieurment")
            print(str(e))"""

##def signup function
def signup(personalname_entry,familyname_entry,age_entry, adress_entry, phone_entry, email_entry):
    personalname=personalname_entry.get()
    familyname=familyname_entry.get()
    age=age_entry.get()
    adress=adress_entry.get()
    phone=phone_entry.get()
    email=email_entry.get()
    cursor=conn.cursor()
    length = random.randint(8, 12)
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    try:
        cursor.execute("INSERT INTO CLIENT(PERSONAL_NAME, family_name, password, age, address, phone, email) VALUES(? ,?, ? ,? ,? ,? ,?)",(personalname, familyname, password, age, adress, phone, email))
        conn.commit()
        username=personalname+str(cursor.lastrowid)
        cursor.execute("UPDATE CLIENT SET USERNAME= ? WHERE ID=?", (username, cursor.lastrowid))
        conn.commit()
        messagebox.showinfo("INFO", "Compte crée avec succès \n Veuillez noter votre nom d'utilisater et votre mot de passe pour des connexions ultérieures \n ")
        show_client(cursor.lastrowid)
    except:
        messagebox.showinfo("INFO", "Veuillez remplir tout les champs correctements")



##Set login layout

def home_root():
    home = tk.Tk()
    home.geometry("800x500")

    style = ThemedStyle(home)
    style.set_theme("breeze")

    tabControl = ttk.Notebook(home)

    Login_tab = ttk.Frame(tabControl)
    Signup_tab = ttk.Frame(tabControl)

    tabControl.add(Login_tab, text="Login")
    tabControl.add(Signup_tab, text="Signup")

    tabControl.pack(expand=1, fill="both")

    ##set logintab
    username_label = ttk.Label(Login_tab, text="Username:")
    username_label.pack()
    username_entry = ttk.Entry(Login_tab)
    username_entry.pack()

    password_label = ttk.Label(Login_tab, text="Password:")
    password_label.pack()
    password_entry = ttk.Entry(Login_tab, show="*")
    password_entry.pack()

    login_button = ttk.Button(Login_tab, text="Login", command=lambda: login(home, username_entry, password_entry, login_type))
    login_button.pack()

    label = ttk.Label(Login_tab, text="Choose an option:")
    label.pack()

    login_type = tk.StringVar()

    option1 = ttk.Radiobutton(Login_tab, text="bibliothecaire", variable=login_type, value="bibliothecaire")
    option1.pack()

    option2 = ttk.Radiobutton(Login_tab, text="client", variable=login_type, value="client")
    option2.pack()



##set signuptab
    personalname_label = ttk.Label(Signup_tab, text="Personal Name :")
    personalname_label.pack()
    personalname_entry = ttk.Entry(Signup_tab)
    personalname_entry.pack()

    familyname_label = ttk.Label(Signup_tab, text="Family Name :")
    familyname_label.pack()
    familyname_entry = ttk.Entry(Signup_tab)
    familyname_entry.pack()

    age_label = ttk.Label(Signup_tab, text="Username :")
    age_label.pack()
    age_entry = ttk.Entry(Signup_tab)
    age_entry.pack()

    adress_label = ttk.Label(Signup_tab, text="Adress :")
    adress_label.pack()
    adress_entry = ttk.Entry(Signup_tab)
    adress_entry.pack()

    phone_label = ttk.Label(Signup_tab, text="Phone :")
    phone_label.pack()
    phone_entry = ttk.Entry(Signup_tab)
    phone_entry.pack()

    email_label = ttk.Label(Signup_tab, text="Email :")
    email_label.pack()
    email_entry = ttk.Entry(Signup_tab)
    email_entry.pack()

    addClient_button = ttk.Button(Signup_tab, text="add", command=lambda: signup(personalname_entry,familyname_entry,age_entry, adress_entry, phone_entry, email_entry))
    addClient_button.pack()

    home.mainloop()





home_root()


