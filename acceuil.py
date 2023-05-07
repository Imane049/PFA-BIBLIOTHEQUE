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
        PHONE INTEGER,
        EMAIL TEXT,
        USERNAME TEXT
    )
""")



conn.execute("""CREATE TABLE IF NOT EXISTS BOOKS (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT NOT NULL, AUTHOR TEXT NOT NULL, GENRE TEXT, LANGUAGE TEXT, year TEXT , CONTEMPLATION_SUR_PLACE INTEGER CHECK (CONTEMPLATION_SUR_PLACE IN (0,1)), ISBN INTEGER NOT NULL, IMAGE BLOB)""")

conn.execute("""CREATE TABLE IF NOT EXISTS rentals (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

conn.execute("""CREATE TABLE IF NOT EXISTS reservations (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

conn.commit()

delai_emprunt = 15
delai_reservation = 7
print("table client connected successfuly")

##login function
def login():
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
        root.destroy()
        root_admin()
    elif identified and user_type=="client":
        session=identified
        print(session)
        root.destroy()
        client_root()
    else:
        messagebox.showinfo("Alert", "Wrong Username or password! \n Please try again")




##Set login layout

root = tk.Tk()
root.title('Library Login')
#oot.configure(background='#2E3436')
root.geometry("400x300")

window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry("+{}+{}".format(position_right, position_down))


style = ThemedStyle(root)
print("done1")
style.set_theme("breeze")
print("done2")

username_label = ttk.Label(root, text="Username:")
username_label.pack()
username_entry = ttk.Entry(root)
username_entry.pack()

password_label = ttk.Label(root, text="Password:")
password_label.pack()
password_entry = ttk.Entry(root, show="*")
password_entry.pack()

login_button =ttk.Button(root, text="Login", command=login)
login_button.pack()


label = ttk.Label(root, text="Choose an option:")
label.pack()

login_type = tk.StringVar()

option1 = ttk.Radiobutton(root, text="bibliothecaire", variable=login_type, value="bibliothecaire")
option1.pack()

option2 = ttk.Radiobutton(root, text="client", variable=login_type, value="client")
option2.pack()






root.mainloop()






