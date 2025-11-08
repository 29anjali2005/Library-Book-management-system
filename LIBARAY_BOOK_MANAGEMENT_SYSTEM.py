import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. Connect to MySQL Database
# ----------------------------------------------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # change this as per your MySQL setup
    database="library_book_management"
)

cursor = mydb.cursor()

# ----------------------------------------------------------
# 2. GUI Functions
# ----------------------------------------------------------

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    category = category_entry.get()
    if title and author and category:
        cursor.execute("INSERT INTO books (title, author, category) VALUES (%s, %s, %s)", (title, author, category))
        mydb.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        category_entry.delete(0, END)
    else:
        messagebox.showerror("Input Error", "All fields are required!")

def view_books():
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    for row in tree_books.get_children():
        tree_books.delete(row)
    for row in rows:
        tree_books.insert("", END, values=row)

def delete_book():
    book_id = delete_book_id_entry.get()
    if book_id:
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Book deleted successfully!")
        delete_book_id_entry.delete(0, END)
    else:
        messagebox.showerror("Input Error", "Please enter a Book ID")

def add_member():
    name = member_name_entry.get()
    contact = member_contact_entry.get()
    if name and contact:
        cursor.execute("INSERT INTO members (name, contact) VALUES (%s, %s)", (name, contact))
        mydb.commit()
        messagebox.showinfo("Success", "Member added successfully!")
        member_name_entry.delete(0, END)
        member_contact_entry.delete(0, END)
    else:
        messagebox.showerror("Input Error", "All fields are required!")

def view_members():
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    for row in tree_members.get_children():
        tree_members.delete(row)
    for row in rows:
        tree_members.insert("", END, values=row)

def delete_member():
    member_id = delete_member_id_entry.get()
    if member_id:
        cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Member deleted successfully!")
        delete_member_id_entry.delete(0, END)
    else:
        messagebox.showerror("Input Error", "Please enter a Member ID")

def show_category_chart():
    cursor.execute("SELECT category, COUNT(*) FROM books GROUP BY category")
    data = cursor.fetchall()
    categories = [row[0] for row in data]
    counts = [row[1] for row in data]
    plt.bar(categories, counts)
    plt.xlabel("Category")
    plt.ylabel("Number of Books")
    plt.title("Books by Category")
    plt.show()

# ----------------------------------------------------------
# 3. GUI Layout
# ----------------------------------------------------------

root = Tk()
root.title("📚 Library Management System")

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# ---------------- Tab 1: Add Book ----------------
tab1 = Frame(notebook)
notebook.add(tab1, text='Add Book')

Label(tab1, text="Title:").grid(row=0, column=0, padx=10, pady=10)
Label(tab1, text="Author:").grid(row=1, column=0, padx=10, pady=10)
Label(tab1, text="Category:").grid(row=2, column=0, padx=10, pady=10)

title_entry = Entry(tab1, width=30)
author_entry = Entry(tab1, width=30)
category_entry = Entry(tab1, width=30)

title_entry.grid(row=0, column=1, padx=10, pady=10)
author_entry.grid(row=1, column=1, padx=10, pady=10)
category_entry.grid(row=2, column=1, padx=10, pady=10)

Button(tab1, text="Add Book", command=add_book).grid(row=3, column=0, columnspan=2, pady=20)

# ---------------- Tab 2: View Books ----------------
tab2 = Frame(notebook)
notebook.add(tab2, text='View Books')

cols = ("ID", "Title", "Author", "Category")
tree_books = ttk.Treeview(tab2, columns=cols, show='headings')
for col in cols:
    tree_books.heading(col, text=col)
tree_books.pack(expand=1, fill="both")

Button(tab2, text="Refresh Books", command=view_books).pack(pady=10)

# ---------------- Tab 3: Delete Book ----------------
tab3 = Frame(notebook)
notebook.add(tab3, text='Delete Book')

Label(tab3, text="Enter Book ID to Delete:").pack(pady=10)
delete_book_id_entry = Entry(tab3, width=30)
delete_book_id_entry.pack(pady=5)

Button(tab3, text="Delete Book", command=delete_book).pack(pady=10)

# ---------------- Tab 4: Add Member ----------------
tab4 = Frame(notebook)
notebook.add(tab4, text='Add Member')

Label(tab4, text="Member Name:").grid(row=0, column=0, padx=10, pady=10)
Label(tab4, text="Contact:").grid(row=1, column=0, padx=10, pady=10)

member_name_entry = Entry(tab4, width=30)
member_contact_entry = Entry(tab4, width=30)

member_name_entry.grid(row=0, column=1, padx=10, pady=10)
member_contact_entry.grid(row=1, column=1, padx=10, pady=10)

Button(tab4, text="Add Member", command=add_member).grid(row=2, column=0, columnspan=2, pady=20)

# ---------------- Tab 5: View Members ----------------
tab5 = Frame(notebook)
notebook.add(tab5, text='View Members')

cols = ("ID", "Name", "Contact")
tree_members = ttk.Treeview(tab5, columns=cols, show='headings')
for col in cols:
    tree_members.heading(col, text=col)
tree_members.pack(expand=1, fill="both")

Button(tab5, text="Refresh Members", command=view_members).pack(pady=10)

# ---------------- Tab 6: Delete Member ----------------
tab6 = Frame(notebook)
notebook.add(tab6, text='Delete Member')

Label(tab6, text="Enter Member ID to Delete:").pack(pady=10)
delete_member_id_entry = Entry(tab6, width=30)
delete_member_id_entry.pack(pady=5)

Button(tab6, text="Delete Member", command=delete_member).pack(pady=10)

# ---------------- Tab 7: Charts ----------------
tab7 = Frame(notebook)
notebook.add(tab7, text='Charts')
Button(tab7, text="Show Category Chart", command=show_category_chart).pack(pady=20)
root.mainloop()
