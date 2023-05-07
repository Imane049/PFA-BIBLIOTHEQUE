import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

import random
import string
import sys
sys.path.append('C:\\Users\\Imane\\Desktop\\Nouveau dossier (3)')
import admin
import acceuil
import qsqds


##ADD CLIENT FUNCTION
def addClient(ClientTree, personalname_entry, familyname_entry,age_entry, adress_entry, phone_entry, email_entry):
    personalname = personalname_entry.get()
    familyname = familyname_entry.get()
    adress = adress_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    age=age_entry.get()
    length = random.randint(8, 12)
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO CLIENT(PERSONAL_NAME, FAMILY_NAME, AGE, PASSWORD, ADDRESS, PHONE, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)",(personalname, familyname, age, password, adress, phone, email))
        id=cursor.lastrowid
        username=personalname+str(id)
        cursor.execute("UPDATE CLIENT SET USERNAME= ? WHERE ID=?", (username, id))
        ClientTree.insert("", "end", text="", values=(id,personalname + familyname, adress, phone ,email, age))
        conn.commit()
        messagebox.showinfo("Info", "Client added successfully!")
    except:
        messagebox.showinfo("INFO", "Veuiller saisir les données correctement")

##searchClientfunction

def searchClient(search_entry, ClientTree):
    search_query = search_entry.get()
    print(len(ClientTree.get_children()))
    for item in ClientTree.get_children():
        print(type(item))
        ClientTree.delete(item)
        ClientTree.update()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENT WHERE FAMILY_NAME LIKE ? OR PERSONAL_NAME LIKE ?", ('%'+search_query+'%', '%'+search_query+'%'))
    clients = cursor.fetchall()

    for client in clients:
        ClientTree.insert("", "end", text=client[0], values=(client[2]+client[1], client[4], client[5],client[6], client[7]))

##def showclientinfo function
def showClientInfo(ClientTree):
    selected_items = ClientTree.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = ClientTree.item(selected_item)['values']
        selected_id = values[0]
        print(selected_id)
        show_client(selected_id)
def show_client(selected_id):
    ClientInfo = tk.Tk()

    cursor=conn.cursor()
    cursor.execute("SELECT * FROM CLIENT WHERE ID=?", (selected_id,))
    client=cursor.fetchone()

    ClientInfo.title("Fiche Info"+ client[1] +" "+client[2])
    id_label = ttk.Button(ClientInfo, text="ID: {}".format(client[0]))
    pname_label = ttk.Button(ClientInfo, text="Personal name : {}".format(client[1]))
    fname_label = ttk.Button(ClientInfo, text=" Family Name: {}".format(client[2]))
    username_label = ttk.Button(ClientInfo, text=" Username: {}".format(client[8]))
    password_label = ttk.Button(ClientInfo, text=" Password: {}".format(client[3]))
    age_label = ttk.Button(ClientInfo, text="Age: {}".format(client[4]))
    address_label = ttk.Button(ClientInfo, text="Address: {}".format(client[5]))
    phone_label = ttk.Button(ClientInfo, text="Phone: {}".format(client[6]))
    email_label = ttk.Button(ClientInfo, text="Email: {}".format(client[7]))

    id_label.grid(row=0, column=1, padx=5, pady=5)
    pname_label.grid(row=1, column=1, padx=5, pady=5)
    fname_label.grid(row=2, column=1, padx=5, pady=5)
    username_label.grid(row=3, column=1, padx=5, pady=5)
    password_label.grid(row=4, column=1, padx=5, pady=5)
    age_label.grid(row=5, column=1, padx=5, pady=5)
    address_label.grid(row=6, column=1, padx=5, pady=5)
    phone_label.grid(row=7, column=1, padx=5, pady=5)
    email_label.grid(row=8, column=1, padx=5, pady=5)

    modClient_button =ttk.Button(ClientInfo, text="Modify", command=lambda: modClient(client))
    modClient_button.grid(row=9, column=4, padx=5, pady=5)
    delClient_button =ttk.Button(ClientInfo, text="Delete", command=lambda: delClient(client))
    delClient_button.grid(row=9, column=5, padx=5, pady=5)
    ClientInfo.mainloop()

#modclient
def modClient(client):
    modClient=tk.Tk()
    personalname_label = ttk.Button(modClient, text="Personal Name :")
    personalname_label.pack()
    personalname_entry =ttk.Entry(modClient, textvariable=client[1])
    personalname_entry.pack()

    familyname_label = ttk.Button(modClient, text="Full Name :")
    familyname_label.pack()
    familyname_entry =ttk.Entry(modClient, textvariable=client[2])
    familyname_entry.pack()

    username_label = ttk.Button(modClient, text="Full Name :")
    username_label.pack()
    username_entry =ttk.Entry(modClient  ,textvariable= client[8])
    username_entry.pack()

    password_label = ttk.Button(modClient, text="Email :")
    password_label.pack()
    password_entry =ttk.Entry(modClient, textvariable=client[3])
    password_entry.pack()

    age_label = ttk.Button(modClient, text="Age :")
    age_label.pack()
    age_entry =ttk.Entry(modClient, textvariable=client[4])
    age_entry.pack()

    adress_label = ttk.Button(modClient, text="Adress :")
    adress_label.pack()
    adress_entry =ttk.Entry(modClient, textvariable=client[5])
    adress_entry.pack()

    phone_label = ttk.Button(modClient, text="Phone :")
    phone_label.pack()
    phone_entry =ttk.Entry(modClient, textvariable=client[6])
    phone_entry.pack()

    email_label = ttk.Button(modClient, text="Email :")
    email_label.pack()
    email_entry =ttk.Entry(modClient, textvariable=client[7])
    email_entry.pack()

    modifier_button =ttk.Button(modClient, text="Modifier", command=lambda: modifyclient(client[0], personalname_entry, familyname_entry, username_entry, age_entry, password_entry, adress_entry, phone_entry, email_entry))
    modifier_button.pack()
    modClient.mainloop()

def delClient(client):
    cursor=conn.cursor()
    cursor.execute("DELETE FROM CLIENT WHERE ID=?", (client[0],))
    conn.commit()
    messagebox.showinfo("Info", "Client deleted successfully!")





def modifyclient(id, personalname_entry, familyname_entry, username_entry, age_entry, password_entry, adress_entry, phone_entry, email_entry):
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
    messagebox.showinfo("Info", "Client modified successfully!")

