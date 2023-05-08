import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random
import string
import admin
import login
import qsqds
import book_functions
import client_functions

def ficheinfo( selected_id):
    root2=tk.Toplevel()
    cursor = conn.cursor()
    frame = tk.Frame(root2)
    frame.pack()
    # Retrieve the image data from the database
    cursor.execute("SELECT * FROM BOOKS WHERE id=?", (selected_id,))
    book=cursor.fetchone()
    image_data = book[8]
    # Convert the image data to a Tkinter-compatible format
    photo_image = tk.PhotoImage(data=image_data)

    # Create a Label widget to display the image
    frame.image = photo_image
    image_label = ttk.Label(frame, image=photo_image)
    image_label.pack(side='left', anchor='nw')
    isbn_label = ttk.Label(frame, text="ISBN: {}".format(book[7]))
    title_label = ttk.Label(frame, text="Title : {}".format(book[1]))
    author_label = ttk.Label(frame, text=" Author: {}".format(book[2]))
    genre_label = ttk.Label(frame, text=" Genre: {}".format(book[3]))
    language_label = ttk.Label(frame, text=" Langue: {}".format(book[4]))
    year_label = ttk.Label(frame, text="année: {}".format(book[5]))
    csp_label = ttk.Label(frame, text="Contemplation sur place: {}".format(book[6]))


    isbn_label.pack()
    title_label.pack()
    author_label.pack()
    genre_label.pack()
    language_label.pack()
    year_label.pack()
    csp_label.pack()

    modBook_button =ttk.Button(frame, text="Modify", command=lambda: modBook(book))
    modBook_button.pack()
    delBook_button =ttk.Button(frame, text="Delete", command=lambda: delBook(book))
    delBook_button.pack()

    root2.mainloop()

def ficheinfoc(selected_id):
    root2=tk.Toplevel()
    cursor = conn.cursor()
    frame = tk.Frame(root2)
    frame.pack()
    # Retrieve the image data from the database
    cursor.execute("SELECT * FROM BOOKS WHERE id=?", (selected_id,))
    book=cursor.fetchone()
    image_data = book[8]
    # Convert the image data to a Tkinter-compatible format
    photo_image = tk.PhotoImage(data=image_data)

    # Create a Label widget to display the image
    frame.image = photo_image
    image_label = ttk.Label(frame, image=photo_image)
    image_label.pack(side='left', anchor='nw')
    isbn_label = ttk.Label(frame, text="ISBN: {}".format(book[7]))
    title_label = ttk.Label(frame, text="Title : {}".format(book[1]))
    author_label = ttk.Label(frame, text=" Author: {}".format(book[2]))
    genre_label = ttk.Label(frame, text=" Genre: {}".format(book[3]))
    language_label = ttk.Label(frame, text=" Langue: {}".format(book[4]))
    year_label = ttk.Label(frame, text="année: {}".format(book[5]))
    csp_label = ttk.Label(frame, text="Contemplation sur place: {}".format(book[6]))


    isbn_label.pack()
    title_label.pack()
    author_label.pack()
    genre_label.pack()
    language_label.pack()
    year_label.pack()
    csp_label.pack()

    modBook_button =ttk.Button(frame, text="Reserver", command=lambda: reserver(selected_id))
    modBook_button.pack()


    root2.mainloop()