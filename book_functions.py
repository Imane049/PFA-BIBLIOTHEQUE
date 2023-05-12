import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import random
import string
import sys
sys.path.append(r"C:\Users\Imane\Desktop\Nouveau dossier (3)")
import admin
import login
import qsqds


def browse_file(entry_image_path):
    file_path = filedialog.askopenfilename()
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, file_path)

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
        cursor.execute("INSERT INTO rentals(BOOK_ID, CLIENT_ID, DATE_EMPRUNT) VALUES (?, ?, date('now'))", (book, client))
        conn.commit()

        messagebox.showinfo("Info", "Book added successfully!")
    elif not client_exist:
            messagebox.showinfo("Info", "Wrong Client ID! \n Please try again")
    elif not book_exist:
            messagebox.showinfo("Info", "Wrong Book ID! \n Please try again")
    elif not book_to_rent:
            messagebox.showinfo("Info", "Book not up to rental! \n Contemplation sur place uniquement")

##showbook  info set

def showBookInfo(BookTree):
    selected_items = BookTree.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = BookTree.item(selected_item)['values']
        selected_id = int(values[0])
    print(selected_id)
    print(type(selected_id))
    ficheinfo(selected_id)

def modBook(book):
    modBook = tk.Tk()
    modBook.title("Modifier un livre")
    title_label = ttk.Label(modBook, text="Titre :")
    title_label.pack()
    title_entry =ttk.Entry(modBook)
    title_entry.insert(0, book[1])
    title_entry.pack()

    author_label = ttk.Label(modBook, text="Auteur :")
    author_label.pack()
    author_entry =ttk.Entry(modBook)
    author_entry.insert(0, book[2])
    author_entry.pack()

    isbn_label = ttk.Label(modBook, text="ISBN :")
    isbn_label.pack()
    isbn_entry =ttk.Entry(modBook)
    isbn_entry.insert(0, book[7])
    isbn_entry.pack()

    genre_label = ttk.Label(modBook, text="Genre :")
    genre_label.pack()
    genre_entry =ttk.Entry(modBook)
    genre_entry.insert(0, book[3])
    genre_entry.pack()

    language_label = ttk.Label(modBook, text="Langue :")
    language_label.pack()
    language_entry =ttk.Entry(modBook)
    language_entry.insert(0, book[4])
    language_entry.pack()

    year_label = ttk.Label(modBook, text="année :")
    year_label.pack()
    year_entry =ttk.Entry(modBook)
    year_entry.insert(0, book[5])
    year_entry.pack()

    csp_label = ttk.Label(modBook, text="Contemplation sur place :")
    csp_label.pack()
    csp = tk.IntVar()

    option1 = ttk.Radiobutton(modBook, text="oui", variable=csp, value=1)
    option1.pack()

    option2 = ttk.Radiobutton(modBook, text="non", variable=csp, value=0)
    option2.pack()

    modifier_button =ttk.Button(modBook, text="Modifier", command=lambda: modifybook(book, title_entry, author_entry, genre_entry, language_entry, year_entry,1 if csp =="oui" else 0, isbn_entry))
    modifier_button.pack()
    modBook.mainloop()


def delBook(book):
    cursor=conn.cursor()
    id=book[0]
    cursor.execute("DELETE FROM BOOKS WHERE ID=?", (id,))
    conn.commit()
    messagebox.showinfo("Info", "Book deleted successfully!")





def modifybook(book, title_entry, author_entry, genre_entry, language_entry, year_entry, csp, isbn_entry):
    id=book[0]
    title = title_entry.get()
    author = author_entry.get()
    genre=genre_entry.get()
    language=language_entry.get()
    year = year_entry.get()
    csp = csp
    isbn=isbn_entry.get()

    cursor = conn.cursor()
    cursor.execute("UPDATE BOOKS SET TITLE=?, AUTHOR=?, GENRE=?, LANGUAGE=?, year=?, CONTEMPLATION_SUR_PLACE=? WHERE ID=?", (title, author,genre, language,year, csp,id ))

    conn.commit()
    messagebox.showinfo("Info", "Book modified successfully!")


def modBook1(book):
    modBook = tk.Tk()
    modBook.title("Modifier un livre")
    title_label = ttk.Label(modBook, text="Titre :")
    title_label.pack()
    title_entry =ttk.Entry(modBook)
    title_entry.insert(0, book[1])
    title_entry.pack()

    author_label = ttk.Label(modBook, text="Auteur :")
    author_label.pack()
    author_entry =ttk.Entry(modBook)
    author_entry.insert(0, book[2])
    author_entry.pack()

    isbn_label = ttk.Label(modBook, text="ISBN :")
    isbn_label.pack()
    isbn_entry =ttk.Entry(modBook)
    isbn_entry.insert(0, book[7])
    isbn_entry.pack()

    genre_label = ttk.Label(modBook, text="Genre :")
    genre_label.pack()
    genre_entry =ttk.Entry(modBook)
    genre_entry.insert(0, book[3])
    genre_entry.pack()

    language_label = ttk.Label(modBook, text="Langue :")
    language_label.pack()
    language_entry =ttk.Entry(modBook)
    language_entry.insert(0, book[4])
    language_entry.pack()

    year_label = ttk.Label(modBook, text="année :")
    year_label.pack()
    year_entry =ttk.Entry(modBook)
    year_entry.insert(0, book[5])
    year_entry.pack()

    csp_label = ttk.Label(modBook, text="Contemplation sur place :")
    csp_label.pack()
    csp = tk.IntVar()


    option1 = ttk.Radiobutton(modBook, text="oui", variable=csp, value=1)
    option1.pack()

    option2 = ttk.Radiobutton(modBook, text="non", variable=csp, value=0)
    option2.pack()

    modifier_button =ttk.Button(modBook, text="Modifier", command=lambda: modifybook1(book, title_entry, author_entry, genre_entry, language_entry, year_entry, 1 if csp=="oui" else 0, isbn_entry))
    modifier_button.pack()
    modBook.mainloop()

def modifybook1(book, title_entry, author_entry, genre_entry, language_entry, year_entry, csp_entry, isbn_entry):
    id=book[0]
    title = title_entry.get()
    author = author_entry.get()
    genre=genre_entry.get()
    language=language_entry.get()
    year = year_entry.get()
    csp = csp_entry
    isbn=isbn_entry.get()

    cursor = conn.cursor()
    cursor.execute("UPDATE BOOKS SET TITLE=?, AUTHOR=?, GENRE=?, LANGUAGE=?, year=?, CONTEMPLATION_SUR_PLACE=? WHERE ID=?", (title, author,genre, language,year, csp,id ))

    conn.commit()
    messagebox.showinfo("Info", "Book modified successfully!")

##SEACH BOOK FUNCTION
def searchBook(searchbook_entry, BookTree):
    search_query = searchbook_entry.get()
    for item in BookTree.get_children():
        print(type(item))
        BookTree.delete(item)
        BookTree.update()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOKS WHERE ID LIKE ? OR TITLE  LIKE ? OR AUTHOR LIKE ? OR GENRE LIKE ? OR LANGUAGE LIKE ? OR year LIKE ? OR ISBN LIKE ?", ('%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%'))
    books = cursor.fetchall()
    for book in books:
        BookTree.insert("", "end", text="", values=(book[0],book[7], book[1], book[2], book[3],book[4], book[5], "oui" if book[6]==1 else "non"))

##ADD BOOK FUNCTION

def addBook(BookTree, title_entry,author_entry,genre_entry, language_entry, year_entry, ISBN_entry,cpsp, entry_image_path):
    title = title_entry.get()
    author = author_entry.get()
    language = language_entry.get()
    genre = genre_entry.get()
    year = year_entry.get()
    ISBN = ISBN_entry.get()
    contemplation_sur_place=cpsp.get()
    image_path=entry_image_path.get()
    with open(image_path, 'rb') as f:
            image_data = f.read()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO BOOKS(title, author, language, genre, year, ISBN, contemplation_sur_place, image) VALUES (?, ?, ?, ?, ?, ?,?,?)", (title, author,language,genre,year,ISBN, contemplation_sur_place, image_data))
        conn.commit()
        messagebox.showinfo("Info", "Book added successfully!")
        id=cursor.lastrowid
        messagebox.showinfo("Info", "Book added successfully!")
    except Exception as e:
        messagebox.showinfo("INFO", "Veuiller saisir les données correctement \n }")
        print(str(e))
    BookTree.insert("", "end", text="", values=(id, ISBN, title, author, language, genre, year, "oui" if contemplation_sur_place==1 else "non"))


def showBookInfoClient(BookTree):
    selected_items = BookTree.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = BookTree.item(selected_item)['values']
        selected_id = int(values[0])
    print(selected_id)
    print(type(selected_id))
    ficheinfoc(selected_id)
##
def reserver(id):
    book_id=int(id)
    print(id)
    client_id=int(id)
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM BOOKS WHERE ID=? and CONTEMPLATION_SUR_PLACE=0''' , (book_id,))
    book_to_rent=cursor.fetchone()
    cursor.execute('''SELECT book_id FROM reservations WHERE BOOK_ID=? ''' , (book_id,))
    book_non_reserved=cursor.fetchone()
    if book_to_rent and book_non_reserved:
        cursor.execute("INSERT INTO reservations VALUES(?, ?, date('now'))",(book_id, client_id))
        conn.commit()
        messagebox.showinfo("Info","Reservation effectuée avec succes!")
    elif not book_to_rent:
        messagebox.showinfo("Info","Livre non disponible pour l'emprunt!'")
    elif not book_non_reserved:
        messagebox.showinfo("Info","Livre deja reserve pour l'emprunt!'")

##
def searchBook1(search_type, searchbook_entry1, BookTree):
    search_query = searchbook_entry1.get()
    print(search_type.get())
    for item in BookTree.get_children():
        BookTree.delete(item)
        BookTree.update()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOOKS WHERE {} LIKE ? ".format(search_type.get()), ('%'+search_query+'%',))
    books = cursor.fetchall()
    for book in books:
        BookTree.insert("", "end", text="", values=(book[0],book[7], book[1], book[2], book[3],book[4], book[5], "oui" if book[6]==1 else "non"))



