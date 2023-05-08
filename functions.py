import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

import random
import string
import sys
sys.path.append('.')

import admin
import login
import qsqds
import book_functions
import client_functions


##ADD rental FUNCTION

def addrental(RentalTree, client_entry,book_entry):
    client = client_entry.get()
    book = book_entry.get()

    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM CLIENT WHERE ID=?''', (client,))
    client_exist=cursor.fetchone()
    cursor.execute('''SELECT id FROM BOOKS WHERE ID=? ''' , (book,))
    book_exist=cursor.fetchone()
    cursor.execute('''SELECT id FROM BOOKS WHERE ID=? and CONTEMPLATION_SUR_PLACE=0''' , (book,))
    book_to_rent=cursor.fetchone()

    if client_exist and book_exist and book_to_rent:
        cursor.execute("INSERT INTO rentalS(BOOK_ID, CLIENT_ID, DATE_EMPRUNT) VALUES (?, ?, date('now'))", (book, client))
        conn.commit()

        messagebox.showinfo("Info", "Book added successfully!")
    elif not client_exist:
            messagebox.showinfo("Info", "Wrong Client ID! \n Please try again")
    elif not book_exist:
            messagebox.showinfo("Info", "Wrong Book ID! \n Please try again")
    elif not book_to_rent:
            messagebox.showinfo("Info", "Book not up to rental! \n Contemplation sur place uniquement")







##search rental function
def searchRental(searchrental_entry, RentalTree):
    search_query = searchrental_entry.get()
    for item in RentalTree.get_children():
        RentalTree.delete(item)
        RentalTree.update()

    cursor = conn.cursor()

    cursor.execute("SELECT rentalS.*, CLIENT.PERSONAL_NAME || ' ' || CLIENT.FAMILY_NAME, BOOKS.TITLE, rentalS.DATE_EMPRUNT, date(rentalS.DATE_EMPRUNT, '+{} days') < date('now') FROM (rentalS JOIN BOOKS ON rentalS.BOOK_ID=BOOKS.ID) JOIN CLIENT ON rentalS.CLIENT_ID=CLIENT.ID WHERE BOOK_ID LIKE ? OR CLIENT_ID LIKE ? OR CLIENT.PERSONAL_NAME LIKE ? OR CLIENT.FAMILY_NAME LIKE ? OR BOOKS.TITLE LIKE ? OR BOOKS.ISBN LIKE ? OR BOOKS.AUTHOR LIKE ? OR BOOKS.ISBN LIKE ? OR BOOKS.GENRE LIKE ? OR BOOKS.LANGUAGE LIKE ? OR BOOKS.year LIKE ? OR BOOKS.ISBN LIKE ?".format(delai_emprunt), ('%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%' , '%'+search_query+'%' , '%'+search_query+'%' , '%'+search_query+'%' , '%'+search_query+'%'))

    rentals = cursor.fetchall()
    for rental in rentals:
        RentalTree.insert("", "end", text ="" ,values=(rental[1],rental[3],rental[0],rental[4], rental[5],"oui" if rental[6]==1 else "non"))

def Return(client_entry,book_entry):
    client_entry=client_entry.get()
    book_entry=book_entry.get()
    try:
        cursor=conn.cursor()
        cursor.execute("DELETE FROM rentalS where CLIENT_ID=? and book_id=?",(client_entry, book_entry))
        messagebox.showinfo("info", "retour enregistré")
    except Exception as e:
        messagebox.showinfo("alert", "erreur, retour innefectué")
        print(str(e))
