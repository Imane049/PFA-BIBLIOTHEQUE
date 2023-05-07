import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import sys
sys.path.append('C:\\Users\\Imane\\Desktop\\Nouveau dossier (3)')
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

conn.commit()

delai_emprunt = 15
delai_reservation = 7
print("table client connected successfuly")





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


